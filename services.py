import database
import datetime

def log_session(student_name, counselor_name, service_name, notes):
    if not student_name or not counselor_name or not service_name:
        return False, "All fields are required."
        
    conn = database.create_connection()
    cursor = conn.cursor()
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    cursor.execute('''
        INSERT INTO session_records (student_name, counselor_name, service_name, date, notes)
        VALUES (?, ?, ?, ?, ?)
    ''', (student_name, counselor_name, service_name, date, notes))
    
    conn.commit()
    conn.close()
    return True, "Session recorded successfully."

def get_all_records():
    conn = database.create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT student_name, counselor_name, service_name, date, notes FROM session_records")
    rows = cursor.fetchall()
    conn.close()
    return rows
