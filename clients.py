import database

def register_student(student_id, name, email, department):
    if not student_id or not name:
        return False, "Student ID and Name are required."
    
    conn = database.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO students (student_id, name, email, department)
            VALUES (?, ?, ?, ?)
        ''', (student_id, name, email, department))
        conn.commit()
        return True, "Student registered successfully."
    except Exception:
        return False, "Error: Student ID might already exist."
    finally:
        conn.close()
