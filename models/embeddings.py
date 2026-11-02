from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the embedding model
MODEL_NAME = "all-MiniLM-L6-v2"

model = None


def load_embedding_model():
    global model

    if model is None:
        model = SentenceTransformer(MODEL_NAME)

    return model


def generate_embeddings(texts):
    if not texts:
        return []

    embedding_model = load_embedding_model()

    embeddings = embedding_model.encode(
        texts,
        convert_to_numpy=True
    )

    return embeddings


def semantic_search(query, articles, top_k=5):

    if not query.strip() or not articles:
        return []

    article_texts = [
        article.get("title", "") + " " +
        article.get("summary", "")
        for article in articles
    ]

    embeddings = generate_embeddings(article_texts)
    query_embedding = generate_embeddings([query])

    scores = cosine_similarity(
        query_embedding,
        embeddings
    )[0]

    ranked_indices = scores.argsort()[::-1][:top_k]

    results = []

    for index in ranked_indices:
        result = articles[index].copy()
        result["similarity_score"] = float(scores[index])
        results.append(result)

    return results