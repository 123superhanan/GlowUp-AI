from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os


def create_vectorstore(chunks: list[Document], persist_directory: str = "./chroma_db"):
    """
    Create a Chroma vector store using Ollama llama3.2 embeddings
    """

    embeddings = OllamaEmbeddings(
        model="all-minilm"          
    )

    # Create / Load Chroma vector store
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )

    print(f"Vector store created with {len(chunks)} chunks")
    print(f"Saved at: {persist_directory}")

    return vectorstore


def load_vectorstore(persist_directory: str = "./chroma_db"):
    """
    Load existing Chroma vector store
    """
    embeddings = OllamaEmbeddings(model="llama3.2")

    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )

    return vectorstore