import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from raw.engine import init_settings
from raw.routes import chat, fhir

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

init_settings()
app = FastAPI()
app.include_router(chat.router)
app.include_router(fhir.router)

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}
