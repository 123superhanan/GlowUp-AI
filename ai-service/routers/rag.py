from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import json

from Rag.vectorstore import load_vectorstore
from Rag.rag_chain import create_rag_chain

router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)

vectorstore = load_vectorstore()
rag_chain, rag_stream = create_rag_chain(vectorstore)


class QueryRequest(BaseModel):
    question: str
    face_shape: Optional[str] = None
    skin_tone: Optional[str] = None
    body_type: Optional[str] = None
    preferences: Optional[str] = None


def build_question(request: QueryRequest) -> str:
    profile_parts = []
    if request.face_shape:
        profile_parts.append(f"Face shape: {request.face_shape}")
    if request.skin_tone:
        profile_parts.append(f"Skin tone: {request.skin_tone}")
    if request.hair_type:
        profile_parts.append(f"Hair type: {request.hair_type}")
    if request.preferences:
        profile_parts.append(f"Style preference: {request.preferences}")

    profile_text = "\n".join(profile_parts) if profile_parts else "No profile provided"

    return f"""
Answer this user question specifically:
{request.question}

Use this profile only as extra context:
{profile_text}
""".strip()


@router.get("/")
def rag_health():
    return {
        "success": True,
        "service": "RAG Style Assistant",
        "status": "Running"
    }


@router.post("/ask")
def ask_question(request: QueryRequest):
    full_question = build_question(request)
    result = rag_chain(full_question)

    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "user_profile": {
            "face_shape": request.face_shape,
            "skin_tone": request.skin_tone,
            "hair_type": request.hair_type,
            "preferences": request.preferences
        }
    }


@router.post("/ask/stream")
def ask_question_stream(request: QueryRequest):
    full_question = build_question(request)

    def event_generator():
        for chunk in rag_stream(full_question):
            if isinstance(chunk, dict) and chunk.get("type") == "sources":
                yield f"data: {json.dumps({'type': 'sources', 'sources': chunk['sources']})}\n\n"
            else:
                yield f"data: {json.dumps({'type': 'token', 'content': chunk})}\n\n"

        yield "data: {\"type\": \"done\"}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )