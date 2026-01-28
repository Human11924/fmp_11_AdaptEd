from pathlib import Path
from app.rag.store import VectorStore
from app.rag.embedder import GeminiEmbedder

# Новый путь: documents.txt внутри папки rag
DOCUMENTS_PATH = Path(__file__).parent / "documents.txt"

def load_knowledge_base() -> VectorStore:
    store = VectorStore()
    embedder = GeminiEmbedder()

    if not DOCUMENTS_PATH.exists():
        print("⚠️ documents.txt не найден")
        return store

    raw_text = DOCUMENTS_PATH.read_text(encoding="utf-8")

    documents = [
        doc.strip()
        for doc in raw_text.split("\n\n")
        if doc.strip()
    ]

    for doc in documents:
        embedding = embedder.embed(doc)
        store.add(embedding, doc)

    print(f"📚 Загружено документов: {len(documents)}")
    return store
