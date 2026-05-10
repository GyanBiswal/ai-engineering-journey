## FastAPI Structure Rule
main.py     → app setup + include routers
routes/     → HTTP endpoints only
services/   → business logic only  
models/     → Pydantic schemas only
core/       → config only

## Test streaming
curl -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "your prompt"}' \
  --no-buffer