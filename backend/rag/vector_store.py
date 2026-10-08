import os
import pickle

import faiss
import numpy as np

from .embeddings import create_embeddings


VECTOR_DIR = "vector_db"

INDEX_FILE = os.path.join(
    VECTOR_DIR,
    "index.faiss"
)

METADATA_FILE = os.path.join(
    VECTOR_DIR,
    "metadata.pkl"
)


def build_index(texts, metadatas):

    os.makedirs(
        VECTOR_DIR,
        exist_ok=True
    )

    embeddings = create_embeddings(texts)

    embeddings = np.array(
        embeddings,
        dtype="float32"
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    faiss.write_index(
        index,
        INDEX_FILE
    )

    with open(
        METADATA_FILE,
        "wb"
    ) as file:

        pickle.dump(
            {
                "texts": texts,
                "metadatas": metadatas
            },
            file
        )


def load_index():

    index = faiss.read_index(
        INDEX_FILE
    )

    with open(
        METADATA_FILE,
        "rb"
    ) as file:

        metadata = pickle.load(file)

    return index, metadata