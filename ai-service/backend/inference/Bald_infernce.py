import os
from pathlib import Path
import torch
from PIL import Image

# Internal Imports
from backend.models.cnn import SimpleCNN
from backend.utils.classes import BALD_CLASSES
from backend.utils.preprocess import preprocess_image
from backend.utils.confidence import get_prediction

# ==========================================
# Paths (Resolved dynamically from project root)
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / "backend" / "models" / "bald_model.pth"

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Could not find model file at: {MODEL_PATH}")

# ==========================================
# Device
# ==========================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ==========================================
# Load Model (Runs Once)
# ==========================================
bald_model = SimpleCNN(num_classes=len(BALD_CLASSES))

bald_model.load_state_dict(
    torch.load(
        str(MODEL_PATH),
        map_location=device
    )
)

bald_model.to(device)
bald_model.eval()


# ==========================================
# Prediction Function
# ==========================================
def predict_bald(image: Image.Image):
    """
    Predict the user's bald status.

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
        output = bald_model(image)

    result = get_prediction(
        output,
        BALD_CLASSES
    )
        
    return result
