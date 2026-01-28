import google.generativeai as genai

class GeminiEmbedder:
    def embed(self, text: str) -> list[float]:
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
        )
        return result["embedding"]
