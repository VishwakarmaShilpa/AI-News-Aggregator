
import sqlite3
from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database location
DB_PATH = BASE_DIR / "data" / "news.db"


# 1. Create database and table
def init_db():

    # Ensure data folder exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT NOT NULL,

            link TEXT UNIQUE NOT NULL,

            summary TEXT,

            published TEXT,

            source TEXT,

            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    conn.commit()
    conn.close()

    print("Database initialized successfully!")


# 2. Save articles into database
def save_articles(articles):

    init_db()

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    saved_count = 0

    for article in articles:

        link = article.get("link", "").strip()

        # Skip articles without a URL
        if not link:
            continue

        cursor.execute("""
            INSERT INTO articles
            (title, link, summary, published, source)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(link) DO UPDATE SET
                title = excluded.title,
                summary = excluded.summary,
                published = excluded.published,
                source = excluded.source
        """, (

            article.get("title", "No title"),

            link,

            article.get("summary", ""),

            article.get("published", "Unknown"),

            article.get("source", "Unknown")

        ))

        saved_count += cursor.rowcount

    conn.commit()
    conn.close()

    return saved_count


# 3. Retrieve articles from database
def get_articles(limit=100):

    init_db()

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM articles
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    articles = [dict(row) for row in rows]

    conn.close()

    return articles


# 4. Get total article count
def get_article_count():

    init_db()

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM articles")

    count = cursor.fetchone()[0]

    conn.close()

    return count


# 5. Test database directly
if __name__ == "__main__":

    init_db()

    print("Total stored articles:", get_article_count())
