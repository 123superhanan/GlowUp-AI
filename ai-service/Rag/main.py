from Loader import load_documents

from chunker import chunk_documents
from vectorstore import create_vectorstore, load_vectorstore
from rag_chain import create_rag_chain

# Load existing vector store (or create new one)
vectorstore = load_vectorstore()
# vectorstore = create_vectorstore(chunks)   # only first time

rag_chain = create_rag_chain(vectorstore)

while True:
    question = input("\nAsk a question (or type 'exit'): ")
    
    if question.lower() in ["exit", "quit"]:
        break

    result = rag_chain(question)

    print("\nAnswer:")
    print(result["answer"])
    
    print("\nSources:")
    for src in result["sources"]:
        print(f"  - {src}")