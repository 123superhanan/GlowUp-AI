from PIL import Image
from fastapi import UploadFile


async def load_image(file: UploadFile):
    """
    Load an uploaded image as a PIL Image.

    Args:
        file (UploadFile): Uploaded image.

    Returns:
        PIL.Image
    """

    image = Image.open(file.file)

    return image