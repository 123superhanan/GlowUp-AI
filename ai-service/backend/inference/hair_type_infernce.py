import os
from pathlib import Path
import torch
from PIL import Image

# Internal Imports
from backend.models.cnn import SimpleCNN
from backend.utils.classes import HAIR_TYPE_CLASSES
from backend.utils.preprocess import preprocess_image
from backend.utils.confidence import get_prediction

# ==========================================
# Paths (Resolved dynamically from project root)
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / "backend" / "models" / "hair_type_model.pth"

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Could not find model file at: {MODEL_PATH}")

# ==========================================
# Device
# ==========================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ==========================================
# Load Model (Runs Once)
# ==========================================
hair_model = SimpleCNN(num_classes=len(HAIR_TYPE_CLASSES))

hair_model.load_state_dict(
    torch.load(
        str(MODEL_PATH),
        map_location=device
    )
)

hair_model.to(device)
hair_model.eval()


# ==========================================
# Prediction Function
# ==========================================
def predict_hair_type(image: Image.Image):
    """
    Predict the user's hair type.

    Args:
        image (PIL.Image): Input image.

    Returns:
        dict:
        {
            "class": "...",
            "confidence": 99.45
        }
    """
    # Preprocess Image
    image = preprocess_image(image)
    image = image.to(device)

    # Disable Gradient Calculation
    with torch.no_grad():
        output = hair_model(image)

    result = get_prediction(
        output,
        HAIR_TYPE_CLASSES
    )
        
    return result
