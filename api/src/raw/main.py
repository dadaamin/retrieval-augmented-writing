import json
import datetime
import logging

from pydantic import BaseModel

from raw import init_settings, get_llm, get_chat_engine
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import StreamingResponse

from llama_index.core.llms import ChatMessage, MessageRole, CompletionResponse
from llama_index.core.llms.llm import LLM
from llama_index.core.chat_engine.types import BaseChatEngine

from typing import List


logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

init_settings()
app = FastAPI()


class _Message(BaseModel):
    role: MessageRole
    content: str


class _ChatData(BaseModel):
    messages: List[_Message]


class _CompleteData(BaseModel):
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
async def complete(data: _CompleteData, request: Request, llm: LLM = Depends(get_llm)):
    response = await llm.astream_complete(data.prompt)
    response_generator = generate_messages(response, request=request)
    return StreamingResponse(response_generator, media_type="application/json")


@app.post("/chat")
async def chat(
    request: Request,
    data: _ChatData,
    chat_engine: BaseChatEngine = Depends(get_chat_engine),
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
    response = await chat_engine.astream_chat(lastMessage.content, messages)
    response_generator = generate_messages(
        response.async_response_gen(), request=request
    )
    return StreamingResponse(response_generator, media_type="application/json")
