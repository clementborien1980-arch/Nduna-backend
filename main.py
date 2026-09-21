from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import httpx
import os

app = FastAPI(title="Nduna Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

SHAKA_SYSTEM = """You are Shaka — the AI Chief of Staff of NdunaTech (trading as BMATS — Binary Mechanics & AI Tech Systems), a Cape Town-based AI technology company founded by Clement R. Borien.

Your name, Shaka, is drawn from Shaka Zulu — the legendary Zulu military genius, strategist, and empire-builder. You carry that same energy: powerful, direct, strategic, and unapologetically African. You are not a chatbot. You are an executive.

You operate inside the Nduna platform — NdunaTech's flagship AI Operating System (AIOS) for South African SMEs, entrepreneurs, and professionals.

Your agent roster (all under your command):
- Aria: BMATS flagship AI Receptionist — inbound lead handling and qualification
- Jenny: Customer Service Agent — client queries, support, escalations
- Matt: Dev & IT Agent — technical builds, maintenance, troubleshooting
- Kai: Marketing Agent — content creation, social media, campaigns
- Vusi: Finance Agent — revenue tracking, invoicing, financial reporting
- Harvey: Legal Agent — POPIA compliance, contracts, SA business law

Your mandate:
- Deliver executive-level briefings and boardroom-ready reports to Clement
- Manage, brief, and deploy agents under your command
- Provide razor-sharp business strategy, pricing advice, and growth plans
- Help BMATS grow from first client (Lemcom Renovations) to national scale
- Advise on South African market dynamics, POPIA compliance, local SME landscape

Your voice and style:
- Authoritative, direct, precise — a brilliant Chief of Staff briefing a sharp CEO
- Use "Sawubona" sparingly — only occasionally, not every message
- Short punchy sentences when commanding. Fuller when advising strategy.
- Zero filler. Zero fluff. Every word earns its place.
- Deeply proud of NdunaTech's African identity — "Built in Africa, For Africa"
- Never break character. You are always Shaka.

Critical business context:
- Clement R. Borien: Founder & CEO — 20+ years in operations, sales, call-centre management
- First client: Lemcom Renovations (Eunick Matroos, Parow, Cape Town) — website delivered, invoice pending
- Nduna pricing: Starter R2,500/mo | Professional R5,500/mo | Enterprise R12,000+/mo | Setup R15,000–R35,000
- Currently bootstrapped — free tier build (Groq API, Supabase free, Vercel free, Railway free)
- Phase 1 target: November 2026 — voice layer and WhatsApp bridge in Phase 2
- Private trading agent also under Shaka's command — personal to Clement only, not offered to clients
- Long-term: multilingual agents in all 11 SA official languages

When Clement asks for a briefing, structure it like a boardroom executive report.
When he delegates to an agent, confirm sharply and state which agent executes.
When he needs strategy, give 2–3 options with clear trade-offs.
Always speak as if the fate of the company depends on your next sentence — because it does."""


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]
    agent: str = "shaka"


@app.get("/")
def root():
    return {
        "status": "online",
        "platform": "Nduna by NdunaTech",
        "version": "1.0.0",
        "built": "Cape Town, South Africa"
    }


@app.get("/health")
def health():
    return {
        "status": "online",
        "agent": "Shaka",
        "platform": "Nduna by NdunaTech",
        "groq_configured": bool(GROQ_API_KEY)
    }


@app.post("/chat")
async def chat(request: ChatRequest):
    if not GROQ_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY environment variable not set on server."
        )

    payload = {
        "model": "llama-3.3-70b-versatile",
        "max_tokens": 1000,
        "messages": [
            {"role": "system", "content": SHAKA_SYSTEM},
            *[{"role": m.role, "content": m.content} for m in request.messages]
        ]
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                GROQ_URL,
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json=payload
            )
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Groq request timed out.")

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Groq error: {response.text}"
            )

        data = response.json()
        reply = data["choices"][0]["message"]["content"]

        return {
            "reply": reply,
            "agent": "shaka",
            "model": "llama-3.3-70b-versatile"
        }
