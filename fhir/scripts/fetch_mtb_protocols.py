from dotenv import load_dotenv, find_dotenv
from fhir_pyrate import Ahoy
from fhir_pyrate import Pirate
import pandas as pd
import requests
from tqdm import tqdm
import requests
from pathlib import Path
import re
import json

#Params
DICOM_WEB_URL = "https://ship.ume.de/app/DicomWeb/view/deidentified/EA"
SEARCH_URL = "https:/ship.ume.de/app/FHIR/r4"
BASIC_AUTH = "https://ship.ume.de/app/Auth/v1/basicAuth"
REFRESH_AUTH = "https://ship.ume.de/app/Auth/v1/refresh"

load_dotenv(find_dotenv())

auth = Ahoy(
    auth_type="token",
    auth_method="env",
    auth_url=BASIC_AUTH,  # The URL for authentication
    refresh_url=REFRESH_AUTH,  # The URL to refresh the authentication
)
search = Pirate(
    auth=auth,
    base_url="https://ship.ume.de/app/FHIR/r4",  # e.g. "http://hapi.fhir.org/baseDstu2"
    print_request_url=True,  # If set to true, you will see all requests
)

fields = ['id', 'presentedForm.url', 'presentedForm.contentType', 'presentedForm.creation', 'subject.reference']
obs = search.steal_bundles_to_dataframe(
        resource_type="DiagnosticReport",
        request_params={
            "_content" : "MTB",
            "category":"https://uk-essen.de/HIS/Cerner/Medico/Docs/Type%7cTKPROTOKOLL",
            "_sort": "-date",
            "_count": 500
        },
        fhir_paths=fields, # type: ignore
    )

all_documents = obs.explode(["presentedForm.contentType", "presentedForm.url", "presentedForm.creation"])
text_documents = all_documents[all_documents["presentedForm.contentType"] == "text/plain; charset=UTF-8"]

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

text_documents["document_path"] = text_documents.apply(lambda x: download_doc(x["presentedForm.url"], x["id"]), axis=1)

text_documents = text_documents[text_documents["document_path"].notna()]

text_documents.rename(columns={"id": "mtb_id", 
                               "presentedForm.url": "mtb_url",
                               "subject.reference": "patient_id",
                               "document_path": "mtb_path",
                               "presentedForm.creation": "mtb_creation"},
                               inplace=True
                               )
text_documents["mtb_path"] = text_documents["mtb_path"].astype(str)

text_documents = text_documents.to_dict(orient="records")

with open("fhir/data/mtb-patients.json", "w") as f_w:
    json.dump(text_documents, f_w)