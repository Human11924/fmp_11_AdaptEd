from fastapi import FastAPI
from app.api.chat import router as chat_router

app = FastAPI(title="Gemini FastAPI RAG Agent")

app.include_router(chat_router)
