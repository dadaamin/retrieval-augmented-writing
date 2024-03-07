import json
import os
import re
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from fhir_pyrate import Ahoy, Pirate
from tqdm.auto import tqdm

tqdm.pandas()

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

fields = [
    "id",
    "presentedForm.url",
    "presentedForm.contentType",
    "presentedForm.creation",
    "subject.reference",
]
obs = search.steal_bundles_to_dataframe(
    resource_type="DiagnosticReport",
    request_params={
        "_content": "MTB",
        "category": "https://uk-essen.de/HIS/Cerner/Medico/Docs/Type%7cTKPROTOKOLL",
        "_sort": "-date",
        "_count": 500,
    },
    fhir_paths=fields,  # type: ignore
)

all_documents = obs.explode(
    ["presentedForm.contentType", "presentedForm.url", "presentedForm.creation"]
)
text_documents = all_documents[
    all_documents["presentedForm.contentType"] == "text/plain; charset=UTF-8"
]

data_dir = Path("fhir/data/docs")
data_dir.mkdir(parents=True, exist_ok=True)

pattern = r"MTB\s\d{2}\.\d{2}\.\d{4}"


def download_doc(url, id):
    output_file = data_dir / f"{id}.txt"
    if output_file.exists():
        return output_file
    res = auth.session.get(url)
    text = res.content.decode("utf-8")

    if re.search(pattern, text):
        with open(output_file, "w") as f_w:
            f_w.write(text)
        return output_file


tqdm.pandas(desc="Downloading documents")
text_documents["document_path"] = text_documents.progress_apply(
    lambda x: download_doc(x["presentedForm.url"], x["id"]), axis=1
)

text_documents = text_documents[text_documents["document_path"].notna()]

text_documents.rename(
    columns={
        "id": "mtb_id",
        "presentedForm.url": "mtb_url",
        "subject.reference": "patient_id",
        "document_path": "mtb_path",
        "presentedForm.creation": "mtb_creation",
    },
    inplace=True,
)
text_documents["mtb_path"] = text_documents["mtb_path"].astype(str)

text_documents = text_documents.to_dict(orient="records")

with open("fhir/data/mtb-patients.json", "w") as f_w:
    json.dump(text_documents, f_w)
