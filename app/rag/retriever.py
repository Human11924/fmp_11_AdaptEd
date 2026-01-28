from app.rag.store import VectorStore
from app.rag.embedder import GeminiEmbedder

class Retriever:
    def __init__(self, store: VectorStore):
        self.store = store
        self.embedder = GeminiEmbedder()

    def retrieve(self, query: str, top_k: int = 3) -> str:
        query_embedding = self.embedder.embed(query)
        docs = self.store.search(query_embedding, top_k=top_k)

        if not docs:
            return ""

        return "\n\n".join(docs)
