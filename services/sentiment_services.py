# services/sentiment_service.py
from config import configure_logging

logger = configure_logging()

def analyze_sentiment(user_input):
    user_input = user_input.lower()
    if any(word in user_input for word in ["angry", "upset", "frustrated", "rude", "bad"]):
        return "negative"
    elif any(word in user_input for word in ["happy", "great", "good", "excited"]):
        return "positive"
    return "neutral"

def adjust_response(sentiment, base_response):
    if sentiment == "negative":
        return f"I’m sorry you feel that way. {base_response} How can I assist you further?"
    elif sentiment == "positive":
        return f"I’m glad you’re pleased! {base_response}"
    return base_response