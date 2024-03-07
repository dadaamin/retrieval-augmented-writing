import json
import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from tqdm.auto import tqdm

tqdm.pandas()

from fhir_pyrate import Ahoy, Pirate

form_to_ext = {
    "text/plain; charset=UTF-8": "txt",
    "application/pdf": "pdf",
    "image/tiff": "tiff",
    "application/msword": "docx",
}

load_dotenv(find_dotenv())

auth = Ahoy(
    auth_type="token",
    auth_method="env",
    auth_url=os.environ["BASIC_AUTH"],  # The URL for authentication
    refresh_url=os.environ["BASIC_AUTH"],  # The URL to refresh the authentication
)
search = Pirate(
    auth=auth,
    base_url=os.environ["SEARCH_URL"],  # e.g. "http://hapi.fhir.org/baseDstu2"
    print_request_url=True,  # If set to true, you will see all requests
)

with open("fhir/data/mtb-patients.json") as f_r:
    mtb_patients = json.load(f_r)


def download_file(url):
    res = auth.session.get(url)
    return res.content


def download_document(doc):
    base_path = f"fhir/data/docs/{doc['id']}"
    presented_form = []
    if isinstance(doc["presentedForm.contentType"], list):
        doc_path = []
        for form, url, creation in zip(
            doc["presentedForm.contentType"],
            doc["presentedForm.url"],
            doc["presentedForm.creation"],
        ):
            if not Path(f"{base_path}.{form_to_ext[form]}").exists():
                content = download_file(url)
                with open(f"{base_path}.{form_to_ext[form]}", "wb") as f_w:
                    f_w.write(content)
            doc_path.append(f"{base_path}.{form_to_ext[form]}")

            presented_form.append(
                {
                    "url": url,
                    "contentType": form,
                    "creation": creation,
                    "path": f"{base_path}.{form_to_ext[form]}",
                }
            )

    else:
        doc_path = f"{base_path}.{form_to_ext[doc['presentedForm.contentType']]}"
        if not Path(doc_path).exists():
            content = download_file(doc["presentedForm.url"])
            with open(doc_path, "wb") as f_w:
                f_w.write(content)

        presented_form.append(
            {
                "url": doc["presentedForm.url"],
                "contentType": doc["presentedForm.contentType"],
                "creation": doc["presentedForm.creation"],
                "path": doc_path,
            }
        )
    return presented_form


def fetch_patient_documents(patient_id):
    fields = [
        "resourceType",
        "id",
        "presentedForm.url",
        "presentedForm.contentType",
        "presentedForm.creation",
        "subject.reference",
        "meta.versionid",
        "meta.lastUpdated",
        "path",
    ]

    documents = search.steal_bundles_to_dataframe(
        resource_type="DiagnosticReport",
        request_params={
            "subject": f"Patient/{patient_id}",
            "_sort": "-date",
            "_count": 500,
        },
        fhir_paths=fields,  # type: ignore
    )
    documents = documents[documents["presentedForm.url"].notnull()]
    tqdm.pandas(desc="Downloading documents")
    documents["presentedForm"] = documents.progress_apply(download_document, axis=1)
    documents = documents.drop(
        ["presentedForm.url", "presentedForm.contentType", "presentedForm.creation"],
        axis=1,
    )

    return documents


for patient in mtb_patients:
    documents = fetch_patient_documents(patient["patient_id"])

documents = documents.to_dict(orient="records")

with open("fhir/data/patient-documents.json", "w") as f_w:
    json.dump(documents, f_w)
