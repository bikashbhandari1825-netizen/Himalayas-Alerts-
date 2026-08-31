import sqlite3

def setup_database():
    conn = sqlite3.connect("nepal_suraksha.db")
    cursor = conn.cursor()

    # १. Users टेबल बनाउने
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT UNIQUE NOT NULL,
        role TEXT DEFAULT 'CITIZEN',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # २. Incidents (रिपोर्टहरू) टेबल बनाउने
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        severity TEXT DEFAULT 'Moderate',
        status TEXT DEFAULT 'Pending',
        description TEXT,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        reported_by INTEGER,
        verified_by INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (reported_by) REFERENCES users (id)
    );
    """)

    # ३. टेस्ट युजर (Test User) थप्ने
    cursor.execute("""
    INSERT OR IGNORE INTO users (id, name, phone, role) 
    VALUES (1, 'Ramesh Thapa', '9841000000', 'CITIZEN');
    """)

    conn.commit()
    conn.close()
    print("🚀 SQLite Database and Tables successfully created!")

if __name__ == "__main__":
    setup_database()