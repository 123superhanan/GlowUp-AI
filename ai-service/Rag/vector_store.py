import os
import hashlib
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any


class VectorStore:

    def __init__(
    self,
    db_path: str = None,
    collection_name: str = "glowup_ai"
    ):
        print("=" * 60)
        print("INITIALIZING CHROMADB")
        print("=" * 60)

    # Current directory (Rag/)
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Default database location: Rag/chroma_db
        if db_path is None:
            db_path = os.path.join(current_dir, "chroma_db")

        # Create the folder if it doesn't exist
        os.makedirs(db_path, exist_ok=True)

        self.client = chromadb.PersistentClient(
        path=db_path,
        settings=Settings(anonymized_telemetry=False)
    )

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )

        print(f"Database Path : {os.path.abspath(db_path)}")
        print(f"Collection    : {collection_name}")
        print("=" * 60)

    def add_documents(
        self,
        embedded_chunks: List[Dict[str, Any]]
    ):
        if not embedded_chunks:
            print("\nNo chunks provided to store.")
            return

        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for index, chunk in enumerate(embedded_chunks):
            # Fallback to prevent missing key errors
            file_name = chunk["metadata"].get("file_name", "unknown_source")
            
            # Generate a deterministic unique ID based on file origin and array positioning
            unique_str = f"{file_name}_chunk_{index}"
            chunk_id = hashlib.md5(unique_str.encode("utf-8")).hexdigest()
            ids.append(chunk_id)

            documents.append(chunk["page_content"])
            embeddings.append(chunk["embedding"])
            metadatas.append(chunk["metadata"])

        # Add records to the local ChromaDB segment
        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

        print()
        print("=" * 60)
        print("VECTOR STORE")
        print("=" * 60)
        print(f"Stored {len(ids)} chunks successfully.")
        print("=" * 60)

    def get_collection_info(self):
        count = self.collection.count()

        print()
        print("=" * 60)
        print("DATABASE INFO")
        print("=" * 60)
        print(f"Vectors Stored : {count}")
        print("=" * 60)

        return count


if __name__ == "__main__":
    # Integration test syncing loader, chunker, embedder, and vector storage components
    from document_loader import load_md_documents
    from chunker import chunk_markdown_by_structure
    from embeddings import Embedder

    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(CURRENT_DIR, "documents")

    # 1. Pipeline: Ingest raw markdown
    docs = load_md_documents(DATA_DIR)

    if docs:
        # 2. Pipeline: Structural paragraph chunking
        chunks = chunk_markdown_by_structure(docs)

        if chunks:
            # 3. Pipeline: Generate local Hugging Face embeddings
            embedder = Embedder()
            embedded_data = embedder.generate_embeddings(chunks)

            # 4. Pipeline: Store down inside ChromaDB index blocks
            store = VectorStore()
            store.add_documents(embedded_data)
            
            # 5. Pipeline: Output database storage inventory overview
            store.get_collection_info()
