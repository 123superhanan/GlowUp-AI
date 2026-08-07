import torch
from PIL import Image

# Internal Imports
from models.cnn import SimpleCNN
from utils.classes import  HAIR_TYPE_CLASSES
from utils.preprocess import preprocess_image
from utils.confidence import get_prediction

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

hair_model = SimpleCNN(num_classes=len(HAIR_TYPE_CLASSES))

hair_model.load_state_dict(
    torch.load(
        "models/hair_type_model.pth",
        map_location=device
    )
)

hair_model.to(device)
hair_model.eval()

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