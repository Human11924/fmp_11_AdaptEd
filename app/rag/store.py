import numpy as np

class VectorStore:
    def __init__(self):
        self.embeddings = []
        self.texts = []

    def add(self, embedding: list[float], text: str):
        self.embeddings.append(embedding)
        self.texts.append(text)

    def search(self, query_embedding: list[float], top_k: int = 3):
        if not self.embeddings:
            return []

        vectors = np.array(self.embeddings)
        query = np.array(query_embedding)

        similarities = vectors @ query
        top_indices = similarities.argsort()[-top_k:][::-1]

        return [self.texts[i] for i in top_indices]
