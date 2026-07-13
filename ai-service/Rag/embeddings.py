from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any


class Embedder:
    """
    Converts text chunks into vector embeddings.
    """

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):

        print("=" * 60)
        print("LOADING EMBEDDING MODEL")
        print("=" * 60)

        self.model = SentenceTransformer(model_name)

        print(f"Model Loaded : {model_name}")
        print("=" * 60)

    def generate_embeddings(
        self,
        chunks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:

        embedded_chunks = []

        print("\nGenerating Embeddings...\n")

        for index, chunk in enumerate(chunks, start=1):

            text = chunk["page_content"]

            embedding = self.model.encode(
                text,
                convert_to_numpy=True
            )

            embedded_chunks.append({

                "page_content": text,

                "metadata": chunk["metadata"],

                "embedding": embedding.tolist()

            })

            print(
                f"[{index}/{len(chunks)}] "
                f"{chunk['metadata']['file_name']} "
                f"-> Vector Length: {len(embedding)}"
            )

        print("\nEmbeddings Generated Successfully.")

        return embedded_chunks
    
if __name__ == "__main__":

    from document_loader import load_md_documents
    from chunker import chunk_markdown_by_structure
    import os

    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

    docs = load_md_documents(
        os.path.join(CURRENT_DIR, "documents")
    )

    chunks = chunk_markdown_by_structure(docs)

    embedder = Embedder()

    embeddings = embedder.generate_embeddings(chunks)

    print("\nExample\n")

    print(embeddings[0]["metadata"])

    print()

    print(embeddings[0]["page_content"][:200])

    print()

    print("Vector Length :", len(embeddings[0]["embedding"]))

    print()

    print("First 10 Values")

    print(embeddings[0]["embedding"][:10])