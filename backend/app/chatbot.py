from openai import OpenAI
from .config import settings


client = OpenAI(
    api_key=settings.OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)


SYSTEM_PROMPT = """
You are the AI customer assistant for Cafe De Flora,
a cafe in Chanakyapuri, New Delhi.

Your job is to help customers with questions about the business.

Rules:
- Be polite and concise.
- Do not invent information.
- If you don't know something, say that you don't have that information.
- Do not claim to be the official Cafe De Flora representative.
- You are currently an independent demo chatbot.

Known information:

Business:
Cafe De Flora

Location:
Santushti Shopping Complex, Chanakyapuri, New Delhi.

More business information will be added through the knowledge base later.
"""


def generate_response(message: str) -> str:

    response = client.chat.completions.create(
        model=settings.OPENROUTER_MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )

    return response.choices[0].message.content
