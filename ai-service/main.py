from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="StockWise AI Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "ai-service"}

@app.post("/detect-receipt")
async def detect_receipt(file: UploadFile = File(...)):
    # Placeholder - ML model will go here
    return {"detected": True, "message": "Receipt detection coming soon"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


