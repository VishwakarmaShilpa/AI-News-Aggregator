
import streamlit as st
import pandas as pd

from src.news_fetcher import fetch_news
from src.database import (
    init_db,
    save_articles,
    get_articles,
    get_article_count
)
from src.summarizer import summarize_news
from src.classifier import classify_news
from src.deduplication import remove_duplicates
from src.recommender import recommend_news
from src.chatbot import ask_news_chatbot
from src.trending import get_trending_topics
from src.preprocessing import preprocess_articles
from models.embeddings import semantic_search


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI News Aggregator",
    page_icon="📰",
    layout="wide"
)

st.title("📰 AI News Aggregator")
st.caption("Your personalized AI-powered news platform")


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("⚙️ News Settings")

if st.sidebar.button("🔄 Refresh News"):
    st.cache_data.clear()
    st.rerun()


# --------------------------------------------------
# LOAD NEWS
# --------------------------------------------------

@st.cache_data(ttl=300)
def load_news():

    init_db()

    fresh_articles = fetch_news()

    saved_count = save_articles(fresh_articles)

    print(f"New articles saved: {saved_count}")

    stored_articles = get_articles(limit=100)

    unique_articles = remove_duplicates(stored_articles)

    clean_articles = preprocess_articles(unique_articles)

    print("Articles after duplicate removal:", len(unique_articles))
    print("Articles after preprocessing:", len(clean_articles))

    return clean_articles


with st.spinner("Fetching latest news..."):
    articles = load_news()


# --------------------------------------------------
# MAIN DASHBOARD
# --------------------------------------------------

if not articles:

    st.error("Unable to fetch news articles.")

else:

    df = pd.DataFrame(articles)

    # Dashboard metrics
    total_articles = get_article_count()

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Articles Displayed", len(df))

    with col2:
        st.metric("Total Articles Stored", total_articles)

    st.divider()

    # --------------------------------------------------
    # NEWS SOURCE FILTER
    # --------------------------------------------------

    st.sidebar.subheader("📰 Filter News")

    sources = ["All Sources"] + sorted(
        df["source"].dropna().unique().tolist()
    )

    selected_source = st.sidebar.selectbox(
        "Filter by News Source",
        sources
    )

    filtered_df = df.copy()

    if selected_source != "All Sources":
        filtered_df = filtered_df[
            filtered_df["source"] == selected_source
        ]

    # --------------------------------------------------
    # AI CATEGORY FILTER
    # --------------------------------------------------

    available_categories = [
        "All Categories",
        "Artificial Intelligence",
        "Machine Learning",
        "Technology",
        "Business",
        "Sports",
        "General News"
    ]

    selected_ai_category = st.sidebar.selectbox(
        "Filter by AI Category",
        available_categories
    )

    if selected_ai_category != "All Categories":

        filtered_df = filtered_df[
            filtered_df.apply(
                lambda row: classify_news(
                    row["title"],
                    row["summary"]
                ) == selected_ai_category,
                axis=1
            )
        ]

    # --------------------------------------------------
    # PERSONALIZED RECOMMENDATIONS
    # --------------------------------------------------

    st.sidebar.subheader("⭐ News Recommendations")

    available_interests = [
        "Python",
        "AI",
        "Machine Learning",
        "ChatGPT",
        "Technology",
        "Business",
        "Sports"
    ]

    selected_interests = st.sidebar.multiselect(
        "Choose your interests",
        available_interests
    )

    if selected_interests:

        recommended_articles = recommend_news(
            articles,
            selected_interests
        )

        st.subheader("⭐ Recommended For You")

        if recommended_articles:

            for article in recommended_articles:
                st.write(f"• {article['title']}")

        else:
            st.info("No recommendations found.")

    # --------------------------------------------------
    # KEYWORD SEARCH
    # --------------------------------------------------

    search = st.text_input(
        "🔎 Search News",
        placeholder="Search AI, technology, business..."
    )

    if search:

        filtered_df = filtered_df[
            filtered_df["title"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    # --------------------------------------------------
    # NEWS SORTING
    # --------------------------------------------------

    sort_option = st.selectbox(
        "Sort News By",
        ["Newest First", "Oldest First"]
    )

    if "published" in filtered_df.columns:

        filtered_df = filtered_df.copy()

        filtered_df["published"] = pd.to_datetime(
            filtered_df["published"],
            errors="coerce",
            utc=True
        )

        filtered_df = filtered_df.sort_values(
            by="published",
            ascending=(sort_option == "Oldest First"),
            na_position="last"
        )

    # --------------------------------------------------
    # SEMANTIC SEARCH
    # --------------------------------------------------

    st.divider()

    st.header("🔍 AI Semantic Search")

    semantic_query = st.text_input(
        "Describe the news you want to find:",
        placeholder="Example: How is AI helping doctors?"
    )

    if st.button("Search with AI"):

        if semantic_query.strip():

            with st.spinner("Understanding your search..."):

                search_results = semantic_search(
                    semantic_query,
                    articles,
                    top_k=5
                )

            st.subheader("Semantic Search Results")

            if search_results:

                for result in search_results:

                    st.markdown(f"### {result['title']}")

                    st.write(
                        result.get("summary", "")
                    )

                    st.caption(
                        f"Relevance score: "
                        f"{result['similarity_score']:.2f}"
                    )

                    if result.get("link"):
                        st.link_button(
                            "Read Full Article",
                            result["link"]
                        )

            else:
                st.info("No relevant articles found.")

        else:
            st.warning("Please enter a search query.")

    # --------------------------------------------------
    # LATEST NEWS
    # --------------------------------------------------

    st.divider()

    st.header("📰 Latest News")

    st.write(
        f"Showing {len(filtered_df)} news articles"
    )

    if filtered_df.empty:

        st.info("No articles match your filters.")

    else:

        for _, article in filtered_df.iterrows():

            with st.container(border=True):

                st.markdown(f"### {article['title']}")

                st.caption(
                    f"Source: {article['source']} | "
                    f"Published: {article['published']}"
                )

                category = classify_news(
                    article["title"],
                    article["summary"]
                )

                st.caption(f"AI Category: {category}")

                st.write(
                    article["summary"] or
                    "No description available."
                )

                if st.button(
                    "✨ Generate AI Summary",
                    key=f"summary_{article['id']}"
                ):

                    with st.spinner(
                        "Gemini is generating your summary..."
                    ):

                        ai_summary = summarize_news(
                            article["summary"]
                        )

                    st.subheader("AI-Generated Summary")
                    st.success(ai_summary)

                if article.get("link"):

                    st.link_button(
                        "Read Full Article",
                        article["link"]
                    )

    # --------------------------------------------------
    # TRENDING TOPICS
    # --------------------------------------------------

    st.divider()

    st.header("🔥 Trending News Topics")

    trending_topics = get_trending_topics(
        articles,
        top_n=10
    )

    if trending_topics:

        for topic, count in trending_topics:
            st.write(f"🔥 **{topic}** — {count} mentions")

    else:
        st.info("No trending topics found.")

    # --------------------------------------------------
    # AI NEWS CHATBOT
    # --------------------------------------------------

    st.divider()

    st.header("🤖 AI News Chatbot")

    st.write(
        "Ask questions about the latest news articles."
    )

    user_question = st.text_input(
        "Enter your question:",
        placeholder="Example: What are the latest AI developments?"
    )

    if st.button("Ask AI"):

        if user_question.strip():

            with st.spinner("AI is thinking..."):

                answer = ask_news_chatbot(
                    user_question,
                    articles
                )

            st.subheader("Chatbot Answer")
            st.write(answer)

        else:
            st.warning("Please enter a question.")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "AI News Aggregator | Powered by Python, Streamlit, "
    "SQLite, Gemini AI and Sentence Transformers"
)
