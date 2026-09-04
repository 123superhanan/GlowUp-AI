print("1 - starting")

from contextlib import asynccontextmanager
print("2 - contextlib OK")

from fastapi import FastAPI
print("3 - fastapi OK")

from backend.routers.skin_tone import router as skin_tone_router
print("4 - skin router OK")

from backend.routers.face_shape import router as face_shape_router
print("5 - face router OK")

from backend.routers.bald_head import router as bald_head_router
print("6 - bald router OK")

from backend.routers.hair_type import router as hair_type_router
print("7 - hair router OK")

from backend.routers.rag import router as rag_router
print("8 - rag router OK")

from Rag.vectorstore import load_vectorstore
print("9 - vectorstore OK")

from Rag.rag_chain import create_rag_chain
print("10 - rag chain OK")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("LIFESPAN")
    yield


print("11 - before FastAPI")

app = FastAPI(
    title="GlowUp AI Service",
    version="1.0.0",
    description="AI Inference Microservice",
    lifespan=lifespan
)

print("12 - FastAPI created")

app.include_router(skin_tone_router)
print("13 - skin included")

app.include_router(face_shape_router)
print("14 - face included")

app.include_router(rag_router)
print("15 - rag included")

app.include_router(bald_head_router)
print("16 - bald included")

app.include_router(hair_type_router)
print("17 - hair included")

print("18 - DONE")