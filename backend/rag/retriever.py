import numpy as np

from .embeddings import create_embeddings
from .vector_store import load_index


def retrieve_documents(
    query,
    top_k=4,
    similarity_threshold=0.35
):
    """
    Retrieve the most relevant document chunks
    from the FAISS vector database.
    """

    index, metadata = load_index()

    # Create embedding for the user's question
    query_embedding = create_embeddings([query])

    query_embedding = np.array(
        query_embedding,
        dtype="float32"
    )

    # Search more results first so we can filter
    search_k = min(top_k * 3, index.ntotal)

    scores, indices = index.search(
        query_embedding,
        search_k
    )

    results = []

    seen_chunks = set()

    for score, index_number in zip(
        scores[0],
        indices[0]
    ):

        if index_number == -1:
            continue

        score = float(score)

        # Ignore weak matches
        if score < similarity_threshold:
            continue

        text = metadata["texts"][index_number]

        # Remove duplicate chunks
        normalized_text = " ".join(
            text.lower().split()
        )

        if normalized_text in seen_chunks:
            continue

        seen_chunks.add(normalized_text)

        results.append({
            "text": text,
            "source": metadata["metadatas"][index_number],
            "score": score
        })

        # Stop when enough relevant results are collected
        if len(results) >= top_k:
            break

    return results