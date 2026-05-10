import asyncio

from openai import AsyncOpenAI
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# =========================================================
# SETTINGS
# =========================================================

class Settings(BaseSettings):
    ollama_base_url: str = "http://localhost:11434/v1"
    ollama_model: str = "llama3.2"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()


# =========================================================
# CLIENT
# =========================================================

# Ollama supports the OpenAI-compatible API format
client = AsyncOpenAI(
    base_url=settings.ollama_base_url,
    api_key="ollama"  # dummy value required by SDK
)


# =========================================================
# PYDANTIC MODEL
# =========================================================

class ChatRequest(BaseModel):
    message: str
    model: str = settings.ollama_model
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


# =========================================================
# FULL RESPONSE
# =========================================================

async def get_response(request: ChatRequest) -> str:
    response = await client.chat.completions.create(
        model=request.model,
        temperature=request.temperature,
        messages=[
            {
                "role": "user",
                "content": request.message
            }
        ]
    )

    return response.choices[0].message.content


# =========================================================
# STREAM RESPONSE
# =========================================================

async def stream_response(request: ChatRequest) -> None:
    stream = await client.chat.completions.create(
        model=request.model,
        temperature=request.temperature,
        messages=[
            {
                "role": "user",
                "content": request.message
            }
        ],
        stream=True
    )

    async for chunk in stream:
        delta = chunk.choices[0].delta.content

        if delta:
            print(delta, end="", flush=True)

    print()


# =========================================================
# MAIN
# =========================================================

async def main():
    request = ChatRequest(
        message="Explain async programming in Python simply."
    )

    print("\n===== FULL RESPONSE =====\n")

    response = await get_response(request)
    print(response)

    print("\n===== STREAMING RESPONSE =====\n")

    await stream_response(request)


if __name__ == "__main__":
    asyncio.run(main())