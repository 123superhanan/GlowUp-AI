import os
from pathlib import Path
import torch
from PIL import Image

# Internal Imports
from backend.models.cnn import CNN
from backend.utils.classes import SKIN_TONE_CLASSES
from backend.utils.preprocess import preprocess_image
from backend.utils.confidence import get_prediction

# ==========================================
# Paths (Resolved dynamically from project root)
# ==========================================
# __file__ is inside 'backend/inference/'
# .parent goes to 'backend/', .parent.parent goes to root 'ai-service/'
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / "backend" / "models" / "skin_tone_model.pth"

# Double check if path string formatting is clean
if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Could not find model file at: {MODEL_PATH}")

# ==========================================
# Device
# ==========================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ==========================================
# Load Model (Runs Once)
# ==========================================
skin_model = CNN(num_classes=len(SKIN_TONE_CLASSES))

skin_model.load_state_dict(
    torch.load(
        str(MODEL_PATH),
        map_location=device
    )
)

skin_model.to(device)
skin_model.eval()


# ==========================================
# Prediction Function
# ==========================================
def predict_skin_tone(image: Image.Image):
    """
    Predict the user's skin tone.

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
        output = skin_model(image)

    # Convert logits to readable prediction
    result = get_prediction(
        output,
        SKIN_TONE_CLASSES
    )

    return result
