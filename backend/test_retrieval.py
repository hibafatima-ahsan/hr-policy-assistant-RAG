from rag.retriever import retrieve_documents


query = "How many annual leave days do employees get?"

results = retrieve_documents(
    query,
    top_k=2
)

print("\n" + "=" * 60)
print("RETRIEVAL RESULTS")
print("=" * 60)

for i, result in enumerate(results, start=1):

    print(f"\nResult {i}")
    print("-" * 60)

    print("Source:", result["source"]["source"])
    print("Page:", result["source"]["page"])
    print("Score:", result["score"])

    print("\nContent:")
    print(result["text"])