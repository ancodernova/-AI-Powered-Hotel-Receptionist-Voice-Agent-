# app.py - Main Flask Application
from flask import Flask
import threading
import os
from services.twilio_service import start_twilio_listener
from database.database import init_db
from config import configure_logging
import logging

logger = configure_logging()
app = Flask(__name__)

@app.route('/')
def home():
    return "Hotel Receptionist Bot is running!"

if __name__ == '__main__':
    init_db()
    twilio_thread = threading.Thread(target=start_twilio_listener)
    twilio_thread.daemon = True
    twilio_thread.start()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)