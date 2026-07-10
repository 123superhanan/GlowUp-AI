from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

from utils.validation import validate_image
from utils.image_loader import load_image
from inference.skin_tone_inference import predict_skin_tone

router = APIRouter(
    prefix="/skin-tone",
    tags=["Skin Tone"]
)


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

        # Validate Image
        is_valid, message = await validate_image(file)

        if not is_valid:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "message": message
                }
            )

        # Load Image
        image = await load_image(file)

        # Predict
        result = predict_skin_tone(image)

        return {
            "success": True,
            "prediction": result
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