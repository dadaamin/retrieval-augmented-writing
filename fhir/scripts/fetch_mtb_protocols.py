from dotenv import load_dotenv, find_dotenv
from fhir_pyrate import Ahoy
from fhir_pyrate import Pirate
import pandas as pd
import requests
from tqdm import tqdm
import requests

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

fields = ['id', 'presentedForm.url', 'presentedForm.contentType']
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

all_documents = obs.explode(["presentedForm.contentType", "presentedForm.url"])
text_documents = all_documents[all_documents["presentedForm.contentType"] == "text/plain; charset=UTF-8"]

def download_doc(url, id):
    res = auth.session.get(url)
    text = res.content.decode("utf-8")
    with open(f"docs/{id}.txt", "w") as f_w:
        f_w.write(text)

text_documents.apply(lambda x: download_doc(x["presentedForm.url"], x["id"]), axis=1)
