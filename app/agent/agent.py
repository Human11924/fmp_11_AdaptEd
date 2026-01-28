# import os
# import google.generativeai as genai
# from dotenv import load_dotenv

# from app.agent.prompt_loader import load_system_prompt
# from app.rag.bootstrap import load_knowledge_base
# from app.rag.retriever import Retriever


# load_dotenv()


# class GeminiAgent:
#     def __init__(self):
#         genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

#         self.system_prompt = load_system_prompt()

#         self.model = genai.GenerativeModel(
#             model_name="gemini-2.5-flash",
#             system_instruction=self.system_prompt,
#         )

#         self.store = load_knowledge_base()
#         self.retriever = Retriever(self.store)

#     async def run(self, user_message: str) -> str:
#         context = self.retriever.retrieve(user_message)

#         prompt = f"""
# КОНТЕКСТ:
# {context}

# ВОПРОС:
# {user_message}
# """

#         response = self.model.generate_content(prompt)
#         return response.text


import os
from dotenv import load_dotenv
import google.generativeai as genai

from app.agent.prompt_loader import load_system_prompt
from app.rag.bootstrap import load_knowledge_base
from app.rag.retriever import Retriever

load_dotenv()

class GeminiAgent:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        self.system_prompt = load_system_prompt()
        self.store = load_knowledge_base()
        self.retriever = Retriever(self.store)

        self.model = genai.GenerativeModel(model_name="gemini-2.5-flash")

    async def run(self, user_message: str) -> str:
        context = self.retriever.retrieve(user_message)

        prompt = f"""
{self.system_prompt}

КОНТЕКСТ:
{context}

ВОПРОС:
{user_message}
"""

        response = self.model.generate_content(prompt)
        return response.text


