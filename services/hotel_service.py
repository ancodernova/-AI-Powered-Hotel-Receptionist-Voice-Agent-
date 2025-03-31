# services/hotel_service.py
from config import HOTEL_NAME, ADMIN_PHONE, HOTEL_PHONE, HOTEL_LOCATION, HOTEL_SERVICES, ROOMS, configure_logging
from database.database import get_available_rooms_for_date, book_room, log_interaction, get_user_history, get_all_bookings
from services.retell_service import get_retell_response
from services.sentiment_service import analyze_sentiment, adjust_response
from datetime import datetime, timedelta
import re

logger = configure_logging()

from services.groq_service import get_groq_response

def handle_customer_message(from_number, message, prompt, sentiment, timestamp):
    if "available" in message.lower():
        date # services/hotel_service.py
from config import HOTEL_NAME, ADMIN_PHONE, HOTEL_PHONE, HOTEL_LOCATION, HOTEL_SERVICES, ROOMS, configure_logging
from database.database import get_available_rooms_for_date, book_room, log_interaction, get_user_history, get_all_bookings, parse_date
from services.retell_service import get_retell_response
from services.llama_service import get_llama_response
from services.sentiment_service import analyze_sentiment, adjust_response
from datetime import datetime
import re

logger = configure_logging()

def negotiate_price(room_type, user_offer, current_price, min_price):
    if user_offer >= current_price:
        return current_price, f"That’s perfect! I can offer the {room_type} for ₹{current_price}."
    elif user_offer >= min_price:
        return user_offer, f"I can meet you at ₹{user_offer} for the {room_type}. Great deal!"
    else:
        return current_price, f"I’m sorry, but the lowest I can go is ₹{min_price} for the {room_type}."

def handle_message(from_number, message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    history = "\n".join([f"User: {m} | AI: {r}" for m, r in get_user_history(from_number)])
    sentiment = analyze_sentiment(message)
    prompt = f"""You are a polite, professional receptionist at {HOTEL_NAME}. Respond via WhatsApp voice.
    Stay humble, even with rude users. Use history: {history}."""

    if from_number == ADMIN_PHONE:
        return handle_admin_message(message)
    elif from_number == HOTEL_PHONE:
        return handle_hotel_message(message)
    else:
        return handle_customer_message(from_number, message, prompt, sentiment, timestamp)

def handle_customer_message(from_number, message, prompt, sentiment, timestamp):
    message_lower = message.lower()
    
    # Room availability
    if "available" in message_lower or "rooms" in message_lower:
        try:
            date = parse_date(message, fuzzy=True).strftime('%Y-%m-%d')
        except ValueError:
            date = datetime.now().strftime('%Y-%m-%d')
        rooms = get_available_rooms_for_date(date)
        response = f"Rooms available on {date}:\n" + "\n".join([f"{r[0]} - ₹{r[1]} ({r[2]} left)" for r in rooms])
    
    # Pricing details
    elif "how much" in message_lower or "price" in message_lower:
        room_type = "Deluxe" if "deluxe" in message_lower else "Suite" if "suite" in message_lower else None
        if room_type:
            response = f"The {room_type} is ₹{ROOMS[room_type]['price']}/night. Features: {ROOMS[room_type]['features']}."
        else:
            response = "We have Deluxe at ₹15000 and Suite at ₹25000 per night."
    
    # Hotel location
    elif "location" in message_lower or "where" in message_lower:
        response = f"We’re located at {HOTEL_LOCATION}. It’s a short walk from the Gateway of India!"
    
    # Room features and services
    elif "features" in message_lower or "services" in message_lower:
        if "room" in message_lower:
            room_type = "Deluxe" if "deluxe" in message_lower else "Suite"
            response = f"The {room_type} includes {ROOMS[room_type]['features']}."
        else:
            response = f"Our services include {HOTEL_SERVICES}."
    
    # Booking
    elif "book" in message_lower:
        room_type = "Deluxe" if "deluxe" in message_lower else "Suite"
        try:
            date = parse_date(message, fuzzy=True).strftime('%Y-%m-%d')
        except ValueError:
            date = datetime.now().strftime('%Y-%m-%d')
        if book_room(from_number, room_type, date):
            response = f"Your {room_type} booking for {date} is confirmed! Enjoy your stay."
        else:
            response = f"Sorry, no {room_type} available for {date}."
    
    # Price negotiation
    elif "offer" in message_lower or "cheaper" in message_lower:
        room_type = "Deluxe" if "deluxe" in message_lower else "Suite"
        user_offer = int(re.search(r'\d+', message).group(0)) if re.search(r'\d+', message) else 0
        current_price, negotiation_response = negotiate_price(room_type, user_offer, ROOMS[room_type]["price"], ROOMS[room_type]["min_price"])
        response = negotiation_response
    
    # Graceful exit
    elif "bye" in message_lower or "thanks" in message_lower:
        response = "Thank you for your time. Have a great day!"
    
    # LLaMA for suggestions/problem-solving
    elif "suggest" in message_lower or "help" in message_lower:
        llama_prompt = f"""You are a helpful assistant at {HOTEL_NAME}. Suggest solutions or enhancements based on user input and history: {history}."""
        response = get_llama_response(llama_prompt, message)
    
    # Default Retell AI response
    else:
        response, audio_url = get_retell_response(prompt, message)
        response = adjust_response(sentiment, response)
        if audio_url:
            response += f"\n[Voice]: {audio_url}"

    log_interaction(from_number, message, response, timestamp)
    return response

def handle_admin_message(message):
    if "bookings" in message.lower():
        bookings = get_all_bookings()
        return "Current Bookings:\n" + "\n".join([f"{b[0]}: {b[1]} on {b[2]} ({b[3]})" for b in bookings])
    elif "rooms" in message.lower():
        date = parse_date(message, fuzzy=True).strftime('%Y-%m-%d')
        rooms = get_available_rooms_for_date(date)
        return f"Rooms on {date}:\n" + "\n".join([f"{r[0]} - ₹{r[1]} ({r[2]} left)" for r in rooms])
    return "Admin commands: 'bookings', 'rooms'"

def handle_hotel_message(message):
    if "update" in message.lower():
        date = parse_date(message, fuzzy=True).strftime('%Y-%m-%d')
        rooms = get_available_rooms_for_date(date)
        return f"Room Status on {date}:\n" + "\n".join([f"{r[0]} - ₹{r[1]} ({r[2]} left)" for r in rooms])
    return "Hotel commands: 'update'"= parse_date(message, fuzzy=True).strftime('%Y-%m-%d')
        rooms = get_available_rooms_for_date(date)
        response = f"Rooms available on {date}:\n" + "\n".join([f"{r[0]} - ₹{r[1]} ({r[2]} left)" for r in rooms])
    elif "suggest" in message.lower():
        groq_prompt = f"You are a helpful assistant at {HOTEL_NAME}. Suggest solutions based on history: {history}."
        response = get_groq_response(groq_prompt, message)

def parse_date(message):
    today = datetime.now()
    if "next weekend" in message.lower():
        days_to_next_saturday = (5 - today.weekday() + 7) % 7 or 7
        return (today + timedelta(days=days_to_next_saturday)).strftime('%Y-%m-%d')
    match = re.search(r'(\d{4}-\d{2}-\d{2})', message)
    return match.group(0) if match else today.strftime('%Y-%m-%d')

def negotiate_price(room_type, user_offer, current_price, min_price):
    if user_offer >= current_price:
        return current_price, f"That’s perfect! I can offer the {room_type} for ₹{current_price}."
    elif user_offer >= min_price:
        return user_offer, f"I can meet you at ₹{user_offer} for the {room_type}. Great deal!"
    else:
        return current_price, f"I’m sorry, but the lowest I can go is ₹{min_price} for the {room_type}."

def handle_message(from_number, message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    history = "\n".join([f"User: {m} | AI: {r}" for m, r in get_user_history(from_number)])
    sentiment = analyze_sentiment(message)
    prompt = f"""You are a polite, professional receptionist at {HOTEL_NAME}. Respond via WhatsApp voice.
    Stay humble, even with rude users. Use history: {history}."""

    if from_number == ADMIN_PHONE:
        return handle_admin_message(message)
    elif from_number == HOTEL_PHONE:
        return handle_hotel_message(message)
    else:
        return handle_customer_message(from_number, message, prompt, sentiment, timestamp)

def handle_customer_message(from_number, message, prompt, sentiment, timestamp):
    message_lower = message.lower()
    
    # Room availability
    if "available" in message_lower or "rooms" in message_lower:
        date = parse_date(message)
        rooms = get_available_rooms_for_date(date)
        response = f"Rooms available on {date}:\n" + "\n".join([f"{r[0]} - ₹{r[1]} ({r[2]} left)" for r in rooms])
    
    # Pricing details
    elif "how much" in message_lower or "price" in message_lower:
        room_type = "Deluxe" if "deluxe" in message_lower else "Suite" if "suite" in message_lower else None
        if room_type:
            response = f"The {room_type} is ₹{ROOMS[room_type]['price']}/night. Features: {ROOMS[room_type]['features']}."
        else:
            response = "We have Deluxe at ₹15000 and Suite at ₹25000 per night."
    
    # Hotel location
    elif "location" in message_lower or "where" in message_lower:
        response = f"We’re located at {HOTEL_LOCATION}. It’s a short walk from the Gateway of India!"
    
    # Room features and services
    elif "features" in message_lower or "services" in message_lower:
        if "room" in message_lower:
            room_type = "Deluxe" if "deluxe" in message_lower else "Suite"
            response = f"The {room_type} includes {ROOMS[room_type]['features']}."
        else:
            response = f"Our services include {HOTEL_SERVICES}."
    
    # Booking
    elif "book" in message_lower:
        room_type = "Deluxe" if "deluxe" in message_lower else "Suite"
        date = parse_date(message)
        if book_room(from_number, room_type, date):
            response = f"Your {room_type} booking for {date} is confirmed! Enjoy your stay."
        else:
            response = f"Sorry, no {room_type} available for {date}."
    
    # Price negotiation
    elif "offer" in message_lower or "cheaper" in message_lower:
        room_type = "Deluxe" if "deluxe" in message_lower else "Suite"
        user_offer = int(re.search(r'\d+', message).group(0)) if re.search(r'\d+', message) else 0
        current_price, negotiation_response = negotiate_price(room_type, user_offer, ROOMS[room_type]["price"], ROOMS[room_type]["min_price"])
        response = negotiation_response
    
    # Graceful exit
    elif "bye" in message_lower or "thanks" in message_lower:
        response = "Thank you for your time. Have a great day!"
    
    # Default AI response
    else:
        response, audio_url = get_retell_response(prompt, message)
        response = adjust_response(sentiment, response)
        if audio_url:
            response += f"\n[Voice]: {audio_url}"

    log_interaction(from_number, message, response, timestamp)
    return response

def handle_admin_message(message):
    if "bookings" in message.lower():
        bookings = get_all_bookings()
        return "Current Bookings:\n" + "\n".join([f"{b[0]}: {b[1]} on {b[2]} ({b[3]})" for b in bookings])
    elif "rooms" in message.lower():
        date = parse_date(message)
        rooms = get_available_rooms_for_date(date)
        return f"Rooms on {date}:\n" + "\n".join([f"{r[0]} - ₹{r[1]} ({r[2]} left)" for r in rooms])
    return "Admin commands: 'bookings', 'rooms'"

def handle_hotel_message(message):
    if "update" in message.lower():
        date = parse_date(message)
        rooms = get_available_rooms_for_date(date)
        return f"Room Status on {date}:\n" + "\n".join([f"{r[0]} - ₹{r[1]} ({r[2]} left)" for r in rooms])
    return "Hotel commands: 'update'"
    return adjust_response(sentiment, response)