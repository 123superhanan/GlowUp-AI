from fastapi import FastAPI
from routers.skin_tone import router as skin_tone_router
from routers.face_shape import router as face_shape_router
from routers.bald_head import router as bald_head_router
from routers.hair_type import router as hair_type_router  
from routers.rag import router as rag_router          

app = FastAPI(
    title="GlowUp AI Service",
    version="1.0.0",
    description="AI Inference Microservice"
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
app.include_router(hair_type_router)  # NEW