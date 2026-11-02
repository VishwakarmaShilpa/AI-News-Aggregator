def remove_duplicates(articles):

    unique_articles = []
    seen_links = set()
    seen_titles = set()

    for article in articles:

        link = article.get("link", "").strip()
        title = article.get("title", "").strip().lower()

        # Skip articles with duplicate links or titles
        if link in seen_links or title in seen_titles:
            continue

        seen_links.add(link)
        seen_titles.add(title)

        unique_articles.append(article)

    return unique_articles