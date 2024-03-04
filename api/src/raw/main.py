import json
import datetime
import logging

from raw.ollama import Ollama
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi import Request

from llama_index.core import Settings

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)


async def generate_messages(response_gen):
    start = datetime.datetime.utcnow()
    async for token in response_gen:
        yield {
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
            "message": token.delta,
            "done": False,
        }
    end = datetime.datetime.utcnow()
    total_duration = (end - start).total_seconds() * 1000

    yield {
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        "message": "",
        "done": True,
        "total_duration": total_duration,
    }


def init_settings():
    Settings.llm = Ollama(
        model="mixtral:latest",
        base_url="https://mirage.kite.ume.de/ollama",
        request_timeout=240,
        temperature=0,
    )


init_settings()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/complete")
async def complete(prompt: str, request: Request):
    response = await Settings.llm.astream_complete(prompt)

    async def event_generator():
        async for message in generate_messages(response):
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break
            yield json.dumps(message) + "\n"

    return StreamingResponse(event_generator(), media_type="application/json")
