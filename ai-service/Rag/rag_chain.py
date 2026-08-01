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
Priority:
1. Answer the user's question first
2. Use profile details only to personalize the answer
3. Use only the given context

Rules:
- Answer only from the given context.
- Be direct, practical, and specific.
- Do not mention weight, fitness struggles, or medical topics.
- Do not give makeup advice.
- Do not ask questions back to the user.
- Structure the answer in these sections when relevant:
  1. Hairstyle
  2. Beard / Facial hair
  3. Clothing
  4. Quick tips
- Keep each section short and actionable.
- If the context is not enough, say you don't have enough information.

Context:
{context}

Question:
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