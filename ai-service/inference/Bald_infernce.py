import torch
from PIL import Image

# Internal Imports
from models.cnn import SimpleCNN
from utils.classes import  BALD_CLASSES
from utils.preprocess import preprocess_image
from utils.confidence import get_prediction

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

bald_model = SimpleCNN(num_classes=len(BALD_CLASSES))

bald_model.load_state_dict(
    torch.load(
        "models/bald_model.pth",
        map_location=device
    )
)

bald_model.to(device)
bald_model.eval()

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