from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents, filename):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100
    )

    texts = []
    metadatas = []

    for document in documents:

        chunks = splitter.split_text(
            document["text"]
        )

        for chunk in chunks:

            texts.append(chunk)

            metadatas.append({
                "source": filename,
                "page": document["page"]
            })

    return texts, metadatas