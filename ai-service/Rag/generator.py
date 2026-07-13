import ollama
from typing import Dict, Any


class Generator:
    """Handles communication with the local Ollama instance to generate responses

    grounded in context prompts.
    """

    # Updated default to match your active local model tag
    def __init__(self, model_name: str = "llama3.2:3b"):
        print("=" * 60)
        print("INITIALIZING GENERATOR")
        print("=" * 60)
        
        self.model_name = model_name
        print(f"Targeting local model : {self.model_name}")
        print("=" * 60)

    def generate_response(self, prompt: str) -> str:
        """Sends the constructed context prompt to Ollama and returns the clean text output."""
        print(f"\nSending payload to local Ollama runtime engine ({self.model_name})...")
        
        try:
            # Execute synchronous completion against local API node
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    "temperature": 0.0  # Force lowest creativity to anchor model to the context
                }
            )
            return response.get("response", "").strip()
            
        except Exception as e:
            error_msg = f"Failed to communicate with local Ollama engine: {str(e)}"
            print(f"[Error]: {error_msg}")
            return f"Error: {error_msg}. Please check if Ollama is running (`ollama serve`)."


if __name__ == "__main__":
    # Full Integration Test: Loader -> Chunker -> Retriever -> PromptBuilder -> Generator
    from retriever import Retriever
    from prompt_builder import PromptBuilder

    # 1. Fetch relevant vector elements from index mapping database
    query = "What hairstyle parameters look best on an oval face structure?"
    retriever = Retriever()
    matched_chunks = retriever.retrieve(query=query, top_k=2)

    # 2. Compile elements into the structured execution prompt
    builder = PromptBuilder()
    compiled_prompt = builder.build_prompt(query, matched_chunks)

    # 3. Request inference response from your local LLM node
    # Updated instantiation string to align with your active local image registry
    generator = Generator(model_name="llama3.2:3b")
    ai_response = generator.generate_response(compiled_prompt)

    print("\n" + "=" * 60)
    print("OLLAMA AI INFERENCE RESPONSE")
    print("=" * 60)
    print(ai_response)
    print("=" * 60 + "\n")
