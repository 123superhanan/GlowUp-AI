# Photos
#   ↓
# CNNs
#   ↓
# face_shape = oval
# skin_tone = brown
# hair_type = curly
# baldness = notbald
#   ↓
# stored user profile / prediction
#   ↓
# chat agent

# agents/agent_router.py

    #               User question
    #                    ↓
    #           classify_intent()
    #                    ↓
    #          ┌─────────┴─────────┐
    #          ↓                   ↓
    #     hairstyle             clothing
    #     beard                 skincare
    #     general
    #          ↓
    #       RAG agent
    #          ↓
    #    user profile
    #          +
    #    retrieved docs
    #          ↓
    #        LLM
    #          ↓
    #       answer

from typing import Optional

from .intent import classify_intent

from Rag.vectorstore import load_vectorstore
from Rag.rag_chain import create_rag_chain


# Load RAG once when the service starts
vectorstore = load_vectorstore()
rag_chain, rag_stream = create_rag_chain(vectorstore)


def build_profile_context(
    face_shape: Optional[str] = None,
    skin_tone: Optional[str] = None,
    body_type: Optional[str] = None,
    hair_type: Optional[str] = None,
    baldness: Optional[str] = None,
    preferences: Optional[str] = None,
) -> str:

    profile = []

    if face_shape:
        profile.append(f"Face shape: {face_shape}")

    if skin_tone:
        profile.append(f"Skin tone: {skin_tone}")

    if body_type:
        profile.append(f"Body type: {body_type}")

    if hair_type:
        profile.append(f"Hair type: {hair_type}")

    if baldness:
        profile.append(f"Baldness status: {baldness}")

    if preferences:
        profile.append(f"Style preference: {preferences}")

    if not profile:
        return "No user profile information available."

    return "\n".join(profile)


def run_agent(
    question: str,
    face_shape: Optional[str] = None,
    skin_tone: Optional[str] = None,
    body_type: Optional[str] = None,
    hair_type: Optional[str] = None,
    baldness: Optional[str] = None,
    preferences: Optional[str] = None,
):
    """
    Main AI entry point.

    1. Detect user intent
    2. Build user profile
    3. Select agent
    4. Run agent
    """

    intent = classify_intent(question)

    profile_context = build_profile_context(
        face_shape=face_shape,
        skin_tone=skin_tone,
        body_type=body_type,
        hair_type=hair_type,
        baldness=baldness,
        preferences=preferences,
    )

    full_question = f"""
User profile:
{profile_context}

Detected intent:
{intent}

User question:
{question}
""".strip()

    # Currently RAG handles all intents.
    # Later you can replace these with separate agents.

    if intent == "hairstyle":
        result = rag_chain(full_question)

    elif intent == "beard":
        result = rag_chain(full_question)

    elif intent == "skincare":
        result = rag_chain(full_question)

    elif intent == "clothing":
        result = rag_chain(full_question)

    else:
        result = rag_chain(full_question)

    return {
        "intent": intent,
        "answer": result["answer"],
        "sources": result["sources"],
        "profile": {
            "face_shape": face_shape,
            "skin_tone": skin_tone,
            "body_type": body_type,
            "hair_type": hair_type,
            "baldness": baldness,
            "preferences": preferences,
        },
    }