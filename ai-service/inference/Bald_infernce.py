import torch
from PIL import Image

# Internal Imports
from models.cnn import CNN
from utils.classes import  BALD_CLASSES
from utils.preprocess import preprocess_image
from utils.confidence import get_prediction

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

hair_model = CNN(num_classes=len(BALD_CLASSES))

hair_model.load_state_dict(
    torch.load(
        "models/bald_model.pth",
        map_location=device
    )
)

hair_model.to(device)
hair_model.eval()

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

        output = hair_model(image)

    result = get_prediction(
                output,
                BALD_CLASSES
            )
        
    return result