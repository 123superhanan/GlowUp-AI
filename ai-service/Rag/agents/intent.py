
# Node chat.controller
#         ↓
# AI service
#         ↓
# agent_router.py
#         ↓
# intent.py
#         ↓
# ┌──────────────┬──────────────┬──────────────┐
# │ hairstyle    │ skincare     │ general      │
# │              │              │              │
# ↓              ↓              ↓
# RAG            RAG            RAG


# agents/intent.py

def classify_intent(question: str) -> str:
    """
    Basic intent classifier.

    Returns:
        hairstyle
        beard
        skincare
        clothing
        general
    """

    question = question.lower().strip()

    if any(word in question for word in [
        "hair",
        "hairstyle",
        "haircut",
        "fade",
        "curl",
        "curly",
        "wavy",
        "straight",
        "dreadlock"
    ]):
        return "hairstyle"

    if any(word in question for word in [
        "beard",
        "mustache",
        "moustache",
        "facial hair",
        "shave"
    ]):
        return "beard"

    if any(word in question for word in [
        "skin",
        "skincare",
        "acne",
        "face wash",
        "moisturizer",
        "dry skin",
        "oily skin"
    ]):
        return "skincare"

    if any(word in question for word in [
        "clothes",
        "clothing",
        "outfit",
        "shirt",
        "pants",
        "trousers",
        "style",
        "fashion"
    ]):
        return "clothing"

    return "general"