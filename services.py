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

    import csv
from tkinter import filedialog

def export_records_to_csv():
    # Get all records from the database
    records = get_all_records()
    
    if not records:
        return False, "No records to export."
        
    # Ask the user where to save the file
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        title="Save Report As"
    )
    
    if not file_path:
        return False, "Export cancelled."
        
    try:
        # Write data to CSV
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write the header row
            writer.writerow(["Student Name", "Counselor", "Service", "Date", "Notes"])
            # Write the data rows
            writer.writerows(records)
        return True, f"Report saved successfully to:\n{file_path}"
    except Exception as e:
        return False, f"Error saving file: {str(e)}"
    cursor = conn.cursor()
    cursor.execute("SELECT student_name, counselor_name, service_name, date, notes FROM session_records")
    rows = cursor.fetchall()
    conn.close()
    return rows
