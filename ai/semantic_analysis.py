from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def semantic_similarity(a, b):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([a, b])
    score = cosine_similarity(vectors)[0][1]
    return round(score * 100, 2)