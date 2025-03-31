# services/llama_service.py
import requests
from config import LLAMA_API_KEY, configure_logging

logger = configure_logging()
LLAMA_API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"

def get_llama_response(prompt, user_input):
    headers = {"Authorization": f"Bearer {LLAMA_API_KEY}"}
    payload = {
        "inputs": f"{prompt}\nUser: {user_input}\nAI: ",
        "parameters": {"max_length": 200, "temperature": 0.7}
    }
    try:
        response = requests.post(LLAMA_API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()[0]["generated_text"].split("AI: ")[-1].strip()
        logger.error(f"LLaMA API error: {response.status_code}")
        return "I’m not sure how to help with that."
    except Exception as e:
        logger.error(f"LLaMA request failed: {str(e)}")
        return "I’m not sure how to help with that."