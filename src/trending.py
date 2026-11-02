from collections import Counter
import re


def get_trending_topics(articles, top_n=10):

    keywords = [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "chatgpt",
        "openai",
        "google",
        "gemini",
        "microsoft",
        "python",
        "cybersecurity",
        "robotics",
        "cloud computing",
        "technology",
        "startup",
        "semiconductor",
        "data science"
    ]

    text = ""

    for article in articles:
        text += (
            article.get("title", "") + " " +
            article.get("summary", "") + " "
        )

    text = re.sub(r"\s+", " ", text.lower())

    topic_counts = Counter()

    for keyword in keywords:
        count = len(re.findall(
            r"\b" + re.escape(keyword) + r"\b",
            text
        ))

        if count > 0:
            topic_counts[keyword.title()] = count

    return topic_counts.most_common(top_n)