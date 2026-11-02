from datetime import datetime


def format_date(date_string):
    """Format a published date for display."""
    if not date_string:
        return "Date unavailable"

    try:
        date = datetime.fromisoformat(
            date_string.replace("Z", "+00:00")
        )
        return date.strftime("%d %B %Y, %I:%M %p")
    except (ValueError, TypeError):
        return date_string


def truncate_text(text, max_length=200):
    """Shorten long text for dashboard display."""
    if not text:
        return ""

    if len(text) <= max_length:
        return text

    return text[:max_length].rsplit(" ", 1)[0] + "..."


def get_article_domain(url):
    """Extract the website domain from an article URL."""
    from urllib.parse import urlparse

    if not url:
        return "Unknown source"

    return urlparse(url).netloc.replace("www.", "")