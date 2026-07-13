import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from utils.validation import validate_image
from utils.image_loader import load_image
from inference.skin_tone_inference import predict_skin_tone

# Import your unified RAG service layer
from Rag.recommendation import RecommendationService

router = APIRouter(
    prefix="/skin-tone",
    tags=["Skin Tone"]
)

# Initialize the RAG service to use your active local model tag
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
        # 1. Validate Image
        is_valid, message = await validate_image(file)
        if not is_valid:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "message": message
                }
            )

        # 2. Load Image
        image = await load_image(file)

        # 3. Computer Vision Prediction
        skin_tone_result = predict_skin_tone(image)

        # 4. Clean Label Extraction
        # Safely extract the raw string classification even if it's nested inside a dictionary
        tone_label = (
            skin_tone_result.get("class", "Olive")
            if isinstance(skin_tone_result, dict)
            else skin_tone_result
        )

        # 5. Dynamic RAG Query Processing
        # Pass the raw classification label string directly to let the RAG engine query organically
        ai_recommendations = ai_service.ask(tone_label, top_k=2)

        # 6. Return the full payload back to Node.js
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
