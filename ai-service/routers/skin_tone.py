import os
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

from utils.validation import validate_image
from utils.image_loader import load_image
from inference.skin_tone_inference import predict_skin_tone

# Import your unified RAG service layer module
from Rag.recommendation import RecommendationService

router = APIRouter(
    prefix="/skin-tone",
    tags=["Skin Tone"]
)

# Instantiate the RAG service targeting your active local model image
ai_service = RecommendationService(model_name="llama3.2:3b")


@router.get("/")
def health_check():
    return {
        "success": True,
        "service": "Skin Tone Inference API",
        "status": "Running"
    }


@router.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # 1. Image Security and Boundary Validation
        is_valid, message = await validate_image(file)
        if not is_valid:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "message": message
                }
            )

        # 2. Extract and load pixel streams into memory
        image = await load_image(file)

        # 3. Vision Core Evaluation (e.g., returns "Olive", "Fair", "Deep")
        skin_tone_result = predict_skin_tone(image)

        # 4. Automated Query Generation 
        # Formulate a targeted RAG question using the raw prediction value
        rag_query = f"What clothing colors, style choices, and seasonal tones look best on {skin_tone_result} skin?"
        
        # Query ChromaDB and let llama3.2:3b extract grounded recommendations
        ai_recommendations = ai_service.ask(rag_query, top_k=2)

        # 5. Deliver fully enriched operational parameters back to the app layer
        return {
            "success": True,
            "prediction": skin_tone_result,
            "recommendations": ai_recommendations
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Internal Server Error",
                "error": str(e)
            }
        )
