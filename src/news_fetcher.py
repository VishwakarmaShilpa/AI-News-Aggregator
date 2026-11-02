
import feedparser
import re
from html import unescape

def clean_html(raw_html):
    if not raw_html:
        return ""

    clean_text = unescape(raw_html)
    clean_text = re.sub(r"<[^>]+>", " ", clean_text)
    clean_text = re.sub(r"\s+", " ", clean_text)

    return clean_text.strip()

# 1. RSS news sources
RSS_FEEDS = {
    "BBC Technology":
        "https://feeds.bbci.co.uk/news/technology/rss.xml",

    "CNN World":
        "http://rss.cnn.com/rss/edition_world.rss",

    "AI News":
        "https://news.google.com/rss/search?q=artificial+intelligence&hl=en-IN&gl=IN&ceid=IN:en",

    "Machine Learning":
        "https://news.google.com/rss/search?q=machine+learning&hl=en-IN&gl=IN&ceid=IN:en"
}


# 2. Function to fetch news
def fetch_news():

    articles = []

    # Loop through every RSS source
    for category, feed_url in RSS_FEEDS.items():

        try:

            print(f"Fetching: {category}")

            # Read RSS feed
            feed = feedparser.parse(feed_url)

            # Extract articles
            for entry in feed.entries:

                article = {
                    "title": entry.get("title", "").strip(),
                    "link": entry.get("link", ""),
                    "summary": clean_html(entry.get("summary", "")),
                    "published": entry.get("published", "Unknown"),
                    "source": category
                }

                articles.append(article)

        except Exception as e:

            print(f"Error fetching {category}: {e}")

    return articles


# 3. Run this file directly for testing
if __name__ == "__main__":

    news = fetch_news()

    print("\nTotal articles fetched:", len(news))

    for article in news[:10]:

        print("\nTitle:", article["title"])

        print("Source:", article["source"])

        print("Link:", article["link"])
