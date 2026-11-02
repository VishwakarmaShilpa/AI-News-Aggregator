
import re
from html import unescape


def clean_text(text):

    if not text:
        return ""

    # Decode HTML entities
    text = unescape(text)

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Remove URLs
    text = re.sub(r"http\S+|www\.\S+", "", text)

    # Remove extra spaces and newlines
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def preprocess_article(article):

    return {
        **article,
        "title": clean_text(article.get("title", "")),
        "summary": clean_text(article.get("summary", ""))
    }


def preprocess_articles(articles):

    return [
        preprocess_article(article)
        for article in articles
    ]