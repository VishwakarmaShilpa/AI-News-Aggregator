
import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = (
    os.getenv("GEMINI_API_KEY")
    or os.getenv("GOOGLE_API_KEY")
)

MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)


def ask_news_chatbot(question, articles):

    if not API_KEY:
        return "Gemini API key is missing. Check your .env file."

    if not question or not question.strip():
        return "Please enter a question."

    if not articles:
        return "No news articles are available."

    news_context = ""

    for article in articles[:10]:
        news_context += (
            f"Title: {article.get('title', '')}\n"
            f"Summary: {article.get('summary', '')[:800]}\n\n"
        )

    prompt = f"""
You are an AI news assistant.

Answer the user's question using the news articles below.
If the answer is not available, say so clearly.
Use simple and understandable language.

NEWS ARTICLES:
{news_context}

USER QUESTION:
{question}
"""

    for attempt in range(3):
        try:
            client = genai.Client(api_key=API_KEY)

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

            if response.text:
                return response.text.strip()

            return "Gemini returned an empty response."

        except Exception as e:
            print(f"Chatbot attempt {attempt + 1} failed: {e}")

            if attempt < 2:
                time.sleep(2 * (attempt + 1))

    return (
        "Gemini could not connect after 3 attempts. "
        "Please check your internet connection and try again."
    )