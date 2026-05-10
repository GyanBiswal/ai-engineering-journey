# Python AI Engineering Patterns

## async/await
- LLM calls are slow → async prevents blocking
- `async def` = pausable function
- `await` = pause here, let others run
- Entry point: `asyncio.run(main())`

## Pydantic
- Data validation for all requests/responses
- `Field(default=x, ge=0, le=2)` = default + constraints
- Use everywhere: API inputs, LLM outputs, config

## Settings (pydantic-settings)
- All config in one `Settings(BaseSettings)` class
- Loads from `.env` automatically
- Never hardcode URLs or keys

## Ollama OpenAI-compatible client
- base_url = "http://localhost:11434/v1"
- api_key = "ollama" (dummy, required by SDK)
- Model name must be exact: "llama3.2" not "llama3"

## Streaming
- stream=True in API call
- `async for chunk in stream:` → chunk.choices[0].delta.content
- Always print with end="", flush=True

## System prompt
- Always add before user message
- {"role": "system", "content": "..."} 
- Makes LLM behavior consistent