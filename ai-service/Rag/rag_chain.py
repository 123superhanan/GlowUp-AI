import os
from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
def format_docs_with_sources(docs):
    content = "\n\n".join(doc.page_content for doc in docs)

    sources = set()
    for doc in docs:
        source = doc.metadata.get("source", "Unknown")
        filename = source.replace("\\", "/").split("/")[-1]
        sources.add(filename)

    return content, list(sources)


# Updated to use Google's latest recommended high-performance engine
def create_rag_chain(vectorstore, model_name: str = "gemini-3.6-flash", gemini_api_key: str = None):

    # Self-healing fallback: If no key is passed directly, pull it automatically from environment
    resolved_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

    if not resolved_api_key:
        raise ValueError(
            "API key required for Gemini Developer API. Provide gemini_api_key parameter "
            "or set GEMINI_API_KEY / GOOGLE_API_KEY environment variables."
        )

    # Correct parameter argument for modern ChatGoogleGenerativeAI is 'api_key'
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        temperature=0.3,
        api_key=resolved_api_key   
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 2}
    )

    prompt = ChatPromptTemplate.from_template("""
You are GlowUP AI, a professional men's style and grooming assistant.

The user message may include a KNOWN USER PROFILE (face shape, skin tone, body type, preferences).
That profile is ground truth.

- CRITICAL: Check the Scalp/Baldness status first. If the status is "Bald", ignore the "Hair type" trait completely, do NOT recommend hairstyles or hair care products for the head, and focus entirely on facial hair, beard grooming, and scalp maintenance instead.

Rules:
- If the user asks what their detected hair type, bald status, face shape, or traits are, ANSWER DIRECTLY by stating exactly what is written in the user profile below. Do NOT make up recommendations or write a style guide if they just want to know their current classification.
- Do NOT say you lack information if those values are present in the user message.
- For style recommendations, use both the profile and the retrieved context.
- Be direct, practical, and specific.
- Do not mention weight, fitness, or medical topics.
- Do not give makeup advice.
- Do not ask questions back.
- When giving style advice, structure as:
  1. Hairstyle
  2. facial hair
  3. Clothing
  4. Quick tips
  5. Recommended products (if applicable)
  6. Recommended grooming tools (if applicable)
  7. Recommended hair care products (if applicable)
  8. Ask some interesting questions to engage the user in a conversation about their style and grooming preferences.

Retrieved style-guide context:
{context}

User message:
{question}

Answer:
""")

    def rag_with_sources(question: str):
        docs = retriever.invoke(question)
        context, sources = format_docs_with_sources(docs)

        chain = prompt | llm | StrOutputParser()
        answer = chain.invoke({
            "context": context,
            "question": question
        })

        return {
            "answer": answer,
            "sources": sources
        }

    def rag_stream(question: str):
        """
        Yields text chunks for streaming.
        Final yield is a special sources marker.
        """
        docs = retriever.invoke(question)
        context, sources = format_docs_with_sources(docs)

        chain = prompt | llm | StrOutputParser()

        for chunk in chain.stream({
            "context": context,
            "question": question
        }):
            yield chunk

        # Send sources at the end
               # Send sources at the end
        yield {
            "type": "sources",
            "sources": sources
        }

    # This should be the absolute end of create_rag_chain function
    return rag_with_sources, rag_stream
