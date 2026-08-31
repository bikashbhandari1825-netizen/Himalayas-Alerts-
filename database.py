import sqlite3

DB_FILE = "nepal_suraksha.db"

def get_db_connection():
    try:
        # SQLite database फाइल स्वतः बनाउँछ
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row  # dictionary जस्तै डेटा लिनका लागि
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None