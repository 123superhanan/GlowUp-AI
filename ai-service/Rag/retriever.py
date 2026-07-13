import os
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
from embeddings import Embedder

# Get the folder where retriever.py actually lives to secure absolute local path lookup
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB_PATH = os.path.normpath(os.path.join(CURRENT_DIR, "chroma_db"))


class Retriever:

    def __init__(
        self,
        db_path: str = DEFAULT_DB_PATH,
        collection_name: str = "glowup_ai",
        model_name: str = "BAAI/bge-small-en-v1.5",
    ):
        print("=" * 60)
        print("INITIALIZING RETRIEVER")
        print("=" * 60)

        # 1. Initialize local embedding transformer engine
        self.embedder = Embedder(model_name=model_name)

        # 2. Connect to the validated persistent storage path block
        print(f"Connecting to DB Path : {db_path}")
        self.client = chromadb.PersistentClient(
            path=db_path, settings=Settings(anonymized_telemetry=False)
        )

        # Use get_collection here since your indexing layer already built it
        self.collection = self.client.get_collection(name=collection_name)

        print(f"Active Collection     : {collection_name}")
        print("=" * 60)

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        print(f"\nUser Query : '{query}'")
        print(f"Retrieving Top {top_k} matching context chunks...")

        # 1. Map query parameters to embedding vector matrix coordinates
        query_vector = self.embedder.model.encode(query, convert_to_numpy=True)

        # 2. Search index graph layout
        results = self.collection.query(
            query_embeddings=[query_vector.tolist()],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )

        retrieved_chunks = []

        # 3. Defensive isolation extraction loop matching query block 0
        if not results or not results["documents"] or not results["documents"][0]:
            print("\n[Warning]: No matching contextual records located in store indices.")
            return []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        print("\n" + "-" * 60)
        print("RETRIEVED CHUNKS VERIFICATION")
        print("-" * 60)

        for i in range(len(documents)):
            distance = distances[i]

            chunk_data = {
                "page_content": documents[i],
                "metadata": metadatas[i],
                "distance": round(float(distance), 4),
            }
            retrieved_chunks.append(chunk_data)

            file_origin = metadatas[i].get("file_name", "unknown_source")
            print(f"Result {i+1} | Source: {file_origin} | Distance Score: {distance:.4f}")
            print(f"Content:\n{documents[i]}")
            print("-" * 60)

        return retrieved_chunks


if __name__ == "__main__":
    # Initialize execution search query
    retriever = Retriever()

    # Highly relevant test parameter matching indexing baseline definitions
    test_query = "What hairstyle parameters look best on an oval face structure?"

    matched_chunks = retriever.retrieve(query=test_query, top_k=2)

    print(f"\nExecution Pipeline Complete: Returned {len(matched_chunks)} chunks.")
