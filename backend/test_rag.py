from rag.retriever import retrieve_documents
from rag.generator import generate_answer


question = "What is the maternity leave policy?"
results = retrieve_documents(
    question,
    top_k=2
)

answer = generate_answer(
    question, 
    results
)


print("\n" + "=" * 60)
print("HR POLICY ASSISTANT")
print("=" * 60)

print("\nQuestion:")
print(question)

print("\nAnswer:")
print(answer)

print("\nSources:")

for result in results:
    print(
        f"- {result['source']['source']} "
        f"(Page {result['source']['page']}) "
        f"Score: {result['score']:.4f}"
    )