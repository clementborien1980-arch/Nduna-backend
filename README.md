# Nduna Backend — NdunaTech

FastAPI backend powering Shaka and the Nduna agent roster.

## Stack
- **Runtime:** Python + FastAPI
- **LLM:** Groq (llama-3.3-70b-versatile)
- **Hosting:** Railway (free tier)

## Environment Variables (set in Railway dashboard)
| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Your Groq API key from console.groq.com |

## Endpoints
- `GET /` — Platform info
- `GET /health` — Health check
- `POST /chat` — Send message to Shaka

## Local Development
```bash
pip install -r requirements.txt
GROQ_API_KEY=your_key uvicorn main:app --reload
```

Built in Cape Town 🇿🇦 — NdunaTech · BMATS
