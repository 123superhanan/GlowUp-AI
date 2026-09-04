import os
import time
import logging

from langchain_chroma import Chroma
from langchain_core.documents import Document

from langchain_ollama import OllamaEmbeddings


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("GlowUP-VectorStore")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")


def get_local_embeddings():
    return OllamaEmbeddings(model="all-minilm")


def create_vectorstore(
    chunks: list[Document],
    persist_directory: str = CHROMA_DIR,
    collection_name: str = "glowup_style_guides"
):
    os.makedirs(persist_directory, exist_ok=True)

    embeddings = get_local_embeddings()

    collection_metadata = {
        "hnsw:space": "cosine",
        "hnsw:construction_ef": 200,
        "hnsw:M": 16,
        "hnsw:search_ef": 100,
    }

    start = time.time()

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name=collection_name,
        collection_metadata=collection_metadata,
    )

    elapsed = time.time() - start
    count = vectorstore._collection.count()

    logger.info("Vector store created")
    logger.info(f"Chunks added: {len(chunks)}")
    logger.info(f"Total documents: {count}")
    logger.info(f"Collection: {collection_name}")
    logger.info(f"Persist path: {persist_directory}")
    logger.info(f"Time taken: {elapsed:.2f}s")

    return vectorstore


def load_vectorstore(
    persist_directory: str = CHROMA_DIR,
    collection_name: str = "glowup_style_guides"
):
    if not os.path.exists(persist_directory):
        raise FileNotFoundError(
            f"No vector store found at: {persist_directory}"
        )

    embeddings = get_local_embeddings()

    start = time.time()

    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
        collection_name=collection_name,
    )

    elapsed = time.time() - start
    count = vectorstore._collection.count()

    logger.info("Vector store loaded")
    logger.info(f"Documents: {count}")
    logger.info(f"Collection: {collection_name}")
    logger.info(f"Load time: {elapsed:.2f}s")

    return vectorstore