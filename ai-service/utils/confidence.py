import torch


def get_prediction(output, classes):
    """
    Convert model output into prediction and confidence.

    Args:
        output (torch.Tensor): Raw model output (logits).
        classes (list): List of class names.

    Returns:
        dict
    """

    # Convert logits to probabilities
    probabilities = torch.softmax(output, dim=1)

    # Get highest probability
    confidence, predicted = torch.max(probabilities, dim=1)

    return {
        "class": classes[predicted.item()],
        "confidence": round(confidence.item() * 100, 2)
    }