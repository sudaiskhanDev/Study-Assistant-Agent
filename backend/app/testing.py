
from services.rag_service import answer_question


question = "What is the difference between parametric and non-parametric algorithms?"

result = answer_question(question)

print("\nQuestion:")
print(question)

print("\nAnswer:")
print(result["answer"])

print("\nSource pages:")
print(result["source_pages"])

print("\nRetrieved sources:")
for source in result["sources"]:
    print(f"Page {source['page_number']}:")
    print(source["text"][:200])
    print("-" * 40)
