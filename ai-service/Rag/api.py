from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from vectorstore import load_vectorstore
from rag_chain import create_rag_chain

app = FastAPI(title="Men's Style RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load vectorstore and chain once
vectorstore = load_vectorstore()
rag_chain = create_rag_chain(vectorstore)


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[str]


@app.get("/")
def home():
    return {"message": "GlowUp AI RAG API is running"}


@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    result = rag_chain(request.question)
    return {
        "answer": result["answer"],
        "sources": result["sources"]
    }