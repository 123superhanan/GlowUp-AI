import requests
import json
from typing import Generator, Optional

BASE_URL = "http://localhost:8000"

def detect_features(image_file) -> dict:
    """Call all CNN endpoints and return results"""
    results = {}

    endpoints = {
        "face_shape": "/face-shape/predict",
        "skin_tone": "/skin-tone/predict",
        "bald_status": "/bald/predict",
        "hair_type": "/hair-type/predict",
    }

    for key, path in endpoints.items():
        try:
            image_file.seek(0)
            files = {"file": (image_file.name, image_file.getvalue(), image_file.type)}
            r = requests.post(f"{BASE_URL}{path}", files=files, timeout=60)
            if r.ok:
                data = r.json()
                # Handle different response shapes
                pred = data.get("prediction") or data.get(f"predicted_{key}") or data
                if isinstance(pred, dict):
                    results[key] = pred.get("class") or pred.get("label")
                else:
                    results[key] = pred
        except Exception as e:
            results[key] = None
            print(f"Error in {key}: {e}")

    return results


def stream_rag_response(
    question: str,
    face_shape: Optional[str] = None,
    skin_tone: Optional[str] = None,
    body_type: Optional[str] = None,
    hair_type: Optional[str] = None,
    preferences: Optional[str] = None,
) -> Generator:
    """Stream response from /rag/ask/stream"""
    payload = {
        "question": question,
        "face_shape": face_shape or None,
        "skin_tone": skin_tone or None,
        "body_type": body_type or None,
        "hair_type": hair_type or None,
        "preferences": preferences or None,
    }

    response = requests.post(
        f"{BASE_URL}/rag/ask/stream",
        json=payload,
        stream=True,
        timeout=90
    )
    response.raise_for_status()

    for line in response.iter_lines(decode_unicode=True):
        if line and line.startswith("data: "):
            yield json.loads(line[6:])