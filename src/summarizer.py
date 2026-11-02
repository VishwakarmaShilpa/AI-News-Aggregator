import os
from dotenv import load_dotenv
from google import genai

# Load API key from .env file
load_dotenv()

API_KEY = (
    os.getenv("GEMINI_API_KEY")
    or os.getenv("GOOGLE_API_KEY")
)

MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)


def summarize_news(text):
    """
    Generate a short summary of a news article using Gemini.
    """

    if not text or not text.strip():
        return "No description available."

    if not API_KEY:
        return "Gemini API key is missing. Please configure your .env file."

    try:
        client = genai.Client(api_key=API_KEY)

        prompt = f"""
        Summarize the following news article in 3 to 5 simple sentences.

        Keep the important facts and main message.
        Use clear and easy-to-understand language.

        News article:
        {text}
        """

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        if response.text:
            return response.text.strip()

        return "Summary could not be generated."

    except Exception as e:
        print("Summarization error:", e)
        return "Unable to generate summary. Please try again later."