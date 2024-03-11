import datetime
import json
import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from llama_index.core.chat_engine.types import BaseChatEngine
from llama_index.core.llms import ChatMessage, CompletionResponse, MessageRole
from llama_index.core.vector_stores.types import ExactMatchFilter, MetadataFilters
from pydantic import BaseModel

from raw.engine import get_index

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

router = APIRouter()


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


@router.post("/chat")
async def chat(
    request: Request,
    data: ChatData,
    index: BaseChatEngine = Depends(get_index),
) -> ChatResponse:
    return await _chat(request, data, index, stream=False)


@router.post("/stream_chat")
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
