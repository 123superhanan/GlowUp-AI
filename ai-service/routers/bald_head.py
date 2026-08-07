import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from utils.validation import validate_image
from utils.image_loader import load_image
from inference.Bald_infernce import predict_bald


router = APIRouter(
    prefix="/bald",
    tags=["Bald"]
)

@router.get("/")
def health_check():
    return {
        "success": True,
        "service": "Bald Inference API",
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
        predicted_bald_status = predict_bald(image)

        return {
            "success": True,
            "predicted_bald_status": predicted_bald_status
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))