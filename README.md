# AI-Powered Hotel Receptionist Voice Agent

## Overview

This project is an **AI-powered real-time voice agent** acting as a hotel receptionist for **Taj Mahal Palace Mumbai**, accessible via **WhatsApp**. It leverages **Groq API** for ultra-fast inference, **Retell AI** for voice-based responses, and **Twilio** for WhatsApp messaging. Additionally, it integrates **LLaMA** for intelligent recommendations, **SQLite** for data management, and **Flask** as the backend framework.

The system is designed to handle customer queries, room bookings, admin tasks, and hotel staff updates. With sentiment analysis, the agent ensures polite and professional interactions, even with challenging customers.

---

## 🔥 Features

### ✅ **Core Features**

- **Room Availability Queries** – Retrieves available rooms for specific dates.
- **Pricing Information** – Provides room costs based on the type and season.
- **Hotel Location & Directions** – Shares the hotel's address and nearby landmarks.
- **Room & Service Details** – Describes amenities like Wi-Fi, TV, dining, and parking.
- **Politeness & Sentiment Awareness** – Stays professional, even with rude customers.
- **Graceful Call Ending** – Concludes conversations appropriately when users lose interest.
- **Room Booking via WhatsApp** – Captures user details and confirms bookings automatically.
- **Price Negotiation** – Allows limited haggling within predefined price boundaries.
- **AI-Powered Room Suggestions** – Uses **LLaMA** to recommend the best room based on user needs.
- **Ultra-Fast AI Responses** – Powered by **Groq API** for responses in under **2 seconds**.

---

## 🛠️ **Technical Highlights**

- **WhatsApp Integration:** Real-time messaging using **Twilio**.
- **Voice-Based Responses:** Generates **Retell AI** audio messages, sending them as WhatsApp voice notes.
- **Intelligent Date Parsing:** Uses `dateutil` to understand flexible date inputs (e.g., "next weekend").
- **Sentiment Analysis:** Responds empathetically based on the user’s tone.
- **Database Management:** Stores room availability, bookings, and chat history in **SQLite**.
- **Groq API Integration:** Utilizes Llama3-70B for **fast and efficient** natural language processing.

---

## 📂 **Project Structure**

```
├── app.py                 # Flask backend
├── config.py              # API keys, logging, hotel data
├── database/
│   ├── database.py        # SQLite logic
│   └── __init__.py        # Package init
├── services/
│   ├── twilio_service.py  # Twilio WhatsApp integration
│   ├── groq_service.py    # Groq API integration
│   ├── retell_service.py  # Retell AI integration
│   ├── llama_service.py   # LLaMA integration
│   ├── sentiment_service.py # Sentiment analysis
│   ├── hotel_service.py   # Hotel logic
│   └── __init__.py        # Package init
├── README.md              # This file
└── requirements.txt       # Dependencies
```

---

## 🔧 **Installation & Setup**

### 2️⃣ **Create a Virtual Environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

### 3️⃣ **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 4️⃣ **Set Up Environment Variables**

Create a `.env` file and add your credentials:

```
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+1234567890

GROQ_API_KEY=your_groq_api_key
RETELL_API_KEY=your_retell_api_key
LLAMA_API_KEY=your_llama_api_key

```

### 5️⃣ **Initialize the Database**

```bash
python database/database.py
```

### 6️⃣ **Run the Application**

```bash
python app.py
```

Your Flask backend will start running on `http://localhost:5000`.

---

## 📝 **Usage Guide**

### ✅ **WhatsApp Commands**

- 🏨 **Check Room Availability:**
  - `"What rooms are available next weekend?"`
- 💰 **Get Pricing Information:**
  - `"How much is a Deluxe room?"`
- 📍 **Get Hotel Location:**
  - `"Where is the hotel located?"`
- 📜 **List Room Features:**
  - `"Does the room have Wi-Fi and TV?"`
- 🎙️ **Voice Interaction via WhatsApp:**
  - Users can receive **Retell AI** voice responses.

### 🤝 **Booking & Negotiation**

- 🛏️ **Book a Room:**
  - `"Book a suite for 2 nights starting Friday."`
- 💲 **Price Negotiation:**
  - `"Can I get a discount on a Deluxe room?"`

---

## 📊 **How It Works**

### ✅ **Step 1: User Sends a Message on WhatsApp**

The agent receives messages via Twilio’s **WhatsApp API**.

### ⚡ **Step 2: AI Processes the Request**

- **Natural Language Understanding**: **Groq API** quickly processes queries.
- **Date & Intent Extraction**: Uses `dateutil` and NLP techniques to understand user intent.
- **Sentiment Analysis**: **sentiment_service.py** ensures polite responses.

### 🏨 **Step 3: Fetch Data from SQLite**

- Retrieves **room availability**, **prices**, or **booking status**.

### 🔊 **Step 4: Response via WhatsApp**

- If **text-based**, Twilio sends a reply.
- If **voice-based**, Retell AI generates an audio response and sends it as a **WhatsApp voice note**.

---

## 🎯 **Future Improvements**

- 🤖 **Multilingual Support** – Add language detection & translation.
- 📊 **Analytics Dashboard** – Monitor booking trends & customer queries.
- 🛎️ **Integration with Hotel APIs** – Sync real-time room availability with hotel databases.
