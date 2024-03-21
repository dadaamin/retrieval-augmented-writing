import json
from datetime import datetime
from pathlib import Path

from llama_index.core.readers import SimpleDirectoryReader

from raw.engine import create_index, init_settings
from raw.loader import PDFReaderPlus, TesseractReader

INDEXING_PRIORITY = {
    "text/plain; charset=UTF-8": 0,
    "text/richtext; charset=UTF-8": 1,
    "application/msword": 2,
    "application/pdf": 3,
    "image/jpeg": 4,
    "image/tiff": 4,
    "application/zip": 999,
}

PDF_READER = PDFReaderPlus(language="deu")
IMAGE_READER = TesseractReader()
CUSTOM_READERS = {
    ".pdf": PDF_READER,
    ".png": IMAGE_READER,
    ".jpg": IMAGE_READER,
    ".jpeg": IMAGE_READER,
    ".tiff": IMAGE_READER,
}


PATIENTS_JSON = Path("../fhir/data/mtb-patients.json")
DOCUMENTS_JSON = Path("../fhir/data/patient-documents.jsonl")
DOCS_BASE_PATH = Path("../fhir/data/docs/")


def str_to_datetime(date_str):
    date_format = "%Y-%m-%dT%H:%M:%S.%f%z"
    return datetime.strptime(date_str, date_format)


def main():
    with open(PATIENTS_JSON) as fin:
        patients = json.load(fin)

    for doc in patients:
        doc["mtb_creation"] = str_to_datetime(doc["mtb_creation"])

    # Determine date of first MTB protocol for each patient
    # We will only keep documents *before* that timestamp.
    cutoffs = {}
    patients = sorted(patients, key=lambda doc: doc["mtb_creation"])
    for doc in patients:
        patient_id = doc["patient_id"]
        if patient_id in cutoffs:
            continue
        cutoffs[patient_id] = doc["mtb_creation"]

    docs = []
    with open(DOCUMENTS_JSON) as fin:
        for line in fin.readlines():
            doc = json.loads(line)
            doc["patient_id"] = doc.pop("subject.reference")
            docs.append(doc)

    # metadata = {file_name: metadata}
    #
    # Example
    # =======
    # metadata['2c31892d26bde905dc49de72550d02c96eaabd787f46b258c8d9f9eb209cd45f.tiff']
    # {'id': '2c31892d26bde905dc49de72550d02c96eaabd787f46b258c8d9f9eb209cd45f',
    #  'meta.lastUpdated': '2023-03-21T08:25:52.182+00:00',
    #  'patient_id': 'Patient/70cd56ad887462a0bff46c879ea4dfb478b1035e07da61596ba75a526105aad3',
    #  'presentedForm': [{'contentType': 'image/tiff',
    #                     'creation': '2023-03-21T09:17:41.000+01:00',
    #                     'path': '2c31892d26bde905dc49de72550d02c96eaabd787f46b258c8d9f9eb209cd45f.tiff',
    #                     'url': 'https://ship.ume.de/app/docs/medico/101873289'}],
    #  'resourceType': 'DiagnosticReport'}
    metadata = {}
    for doc in docs:
        patient_id = doc["patient_id"]
        last_updated = str_to_datetime(doc["meta.lastUpdated"])
        cutoff = cutoffs[patient_id]

        if last_updated >= cutoff:
            # skip document as it came after first MTB
            continue

        doc["presentedForm"] = sorted(
            doc["presentedForm"], key=lambda x: INDEXING_PRIORITY[x["contentType"]]
        )
        if len(doc["presentedForm"]) == 0:
            # skip document as there is no attachment
            continue

        for form in doc["presentedForm"]:
            form["path"] = Path(form["path"]).name

        # select the first attachment for indexing
        form = doc["presentedForm"][0]
        if INDEXING_PRIORITY[form["contentType"]] == 999:
            # skip document as there is no compatible attachment
            continue
        metadata[form["path"]] = doc

    print(f"Total documents: {len(docs):,}")
    print(f"Documents to index: {len(metadata):,}")

    files_to_index = metadata.keys()
    files_to_index = [DOCS_BASE_PATH / f for f in files_to_index]

    reader = SimpleDirectoryReader(
        input_files=files_to_index,
        filename_as_id=True,
        file_extractor=CUSTOM_READERS,
    )
    print("Load documents from files.")
    docs = reader.load_data(show_progress=True, num_workers=8)

    # Add metadata (presented forms, ship ID, patient_id, ...)
    # and drop paths and redundant file names
    for doc in docs:
        doc.doc_id = Path(doc.doc_id).name
        file_name = Path(doc.metadata["file_path"]).name
        doc.metadata["file_name"] = file_name
        doc.metadata["patient_id"] = metadata[file_name]["patient_id"]

    init_settings()
    create_index(docs)


if __name__ == "__main__":
    main()
