from .config import settings


BUSINESS_CONTEXT = """
You are the AI customer assistant for Cafe De Flora in Chanakyapuri, New Delhi.

Your job is to help customers with questions about the cafe.

Important rules:
1. Answer only using information provided in the business context.
2. Never invent menu items, prices, timings, availability, or policies.
3. If you do not know something, clearly say that you don't have that information.
4. Be polite, concise, and helpful.
5. You are an independent demo chatbot and must not claim to be the official Cafe De Flora representative.

Current business information:

Business: Cafe De Flora
Location: Santushti Shopping Complex, Chanakyapuri, New Delhi.

The detailed menu, prices, timings, facilities and FAQs will be added to the knowledge base later.
"""


def generate_response(message: str) -> str:
    """
    Temporary chatbot response.
    We will connect an AI model here in the next step.
    """

    message_lower = message.lower()

    if "location" in message_lower or "where" in message_lower:
        return (
            "Cafe De Flora is located at Santushti Shopping Complex "
            "in Chanakyapuri, New Delhi."
        )

    if "hello" in message_lower or "hi" in message_lower:
        return (
            "Hello! 👋 I'm the Cafe De Flora AI Assistant. "
            "How can I help you?"
        )

    return (
        "I'm currently being set up. I can help with Cafe De Flora's "
        "menu, timings, location and other customer questions once my "
        "knowledge base is connected."
    )
