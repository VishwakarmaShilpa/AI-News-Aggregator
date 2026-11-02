def recommend_news(articles, interests):

    recommended_articles = []

    for article in articles:

        title = article.get("title", "").lower()
        summary = article.get("summary", "").lower()

        text = title + " " + summary

        for interest in interests:

            if interest.lower() in text:
                recommended_articles.append(article)
                break

    return recommended_articles