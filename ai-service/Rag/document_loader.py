import os
from glob import glob
from typing import List, Dict, Any


def load_md_documents(data_dir: str) -> List[Dict[str, Any]]:
    """
    Load all Markdown (.md) files from the documents folder.

    Returns:
        List of dictionaries containing:
        - page_content
        - metadata
    """

    documents = []

    search_path = os.path.join(data_dir, "**", "*.md")
    md_files = glob(search_path, recursive=True)

    print("=" * 60)
    print("DOCUMENT LOADER")
    print("=" * 60)

    print(f"Searching in : {os.path.abspath(data_dir)}")
    print(f"Markdown files found : {len(md_files)}")

    for file_path in md_files:

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read().strip()

            if not content:
                print(f"Skipping empty file : {os.path.basename(file_path)}")
                continue

            document = {
                "page_content": content,
                "metadata": {
                    "source": os.path.abspath(file_path),
                    "file_name": os.path.basename(file_path),
                },
            }

            documents.append(document)

            print(f"Loaded : {os.path.basename(file_path)} ({len(content)} characters)")

        except Exception as error:
            print(f"Error reading {file_path}")
            print(error)

    print("-" * 60)
    print(f"Successfully loaded {len(documents)} documents.")

    return documents


if __name__ == "__main__":

    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

    DOCUMENTS_DIR = os.path.join(CURRENT_DIR, "documents")

    loaded_documents = load_md_documents(DOCUMENTS_DIR)

    print("\nPreview\n")

    for index, document in enumerate(loaded_documents, start=1):

        print(f"Document {index}")

        print("File :", document["metadata"]["file_name"])

        print("Characters :", len(document["page_content"]))

        print(document["page_content"][:200])

        print("-" * 60)