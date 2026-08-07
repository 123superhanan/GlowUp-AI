import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from utils.validation import validate_image
from utils.image_loader import load_image
from inference.hair_type_infernce import predict_hair_type


router = APIRouter(
    prefix="/hair-type",
    tags=["Hair Type"]
)

@router.get("/")
def health_check():
    return {
        "success": True,
        "service": "Hair Type Inference API",
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
        predicted_hair_type = predict_hair_type(image)

        return {
            "success": True,
            "predicted_hair_type": predicted_hair_type
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))