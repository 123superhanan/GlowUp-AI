# main.py
import os
from dotenv import load_dotenv

# Load all secret environment configuration tokens at boot time
load_dotenv()

from Loader import load_documents
from chunker import chunk_documents
from vectorstore import create_vectorstore, load_vectorstore
from rag_chain import create_rag_chain

PERSIST_DIR = "./chroma_db"

# Automated Check: Build database if the folder is missing
if not os.path.exists(PERSIST_DIR):
    print(f"Directory {PERSIST_DIR} not found. Running ingestion data pipeline...")
    
    # 1. Read your raw style guide data files (make sure these paths match yours)
    raw_docs = load_documents() 
    
    # 2. Divide documents into manageable HNSW text windows
    chunks = chunk_documents(raw_docs)
    
    # 3. Process local Ollama embeddings matrix and save to disk
    vectorstore = create_vectorstore(chunks, persist_directory=PERSIST_DIR)
else:
    # If the folder exists, load it directly to bypass generation delays
    print(f"Found existing vector index. Loading from {PERSIST_DIR}...")
    vectorstore = load_vectorstore(persist_directory=PERSIST_DIR)

# Mount your unified generation completions engine
# Inside main.py (Line 33)
# This is where the unpacking assignment actually belongs!
rag_chain, rag_stream = create_rag_chain(vectorstore)


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
