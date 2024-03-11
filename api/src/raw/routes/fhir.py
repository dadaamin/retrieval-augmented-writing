from pathlib import Path
from typing import List

import pandas as pd
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class PresentedForm(BaseModel):
    url: str
    content_type: str
    creation: str
    path: str


class Document(BaseModel):
    document_id: str
    resource_type: str
    patient_id: str
    last_updated: str
    presented_form: List[PresentedForm]


class DocumentContent(BaseModel):
    document_id: str
    url: str
    content_type: str
    creation: str
    content: bytes


def load_documents(json_path):
    df = pd.read_json(json_path, lines=True)
    df = df.rename(  # pylint: disable=E1101
        {
            "id": "document_id",
            "resourceType": "resource_type",
            "subject.reference": "patient_id",
            "meta.lastUpdated": "last_updated",
            "presentedForm": "presented_form",
        },
        axis=1,
    )

    def rename_forms(presented_forms):
        forms = []
        for form in presented_forms:
            forms.append(
                {
                    "url": form["url"],
                    "content_type": form["contentType"],
                    "creation": form["creation"],
                    "path": Path(form["path"]).name,
                }
            )
        return forms

    df["presented_form"] = df["presented_form"].apply(rename_forms)
    return df


def load_patients(json_path):
    return pd.read_json(json_path)


df_patients = load_patients("../fhir/data/mtb-patients.json")
df_documents = load_documents("../fhir/data/patient-documents.jsonl")
base_path_docs = Path("../fhir/data/docs/")


@router.get("/patients")
def patients() -> List[str]:
    return df_patients["patient_id"].values.tolist()


@router.get("/documents", response_model=List[Document])
def documents(patient_id):
    mask = df_documents["patient_id"] == patient_id
    return df_documents[mask].to_dict(orient="records")


@router.get("/document", response_model=Document)
def document(document_id):
    mask = df_documents["document_id"] == document_id
    return df_documents[mask].iloc[0].to_dict()


@router.get("/document_raw")
def document_raw(document_id, presented_form_url) -> DocumentContent:
    doc = document(document_id)
    form = next(
        form for form in doc["presented_form"] if form["url"] == presented_form_url
    )
    path = base_path_docs / Path(form["path"]).name
    with open(path, "rb") as fin:
        content = fin.read()

    return DocumentContent(
        document_id=document_id,
        url=form["url"],
        content_type=form["content_type"],
        creation=form["creation"],
        content=content,
    )
