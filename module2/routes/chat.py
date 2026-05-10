from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from models.schemas import ChatRequest, ChatResponse
from services.llm import get_full_response, stream_generator

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = await get_full_response(request)
        return ChatResponse(response=response, model=request.model)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stream")
async def chat_stream(request: ChatRequest):
    return StreamingResponse(
        stream_generator(request),
        media_type="text/event-stream",
        headers={"X-Accel-Buffering": "no"}
    )