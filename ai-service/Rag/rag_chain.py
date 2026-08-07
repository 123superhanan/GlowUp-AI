from langchain_ollama import ChatOllama
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


def create_rag_chain(vectorstore, model_name: str = "llama3.2:3b"):
    llm = ChatOllama(
        model=model_name,
        temperature=0.3
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
        yield {
            "type": "sources",
            "sources": sources
        }

    return rag_with_sources, rag_stream