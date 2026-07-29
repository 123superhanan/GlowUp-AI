from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def chunk_documents(documents: list[Document]):
    """
    1. Split by Markdown headers
    2. Further split large sections by length
    """

    # Step 1: Split by headers
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]

    markdown_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=headers_to_split_on,
        strip_headers=False
    )

    header_chunks = []
    for doc in documents:
        splits = markdown_splitter.split_text(doc.page_content)
        for split in splits:
            split.metadata.update(doc.metadata)
        header_chunks.extend(splits)

    # Step 2: Length-based splitting
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=80
    )

    final_chunks = text_splitter.split_documents(header_chunks)
    print(f"Created {len(final_chunks)} chunks")
    
    return final_chunks