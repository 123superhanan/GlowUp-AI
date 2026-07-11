from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader("rag/documents").load_data()