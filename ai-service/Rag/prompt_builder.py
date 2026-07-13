from typing import List, Dict, Any


class PromptBuilder:
    """Combines user questions and retrieved context chunks into structured,

    grounded prompts for the LLM.
    """

    def __init__(self):
        # Define a rigid system baseline instruction to control hallucination
        self.system_instruction = (
            "You are GlowUp AI, an expert personal styling and grooming assistant.\n"
            "Answer the user's question using ONLY the provided context blocks below.\n"
            "If the answer cannot be found in the context, politely state that you "
            "do not have that information.\n"
            "Do not invent facts, and do not use any outside knowledge."
        )

    def build_prompt(self, query: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
        """Assembles context strings and the query into a clean, unified template."""
        # Cleanly stitch context contents together
        context_str = ""
        for i, chunk in enumerate(retrieved_chunks, start=1):
            context_str += f"--- Context Block {i} ---\n"
            context_str += f"{chunk['page_content'].strip()}\n\n"

        # Construct the explicit structural execution string
        prompt = (
            f"{self.system_instruction}\n\n"
            f"=== CONTEXT ===\n"
            f"{context_str}"
            f"=== USER QUESTION ===\n"
            f"{query}\n\n"
            f"=== GLOWUP AI RESPONSE ==="
        )
        return prompt


if __name__ == "__main__":
    # Integration test with your verified retriever file
    from retriever import Retriever

    # 1. Fetch live context
    retriever = Retriever()
    query = "What hairstyle parameters look best on an oval face structure?"
    matched_chunks = retriever.retrieve(query=query, top_k=2)

    # 2. Compile into a prompt package
    builder = PromptBuilder()
    final_prompt = builder.build_prompt(query, matched_chunks)

    print("\n" + "=" * 60)
    print("PROMPT BUILDER OUTPUT PREVIEW")
    print("=" * 60)
    print(final_prompt)
    print("=" * 60)
