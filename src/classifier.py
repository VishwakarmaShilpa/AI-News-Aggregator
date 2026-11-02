

def classify_news(title, summary=""):

    text = f"{title} {summary}".lower()

    categories = {
        "Artificial Intelligence": [
            "artificial intelligence", " ai ", "chatgpt",
            "gemini", "openai", "llm", "generative ai"
        ],

        "Machine Learning": [
            "machine learning", "deep learning",
            "neural network", "training model",
            "supervised learning", "unsupervised learning"
        ],

        "Technology": [
            "technology", "software", "python",
            "programming", "computer", "cybersecurity"
        ],

        "Business": [
            "business", "company", "market",
            "stock", "finance", "startup"
        ],

        "Sports": [
            "cricket", "football", "tennis",
            "olympics", "sports"
        ]
    }

    for category, keywords in categories.items():

        for keyword in keywords:

            if keyword in text:
                return category

    return "General News"