import requests

API_BASE = "http://127.0.0.1:8000"

REQUEST_TIMEOUT = 120


def api_request(method, endpoint, files=None, json=None):
    """
    Generic FastAPI request handler.
    """

    url = f"{API_BASE}{endpoint}"

    try:
        if method.upper() == "GET":
            response = requests.get(
                url,
                timeout=5
            )

        elif method.upper() == "POST":
            response = requests.post(
                url,
                files=files,
                json=json,
                timeout=REQUEST_TIMEOUT
            )

        else:
            return {
                "success": False,
                "message": "Unsupported request method."
            }

        response.raise_for_status()

        return {
            "success": True,
            "data": response.json()
        }

    except requests.exceptions.ConnectionError:

        return {
            "success": False,
            "message": "Cannot connect to FastAPI server."
        }

    except requests.exceptions.Timeout:

        return {
            "success": False,
            "message": "Request timed out."
        }

    except requests.exceptions.HTTPError:

        return {
            "success": False,
            "message": response.text
        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }


def health_check():
    return api_request(
        "GET",
        "/"
    )


def predict_face(image_bytes):

    files = {
        "file": (
            "image.png",
            image_bytes,
            "image/png"
        )
    }

    return api_request(
        "POST",
        "/face-shape/predict",
        files=files
    )


def predict_skin(image_bytes):

    files = {
        "file": (
            "image.png",
            image_bytes,
            "image/png"
        )
    }

    return api_request(
        "POST",
        "/skin-tone/predict",
        files=files
    )


def ask_glowup(face_shape, skin_tone, question):

    payload = {

        "face_shape": face_shape,

        "skin_tone": skin_tone,

        "query": question

    }

    return api_request(
        "POST",
        "/recommendations",
        json=payload
    )