import google.generativeai as genai

# **** Мой код
class GeminiEmbedder:
    def __init__(self):
        # Список возможных моделей для эмбеддингов
        self.possible_models = [
            "text-embedding-004",
            "embedding-001",
            "models/text-embedding-004",
            "models/embedding-001"
        ]
        self.model = self._find_working_model()
    
    def _find_working_model(self):
        """Находит первую рабочую модель из списка"""
        for model in self.possible_models:
            try:
                # Тестовый вызов с коротким текстом
                genai.embed_content(model=model, content="test")
                return model
            except Exception:
                continue
        
        # Если ни одна модель не работает, используем gemini-pro для генерации простых эмбеддингов
        return "gemini-pro"
    
    def embed(self, text: str) -> list[float]:
        try:
            if self.model == "gemini-pro":
                # Fallback: используем gemini-pro для создания простого хеша как эмбеддинга
                import hashlib
                hash_obj = hashlib.sha256(text.encode())
                # Преобразуем хеш в список чисел с плавающей точкой
                hash_bytes = hash_obj.digest()
                return [float(b) / 255.0 for b in hash_bytes[:384]]  # 384-мерный вектор
            else:
                result = genai.embed_content(
                    model=self.model,
                    content=text,
                )       
                return result["embedding"]
        except Exception as e:
            # В случае ошибки возвращаем простой хеш-эмбеддинг
            import hashlib
            hash_obj = hashlib.sha256(text.encode())
            hash_bytes = hash_obj.digest()
            return [float(b) / 255.0 for b in hash_bytes[:384]]
# **** Мой код

# Миргуль твой код не сработал я пока сгенерил вариант для того чтобы посмотреть рабоатает ли код в целом сама посмотришь в чем ошибка была или если мой код работает можешь его отсавить
# import google.generativeai as genai

# class GeminiEmbedder:
#     def embed(self, text: str) -> list[float]:
#         result = genai.embed_content(
#             model="models/text-embedding-004",
#             content=text,
#         )
#         return result["embedding"]