import datetime
import json
import logging
import random
import string
from typing import Any, Dict, List, Optional

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from llama_index.core.chat_engine.types import BaseChatEngine
from llama_index.core.llms import ChatMessage, CompletionResponse, MessageRole
from llama_index.core.vector_stores.types import ExactMatchFilter, MetadataFilters
from pydantic import BaseModel

from raw.engine import get_index, init_settings

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

init_settings()
app = FastAPI()

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


class Message(BaseModel):
    role: MessageRole
    content: str


class ChatData(BaseModel):
    messages: List[Message]
    patient_id: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "messages": [
                        {
                            "role": "system",
                            "content": "Antworte immer auf deutsch. Bleibe kurz und knapp.",
                        },
                        {"role": "user", "content": "Was ist die Diagnose?"},
                    ],
                    "patient_id": "p1",
                }
            ]
        }
    }


class SourceNode(BaseModel):
    node_id: str
    text: str
    metadata: Optional[Dict[str, Any]]


class ChatResponse(BaseModel):
    source_nodes: Optional[List[SourceNode]]
    message: str
    created_at: str
    total_duration: float
    done: bool


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/documents")
def documents(patient_id: str):
    random.seed(patient_id)

    def generate_random_date():
        start_date = datetime.date(2020, 1, 1)
        end_date = datetime.date.today()
        random_date = start_date + datetime.timedelta(
            days=random.randint(0, (end_date - start_date).days)
        )
        return random_date.isoformat()

    def generate_random_filename():
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for _ in range(10)) + ".pdf"

    return [
        {
            "id": i,
            "created_at": generate_random_date(),
            "filename": generate_random_filename(),
            "patient_id": patient_id,
        }
        for i in range(5)
    ]


@app.post("/chat")
async def chat(
    request: Request,
    data: ChatData,
    index: BaseChatEngine = Depends(get_index),
) -> ChatResponse:
    return await _chat(request, data, index, stream=False)


@app.post("/stream_chat")
async def stream_chat(
    request: Request,
    data: ChatData,
    index: BaseChatEngine = Depends(get_index),
) -> ChatResponse:
    return await _chat(request, data, index, stream=True)


async def _chat(request: Request, data: ChatData, index: BaseChatEngine, stream=False):
    if len(data.messages) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No messages provided",
        )

    last_message = data.messages.pop()
    if last_message.role != MessageRole.USER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Last message must be from user",
        )

    messages = [
        ChatMessage(
            role=m.role,
            content=m.content,
        )
        for m in data.messages
    ]

    chat_engine = index.as_chat_engine(
        similarity_top_k=3,
        chat_mode="context",
        use_async=False,
        filters=MetadataFilters(
            filters=[
                ExactMatchFilter(
                    key="patient_id",
                    value=data.patient_id,
                )
            ]
        ),
    )

    if stream:
        response = await chat_engine.astream_chat(last_message.content, messages)
        response_generator = stream_chat_generator(response, request)
        return StreamingResponse(response_generator, media_type="application/json")

    start = datetime.datetime.utcnow()
    response = chat_engine.chat(last_message.content, messages)
    end = datetime.datetime.utcnow()
    total_duration = (end - start).total_seconds() * 1000

    source_nodes = [
        {"node_id": node.id_, "text": node.text, "metadata": node.metadata}
        for node in response.source_nodes
    ]

    data = {
        "source_nodes": source_nodes,
        "message": response.response,
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        "total_duration": total_duration,
        "done": True,
    }
    return data


async def stream_chat_generator(response, request):
    start = datetime.datetime.utcnow()

    # First reply: source nodes
    source_nodes = [
        {"node_id": node.id_, "text": node.text, "metadata": node.metadata}
        for node in response.source_nodes
    ]
    data = {
        "source_nodes": source_nodes,
        "message": "",
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        "total_duration": 0,
        "done": False,
    }
    yield json.dumps(data)

    # Subsequent replies: generated tokens
    async for response in response.async_response_gen():
        if await request.is_disconnected():
            # If client closes connection, stop sending events
            return

        if isinstance(response, CompletionResponse):
            response = response.delta

        yield json.dumps(
            {
                "created_at": datetime.datetime.utcnow().isoformat() + "Z",
                "message": response,
                "done": False,
            }
        ) + "\n"
    end = datetime.datetime.utcnow()
    total_duration = (end - start).total_seconds() * 1000

    # Final reply: done and total duration
    yield json.dumps(
        {
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
            "message": "",
            "done": True,
            "total_duration": total_duration,
        }
    ) + "\n"
