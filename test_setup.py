# import httpx
# import asyncio

# async def test_ollama():
#     async with httpx.AsyncClient(timeout=30) as client:
#         response = await client.post(
#             "http://localhost:11434/api/generate",
#             json={
#                 "model": "llama3.2",
#                 "prompt": "Say 'setup complete' and nothing else.",
#                 "stream": False
#             }
#         )
#         data = response.json()
#         print("✅ Ollama working:", data["response"])

# asyncio.run(test_ollama())


import httpx
import asyncio

async def stream_response(prompt: str):
    async with httpx.AsyncClient(timeout=60) as client:
        # stream=True means we get chunks as they arrive
        async with client.stream(
            "POST",
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": True   # key difference
            }
        ) as response:
            async for chunk in response.aiter_lines():
                if chunk:
                    import json
                    data = json.loads(chunk)
                    token = data.get("response", "")
                    print(token, end="", flush=True)  # print each token immediately
                    if data.get("done"):
                        break

asyncio.run(stream_response("Explain RAG in 3 sentences"))