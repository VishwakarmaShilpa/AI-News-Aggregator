# AI News Aggregator

An AI-powered news aggregation platform built using Python, Streamlit, SQLite, and Google's Gemini API.

## Features

- Fetches news from multiple RSS feeds.
- Stores news articles in an SQLite database.
- Generates AI-powered news summaries using Gemini.
- Automatically categorizes news articles.
- Removes duplicate articles.
- Provides personalized news recommendations.
- Supports semantic search using Sentence Transformers.
- Includes an AI-powered news chatbot.
- Displays trending topics from collected news.

## Technologies Used

- Python
- Streamlit
- SQLite
- Google Gemini API
- Sentence Transformers
- Pandas
- RSS / Feedparser
- Scikit-learn

## How to Run

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:

   `pip install -r requirements.txt`

4. Create a `.env` file and add your Gemini API key:

   `GEMINI_API_KEY=your_api_key_here`

5. Run the application:

   `streamlit run app.py`

## Project Structure

- `app.py` — Streamlit dashboard
- `src/` — News fetching, database, chatbot, summarization and other modules
- `models/` — Semantic search and embedding model
- `utils/` — Helper functions
- `data/` — Local database (not committed to GitHub)

## Author
Shilpa vishwakarma
Computer Science and Engineering Student

## Note

This project is developed for learning and demonstrating practical applications of AI, machine learning, and natural language processing.