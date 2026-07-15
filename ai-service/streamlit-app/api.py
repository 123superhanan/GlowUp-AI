import requests

API_BASE = "http://127.0.0.1:8000"
REQUEST_TIMEOUT = 120

# ============================================================
# TOGGLE THIS TO DISABLE RAG TEMPORARILY
# ============================================================
USE_RAG = False  # Set to False to use mock recommendations

def api_request(method, endpoint, files=None, json=None):
    """
    Generic FastAPI request handler.
    """
    url = f"{API_BASE}{endpoint}"

    try:
        if method.upper() == "GET":
            response = requests.get(url, timeout=5)
        elif method.upper() == "POST":
            response = requests.post(
                url,
                files=files,
                json=json,
                timeout=REQUEST_TIMEOUT
            )
        else:
            return {"success": False, "message": "Unsupported request method."}

        response.raise_for_status()
        return {"success": True, "data": response.json()}

    except requests.exceptions.ConnectionError:
        return {"success": False, "message": "Cannot connect to FastAPI server."}
    except requests.exceptions.Timeout:
        return {"success": False, "message": "Request timed out."}
    except requests.exceptions.HTTPError:
        return {"success": False, "message": response.text}
    except Exception as e:
        return {"success": False, "message": str(e)}


def health_check():
    return api_request("GET", "/")


def predict_face(image_bytes):
    files = {"file": ("image.png", image_bytes, "image/png")}
    return api_request("POST", "/face-shape/predict", files=files)


def predict_skin(image_bytes):
    files = {"file": ("image.png", image_bytes, "image/png")}
    return api_request("POST", "/skin-tone/predict", files=files)


# ============================================================
# RECOMMENDATIONS WITH RAG TOGGLE
# ============================================================
def ask_glowup(face_shape, skin_tone, question):
    """
    Get recommendations. Uses RAG if enabled, otherwise mock.
    """
    if USE_RAG:
        # Use actual RAG endpoint
        payload = {
            "face_shape": face_shape,
            "skin_tone": skin_tone,
            "query": question
        }
        return api_request("POST", "/recommendations", json=payload)
    else:
        # Mock recommendations (no API call)
        return get_mock_recommendations(face_shape, skin_tone, question)


def get_mock_recommendations(face_shape, skin_tone, question):
    """
    Generate mock recommendations based on face shape and skin tone.
    This runs locally without hitting any API.
    """
    
    # Face shape recommendations
    face_recs = {
        "Oval": {
            "hairstyles": "Pompadour, Side Part, Textured Crop",
            "beard": "Any style works (goatee, stubble, full beard)",
            "glasses": "Square, Rectangular, Aviator",
            "avoid": "Heavy bangs, flat center part"
        },
        "Square": {
            "hairstyles": "Textured Crop, Side Swept Bangs, Pompadour",
            "beard": "Goatee with mustache, Circle Beard",
            "glasses": "Round, Oval, Aviator",
            "avoid": "Buzz cut, center part"
        },
        "Round": {
            "hairstyles": "Pompadour, Faux Hawk, Slick Back",
            "beard": "Goatee with soul patch, Anchor Beard",
            "glasses": "Square, Rectangular, Geometric",
            "avoid": "Center part, full bangs"
        },
        "Heart": {
            "hairstyles": "Side Swept Bangs, Chin-Length Bob",
            "beard": "Full Goatee, Van Dyke",
            "glasses": "Round, Oval, Rimless",
            "avoid": "Volume at top, pixie cut"
        },
        "Oblong": {
            "hairstyles": "Long Bangs, Layered Cut, Curly/Wavy",
            "beard": "Full Beard, Stubble",
            "glasses": "Square, Oversized, Wayfarer",
            "avoid": "Long hair straight, top volume"
        }
    }
    
    # Skin tone recommendations
    skin_recs = {
        "Olive": {
            "routine": "Gentle foaming cleanser → Rose water → Vitamin C → Lightweight gel moisturizer → SPF 50+",
            "products": "CeraVe Foaming Cleanser, The Ordinary Vitamin C, Neutrogena Hydro Boost",
            "makeup": "Warm yellow/golden undertones, terracotta blush, nude brown lipstick",
            "avoid": "Ash-toned foundations, cool pink blushes"
        },
        "White": {
            "routine": "Creamy milk cleanser → Hydrating toner → Niacinamide → Rich cream → SPF 50+",
            "products": "La Roche-Posay Toleriane, The Ordinary Niacinamide, CeraVe Daily Moisturizer",
            "makeup": "Pink/neutral undertones, soft pink blush, rose lipstick",
            "avoid": "Yellow/olive foundations, deep orange bronzers"
        },
        "Dark Brown": {
            "routine": "Creamy cleanser → Acid toner → Alpha Arbutin → Shea butter cream → SPF 50+",
            "products": "Black Girl Sunscreen Cleanser, Good Molecules Serum, SheaMoisture Cream",
            "makeup": "Red/golden undertones, deep berry blush, deep red lipstick",
            "avoid": "Ashy/grey foundations, pale pink blushes"
        }
    }
    
    # Get recommendations
    face_data = face_recs.get(face_shape, face_recs["Oval"])
    skin_data = skin_recs.get(skin_tone, skin_recs["Olive"])
    
    # Build response
    response = f"""
Based on your {face_shape} face shape and {skin_tone} skin tone:

HAIRSTYLE RECOMMENDATIONS:
• Best: {face_data['hairstyles']}
• Beard: {face_data['beard']}
• Glasses: {face_data['glasses']}
• Avoid: {face_data['avoid']}

SKINCARE ROUTINE:
• Routine: {skin_data['routine']}
• Products: {skin_data['products']}
• Makeup: {skin_data['makeup']}
• Avoid: {skin_data['avoid']}

YOUR QUESTION: {question}

ADDITIONAL TIPS:
• Stay hydrated (2-3L water daily)
• Get 7-8 hours of sleep
• Use SPF 50+ daily
• Maintain consistent routine
• Track progress weekly
"""
    
    # Return in same format as API
    return {
        "success": True,
        "data": {
            "response": response,
            "recommendations": [
                {"title": "Hairstyle", "description": face_data['hairstyles']},
                {"title": "Beard", "description": face_data['beard']},
                {"title": "Glasses", "description": face_data['glasses']},
                {"title": "Skincare", "description": skin_data['routine']},
                {"title": "Products", "description": skin_data['products']},
                {"title": "Makeup", "description": skin_data['makeup']}
            ],
            "context": {
                "face_shape": face_shape,
                "skin_tone": skin_tone,
                "query": question
            }
        }
    }