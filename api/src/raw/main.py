from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/query/")
def query(patient_id: str, query: str):
    return {"patient_id": patient_id, "query": query}
