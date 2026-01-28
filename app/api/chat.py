from fastapi import APIRouter
from pydantic import BaseModel
from app.agent.agent import GeminiAgent

router = APIRouter()
agent = GeminiAgent()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    answer = await agent.run(req.message)
    return {"response": answer}
