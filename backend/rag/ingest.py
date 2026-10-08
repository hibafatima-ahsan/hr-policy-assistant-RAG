import os

from .loader import load_pdf
from .splitter import split_documents
from .vector_store import build_index


UPLOAD_DIR = "uploads"


def ingest_documents():

    all_texts = []
    all_metadata = []

    for filename in os.listdir(UPLOAD_DIR):

        if not filename.lower().endswith(".pdf"):
            continue

        file_path = os.path.join(
            UPLOAD_DIR,
            filename
        )

        print(f"Processing: {filename}")

        pages = load_pdf(file_path)

        texts, metadata = split_documents(
            pages,
            filename
        )

        all_texts.extend(texts)
        all_metadata.extend(metadata)

    if not all_texts:
        raise ValueError(
            "No PDF documents found."
        )

    build_index(
        all_texts,
        all_metadata
    )

    return len(all_texts)


if __name__ == "__main__":

    count = ingest_documents()

    print(
        f"\nSuccessfully created {count} chunks."
    )