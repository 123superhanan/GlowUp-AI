import os
# Change these from absolute imports to relative imports (add a dot .)
from .retriever import Retriever
from .prompt_builder import PromptBuilder
from .generator import Generator



class RecommendationService:
    """Service layer that orchestrates retrieval, prompt construction, and

    generation into a single unified call for downstream applications.
    """

    # 1. FIXED: Updated default model target to match your active system tag
    def __init__(self, model_name: str = "llama3.2:3b"):
        # Access local absolute path contexts safely
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(current_dir, "chroma_db")

        # Initialize internal components cleanly
        self.retriever = Retriever(db_path=db_path)
        self.prompt_builder = PromptBuilder()
        self.generator = Generator(model_name=model_name)

    def ask(self, question: str, top_k: int = 2) -> str:
        """Processes a raw question string through the complete inference execution loop

        and returns the final text response.
        """
        # 1. Fetch relevant vector fragments from our custom knowledge store
        matched_chunks = self.retriever.retrieve(query=question, top_k=top_k)

        if not matched_chunks:
            return "Error: No matching contextual metrics located inside your vector database."

        # 2. Build our isolated, grounded execution prompt frame
        compiled_prompt = self.prompt_builder.build_prompt(
            query=question, retrieved_chunks=matched_chunks
        )

        # 3. Stream through our local model to perform inference
        response = self.generator.generate_response(compiled_prompt)

        return response


if __name__ == "__main__":
    # 2. FIXED: Changed the execution call to target llama3.2:3b explicitly
    service = RecommendationService(model_name="llama3.2:3b")

    test_query = "What hairstyle parameters look best on an oval face structure?"
    final_answer = service.ask(test_query)

    print("\n" + "=" * 60)
    print("RECOMMENDATION SERVICE FINAL ANSWER")
    print("=" * 60)
    print(final_answer)
    print("=" * 60 + "\n")
