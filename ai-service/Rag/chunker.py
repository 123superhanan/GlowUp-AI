import os
import re
from typing import Dict, List, Any

def chunk_markdown_by_structure(
    documents: List[Dict[str, Any]], 
    max_chunk_size: int = 600,
    chunk_overlap: int = 50
) -> List[Dict[str, Any]]:
    """
    Chunks markdown files intelligently by respecting paragraph and structural 
    boundaries, preventing arbitrary midway splits.
    """
    chunks = []
    
    for doc in documents:
        content = doc["page_content"]
        metadata = doc["metadata"]
        file_name = metadata.get("file_name", "Unknown File")
        
        # Split documents cleanly by paragraphs or double newlines
        paragraphs = re.split(r'\n\s*\n', content)
        
        current_chunk = []
        current_length = 0
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
                
            para_len = len(para)
            
            # If a single paragraph is larger than the maximum allowed chunk size,
            # break it down forcefully using a character window fallback.
            if para_len > max_chunk_size:
                if current_chunk:
                    # Flush what we have so far
                    combined_text = "\n\n".join(current_chunk)
                    chunks.append({"page_content": combined_text, "metadata": metadata.copy()})
                    current_chunk = []
                    current_length = 0
                
                # Split large individual paragraph forcefully
                start = 0
                while start < para_len:
                    end = start + max_chunk_size
                    chunks.append({
                        "page_content": para[start:end],
                        "metadata": metadata.copy()
                    })
                    start += (max_chunk_size - chunk_overlap)
                continue

            # If adding this paragraph exceeds our budget, flush the current accumulation
            if current_length + para_len + 2 > max_chunk_size:
                combined_text = "\n\n".join(current_chunk)
                chunks.append({"page_content": combined_text, "metadata": metadata.copy()})
                
                # Hand over elements within the overlap buffer window
                overlap_text = []
                overlap_len = 0
                for item in reversed(current_chunk):
                    if overlap_len + len(item) < chunk_overlap:
                        overlap_text.insert(0, item)
                        overlap_len += len(item)
                    else:
                        break
                current_chunk = overlap_text
                current_length = overlap_len

            current_chunk.append(para)
            current_length += para_len + 2 # Accounting for newline joining characters
            
        # Append any remaining fragments left over at trailing positions
        if current_chunk:
            combined_text = "\n\n".join(current_chunk)
            chunks.append({"page_content": combined_text, "metadata": metadata.copy()})
            
    print(f"\n============================================================")
    print(f"CHUNKER (Structural)")
    print(f"============================================================")
    print(f"Documents Received : {len(documents)}")
    print(f"Total Chunks Created: {len(chunks)}")
    print(f"============================================================")
    return chunks
