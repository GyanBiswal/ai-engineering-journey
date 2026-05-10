from openai import AsyncOpenAI
from core.config import settings
import json

client = AsyncOpenAI(
    base_url=settings.ollama_base_url,
    api_key="ollama"
)

async def get_full_response(request) -> str:
    result = await client.chat.completions.create(
        model=request.model,
        temperature=request.temperature,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": request.message}
        ]
    )
    return result.choices[0].message.content

async def stream_generator(request):
    stream = await client.chat.completions.create(
        model=request.model,
        temperature=request.temperature,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": request.message}
        ],
        stream=True
    )
    async for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield f"data: {json.dumps({'token': delta})}\n\n"
    yield "data: [DONE]\n\n"