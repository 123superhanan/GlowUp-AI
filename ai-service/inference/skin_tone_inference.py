import torch
from PIL import Image

# Import internal modular components
from models.cnn import CNN
from utils.classes import SKIN_TONE_CLASSES
from utils.preprocess import preprocess_image
from utils.confidence import get_prediction
from config import SKIN_TONE_MODEL

# ==========================================
# Device
# ==========================================

device =  torch.device("cuda" if torch.cuda.is_available() else "cpu")

import torch
from PIL import Image

# Internal Imports
from models.cnn import CNN
from utils.classes import SKIN_TONE_CLASSES
from utils.preprocess import preprocess_image
from utils.confidence import get_prediction

# ==========================================
# Device
# ==========================================

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ==========================================
# Load Model (Runs Once)
# ==========================================

skin_model = CNN(num_classses=len(SKIN_TONE_CLASSES))
skin_model.load_state_dict(
    torch.load(SKIN_TONE_MODEL, map_location=device)
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
    