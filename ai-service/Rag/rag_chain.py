from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


def format_docs_with_sources(docs):
    """Format documents and collect sources"""
    content = "\n\n".join(doc.page_content for doc in docs)
    
    # Collect unique sources
    sources = set()
    for doc in docs:
        source = doc.metadata.get("source", "Unknown")
        # Get only the filename
        filename = source.split("\\")[-1].split("/")[-1]
        sources.add(filename)
    
    return content, list(sources)


def create_rag_chain(vectorstore, model_name: str = "llama3.2:3b"):
    """
    RAG Chain with Source Citation
    """

    llm = ChatOllama(
        model=model_name,
        temperature=0.3
    )

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    prompt = ChatPromptTemplate.from_template("""
You are a helpful men's style and grooming assistant.
Answer the question based only on the following context.
If you don't know the answer, just say you don't know.
Keep the answer clear and helpful.

Context:
{context}

Question: {question}

Answer:
""")

    def rag_with_sources(question: str):
        # Retrieve documents
        docs = retriever.invoke(question)
        
        # Format content + sources
        context, sources = format_docs_with_sources(docs)
        
        # Generate answer
        chain = prompt | llm | StrOutputParser()
        answer = chain.invoke({
            "context": context,
            "question": question
        })
        
        return {
            "answer": answer,
            "sources": sources
        }

    return rag_with_sources