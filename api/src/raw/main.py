import logging
import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from raw.engine import init_settings
from raw.routes import chat, fhir

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)


if __name__ == "__main__":
    import os
    os.environ["QDRANT_LOCATION"] = 'http://localhost:6333/'
    os.environ["QDRANT_COLLECTION"] = 'mtb_protocols'
    os.environ["OLLAMA_BASE_URL"] = 'https://mirage.kite.ume.de/ollama'


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


# these lines are only for starting the backend with the debugger
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
