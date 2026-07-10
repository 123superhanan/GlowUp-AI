from fastapi import FastAPI
from routers.skin_tone import router as skin_tone_router

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