from torchvision import transforms

# Same preprocessing used during training
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

def preprocess_image(image):
    """
    Preprocess an uploaded image for CNN inference.

    Args:
        image (PIL.Image): Uploaded image object.

    Returns:
        torch.Tensor: Image tensor with batch dimension.
    """
    image = image.convert("RGB")  # Ensure image is in RGB format
    image = transform(image)      # Apply the same transformations as during training
    image = image.unsqueeze(0)    # Add batch dimension

    return image
