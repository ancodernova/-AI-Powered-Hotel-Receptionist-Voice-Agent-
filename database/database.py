# database/database.py
import sqlite3
from config import DATABASE_NAME, ROOMS
from datetime import datetime, timedelta

def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rooms 
                 (id INTEGER PRIMARY KEY, type TEXT, price REAL, min_price REAL, features TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS availability 
                 (id INTEGER PRIMARY KEY, room_type TEXT, date TEXT, available INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS bookings 
                 (id INTEGER PRIMARY KEY, user_phone TEXT, room_type TEXT, checkin_date TEXT, status TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS interactions 
                 (id INTEGER PRIMARY KEY, user_phone TEXT, message TEXT, response TEXT, timestamp TEXT)''')
    
    # Insert room data
    c.execute("SELECT COUNT(*) FROM rooms")
    if c.fetchone()[0] == 0:
        for room_type, data in ROOMS.items():
            c.execute("INSERT INTO rooms (type, price, min_price, features) VALUES (?, ?, ?, ?)",
                      (room_type, data["price"], data["min_price"], data["features"]))
    
    # Initialize availability for next 30 days
    c.execute("SELECT COUNT(*) FROM availability")
    if c.fetchone()[0] == 0:
        for i in range(30):
            date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
            for room_type in ROOMS:
                c.execute("INSERT INTO availability (room_type, date, available) VALUES (?, ?, ?)",
                          (room_type, date, 5))  # 5 rooms available per type per day
    conn.commit()
    conn.close()

def get_available_rooms_for_date(date):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT r.type, r.price, a.available, r.features FROM rooms r JOIN availability a ON r.type = a.room_type WHERE a.date = ? AND a.available > 0", (date,))
    rooms = c.fetchall()
    conn.close()
    return rooms

def book_room(user_phone, room_type, checkin_date):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("UPDATE availability SET available = available - 1 WHERE room_type = ? AND date = ? AND available > 0", (room_type, checkin_date))
    if conn.total_changes > 0:
        c.execute("INSERT INTO bookings (user_phone, room_type, checkin_date, status) VALUES (?, ?, ?, 'Confirmed')", 
                  (user_phone, room_type, checkin_date))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def log_interaction(user_phone, message, response, timestamp):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO interactions (user_phone, message, response, timestamp) VALUES (?, ?, ?, ?)",
              (user_phone, message, response, timestamp))
    conn.commit()
    conn.close()

def get_user_history(user_phone):
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT message, response FROM interactions WHERE user_phone = ? ORDER BY timestamp DESC LIMIT 5", 
              (user_phone,))
    history = c.fetchall()
    conn.close()
    return history

def get_all_bookings():
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    c.execute("SELECT user_phone, room_type, checkin_date, status FROM bookings")
    bookings = c.fetchall()
    conn.close()
    return bookings