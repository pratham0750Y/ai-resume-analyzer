from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def match_roles(found_skills, roles_df):
    """Give every job role a match score (0-100) using TF-IDF + cosine similarity."""
    # Turn skills into one 'document' per role. '_' keeps multi-word skills together.
    role_docs = [r.replace(" ", "_").replace("|", " ") for r in roles_df["required_skills"]]
    resume_doc = " ".join(s.replace(" ", "_") for s in found_skills)

    # TF-IDF turns each document into a vector of numbers
    vectorizer = TfidfVectorizer(token_pattern=r"\S+")
    vectors = vectorizer.fit_transform(role_docs + [resume_doc])

    # Cosine similarity: compare the resume vector (last one) with every role vector
    scores = cosine_similarity(vectors[-1], vectors[:-1]).ravel() * 100

    result = roles_df[["role"]].copy()
    result["match_score"] = scores.round(0).astype(int)
    return result.sort_values("match_score", ascending=False).reset_index(drop=True)
