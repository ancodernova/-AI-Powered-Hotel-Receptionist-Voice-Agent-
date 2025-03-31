import requests
from config import GROQ_API_KEY, configure_logging

logger = configure_logging()
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def get_groq_response(prompt, user_input):
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama3-70b-8192",
        "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": user_input}],
        "max_tokens": 500,
        "temperature": 0.7
    }
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        logger.error(f"Groq API error: {response.status_code}")
        return "Sorry, I couldn’t process that."
    except Exception as e:
        logger.error(f"Groq request failed: {str(e)}")
        return "Sorry, I couldn’t process that."