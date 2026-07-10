from PIL import Image
from fastapi import UploadFile

# Allowed image formats
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

# Maximum file size (5 MB)
MAX_FILE_SIZE = 5 * 1024 * 1024


async def validate_image(file: UploadFile):
    """
    Validate an uploaded image.

    Returns:
        (bool, str)
        True, "" if valid
        False, "reason" if invalid
    """

    # Check if a file was uploaded
    if not file:
        return False, "No file uploaded."

    # Check file extension
    extension = file.filename.split(".")[-1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        return False, "Only JPG, JPEG and PNG images are allowed."

    # Read file bytes
    contents = await file.read()

    # Check file size
    if len(contents) > MAX_FILE_SIZE:
        return False, "Image size must be less than 5 MB."

    # Check corrupted image
    try:
        image = Image.open(file.file)
        image.verify()
    except Exception:
        return False, "Invalid or corrupted image."

    # Reset pointer for later reading
    await file.seek(0)

    return True, ""