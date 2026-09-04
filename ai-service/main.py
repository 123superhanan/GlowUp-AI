from contextlib import asynccontextmanager
from dotenv import load_dotenv


from fastapi import FastAPI

from backend.routers.skin_tone import router as skin_tone_router
from backend.routers.face_shape import router as face_shape_router
from backend.routers.bald_head import router as bald_head_router
from backend.routers.hair_type import router as hair_type_router
from backend.routers.rag import router as rag_router

from Rag.vectorstore import load_vectorstore
from Rag.rag_chain import create_rag_chain

load_dotenv()
@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Loading GlowUp RAG...")

    vectorstore = load_vectorstore()

    rag_chain, rag_stream = create_rag_chain(
        vectorstore
    )

    app.state.vectorstore = vectorstore
    app.state.rag_chain = rag_chain
    app.state.rag_stream = rag_stream

    print("GlowUp RAG loaded successfully.")

    yield

    print("Shutting down GlowUp RAG...")


app = FastAPI(
    title="GlowUp AI Service",
    version="1.0.0",
    description="AI Inference Microservice",
    lifespan=lifespan
)


@app.get("/")
def root():
    return {
        "success": True,
        "message": "GlowUp AI Service is running."
    }


@app.get("/health")
def health():
    return {
        "success": True,
        "status": "healthy"
    }


app.include_router(skin_tone_router)
app.include_router(face_shape_router)
app.include_router(rag_router)
app.include_router(bald_head_router)
app.include_router(hair_type_router)