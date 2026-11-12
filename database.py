import sqlite3
import hashlib

DB_NAME = 'promanage.db'

def create_connection():
    """Establishes a connection to the SQLite database."""
    return sqlite3.connect(DB_NAME)

def hash_password(password):
    """Converts a plain text password into a secure SHA-256 hash."""
    return hashlib.sha256(password.encode()).hexdigest()

def setup_database():
    """Creates tables if they don't exist and inserts default data."""
    conn = create_connection()
    cursor = conn.cursor()
    
    # 1. Users Table (For Security & Login)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    
    # 2. Students Table (Clients)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            email TEXT,
            department TEXT
        )
    ''')
    
    # 3. Counselors Table (Professions)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS counselors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')
    
    # 4. Services Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_name TEXT UNIQUE NOT NULL
        )
    ''')
    
    # 5. Session Records
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS session_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            counselor_name TEXT,
            service_name TEXT,
            date TEXT,
            notes TEXT
        )
    ''')
    
    # Insert Default Admin
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                       ('admin', hash_password('admin123'), 'Administrator'))
    except sqlite3.IntegrityError:
        pass # Ignore if admin already exists
        
    # Insert Default Counselors
    try:
        cursor.execute("INSERT INTO counselors (name) VALUES ('Dr. Smith')")
        cursor.execute("INSERT INTO counselors (name) VALUES ('Ms. Johnson')")
    except sqlite3.IntegrityError:
        pass
        
    # Insert Default Services
    try:
        cursor.execute("INSERT INTO services (service_name) VALUES ('Stress Management')")
        cursor.execute("INSERT INTO services (service_name) VALUES ('Career Counseling')")
        cursor.execute("INSERT INTO services (service_name) VALUES ('Academic Support')")
    except sqlite3.IntegrityError:
        pass
        
    conn.commit()
    conn.close()
