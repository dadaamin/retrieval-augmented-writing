import datetime
import json
import logging
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import StreamingResponse
from llama_index.core.chat_engine.types import BaseChatEngine
from llama_index.core.llms import ChatMessage, CompletionResponse, MessageRole
from llama_index.core.llms.llm import LLM
from llama_index.core.vector_stores.types import ExactMatchFilter, MetadataFilters
from pydantic import BaseModel

from raw.engine import get_index, get_llm, init_settings

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

init_settings()
app = FastAPI()


class Message(BaseModel):
    role: MessageRole
    content: str


class ChatData(BaseModel):
    messages: List[Message]
    patient_id: str


class CompleteData(BaseModel):
    prompt: str


async def generate_messages(response_gen, request):
    start = datetime.datetime.utcnow()
    async for response in response_gen:
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

    yield json.dumps(
        {
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
            "message": "",
            "done": True,
            "total_duration": total_duration,
        }
    ) + "\n"


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/complete")
async def complete(data: CompleteData, request: Request, llm: LLM = Depends(get_llm)):
    response = await llm.astream_complete(data.prompt)
    response_generator = generate_messages(response, request=request)
    return StreamingResponse(response_generator, media_type="application/json")


@app.post("/chat")
async def chat(
    request: Request,
    data: ChatData,
    index: BaseChatEngine = Depends(get_index),
):
    if len(data.messages) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No messages provided",
        )

    lastMessage = data.messages.pop()
    if lastMessage.role != MessageRole.USER:
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
        chat_mode="condense_plus_context",
        use_async=True,
        filters=MetadataFilters(
            filters=[
                ExactMatchFilter(
                    key="patient_id",
                    value=data.patient_id,
                )
            ]
        ),
    )

    response = await chat_engine.astream_chat(lastMessage.content, messages)
    response_generator = generate_messages(
        response.async_response_gen(), request=request
    )
    return StreamingResponse(response_generator, media_type="application/json")
