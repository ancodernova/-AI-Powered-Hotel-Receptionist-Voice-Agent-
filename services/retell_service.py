# services/retell_service.py
import requests
from config import RETELL_API_KEY, configure_logging

logger = configure_logging()
RETELL_API_URL = "https://api.retell.ai/v1/voice"  # Adjust per Retell docs

def generate_voice_response(text):
    headers = {"Authorization": f"Bearer {RETELL_API_KEY}"}
    payload = {"text": text, "voice_id": "default-voice", "format": "mp3"}
    try:
        response = requests.post(RETELL_API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json().get("audio_url")
        logger.error(f"Retell API error: {response.status_code}")
        return None
    except Exception as e:
        logger.error(f"Retell request failed: {str(e)}")
        return None

def get_retell_response(prompt, user_input):
    full_prompt = f"{prompt}\nUser: {user_input}"
    headers = {"Authorization": f"Bearer {RETELL_API_KEY}"}
    payload = {"text": full_prompt}
    try:
        response = requests.post(RETELL_API_URL + "/text", headers=headers, json=payload)  # Hypothetical endpoint
        if response.status_code == 200:
            text_response = response.json().get("response")
            audio_url = generate_voice_response(text_response)
            return text_response, audio_url
        return "Sorry, I couldn’t assist you.", None
    except Exception as e:
        logger.error(f"Retell text failed: {str(e)}")
        return "Sorry, I couldn’t assist you.", None