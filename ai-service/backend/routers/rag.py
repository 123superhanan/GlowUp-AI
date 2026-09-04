from fastapi import APIRouter, UploadFile, File, Form, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import json
import io

from PIL import Image

from Rag.vectorstore import load_vectorstore
from Rag.rag_chain import create_rag_chain

from backend.inference.Bald_infernce import predict_bald
from backend.inference.hair_type_infernce import predict_hair_type


router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)


class QueryRequest(BaseModel):
    question: str
    face_shape: Optional[str] = None
    skin_tone: Optional[str] = None
    body_type: Optional[str] = None
    hair_type: Optional[str] = None
    preferences: Optional[str] = None


def build_hybrid_question(
    question: str,
    face_shape: Optional[str],
    skin_tone: Optional[str],
    hair_type: Optional[str],
    bald_status: Optional[str],
    preferences: Optional[str]
) -> str:

    profile_parts = []

    if face_shape:
        profile_parts.append(f"Face shape: {face_shape}")

    if skin_tone:
        profile_parts.append(f"Skin tone: {skin_tone}")

    if hair_type:
        profile_parts.append(f"Hair type/structure: {hair_type}")

    if bald_status:
        profile_parts.append(f"Scalp/Baldness status: {bald_status}")

    if preferences:
        profile_parts.append(f"Style preference: {preferences}")

    profile_text = (
        "\n".join(profile_parts)
        if profile_parts
        else "No profile provided"
    )

    return f"""
Answer this user question specifically:
{question}

Use this profile only as extra context:
{profile_text}
""".strip()


@router.post("/ask")
async def ask_question(
    request: Request,
    question: str = Form(...),
    face_shape: Optional[str] = Form(None),
    skin_tone: Optional[str] = Form(None),
    preferences: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):

    detected_hair = None
    detected_bald = None

    if file:
        image_bytes = await file.read()

        pil_image = Image.open(
            io.BytesIO(image_bytes)
        ).convert("RGB")

        bald_res = predict_bald(pil_image)
        hair_res = predict_hair_type(pil_image)

        detected_bald = bald_res.get("class")
        detected_hair = hair_res.get("class")

    full_question = build_hybrid_question(
        question,
        face_shape,
        skin_tone,
        detected_hair,
        detected_bald,
        preferences
    )

    result = request.app.state.rag_chain(full_question)

    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "user_profile": {
            "face_shape": face_shape,
            "skin_tone": skin_tone,
            "detected_hair_type": detected_hair,
            "detected_bald_status": detected_bald,
            "preferences": preferences
        }
    }


@router.post("/ask/stream")
def ask_question_stream(
    request: Request,
    query: QueryRequest
):

    full_question = build_hybrid_question(
        question=query.question,
        face_shape=query.face_shape,
        skin_tone=query.skin_tone,
        hair_type=query.hair_type,
        bald_status=query.body_type,
        preferences=query.preferences
    )

    rag_stream = request.app.state.rag_stream

    def event_generator():

        for chunk in rag_stream(full_question):

            if isinstance(chunk, dict) and chunk.get("type") == "sources":

                yield (
                    f"data: {json.dumps({
                        'type': 'sources',
                        'sources': chunk['sources']
                    })}\n\n"
                )

            else:

                yield (
                    f"data: {json.dumps({
                        'type': 'token',
                        'content': chunk
                    })}\n\n"
                )

        yield 'data: {"type": "done"}\n\n'

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )