import csv
import database
from tkinter import filedialog

def get_all_records():
    """Fetches all counseling records from the database."""
    conn = database.create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT student_name, counselor_name, service_name, date, notes FROM session_records ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def export_to_csv():
    """Prompts the user to save a CSV file of all records."""
    records = get_all_records()
    
    if not records:
        return False, "No records available to export."
        
    # Open a save file dialog (Presentation Layer integration)
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
        title="Save Session Report As"
    )
    
    if not file_path:
        return False, "Export cancelled by user."
        
    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write Header
            writer.writerow(["Student Name", "Counselor", "Service", "Date & Time", "Notes"])
            # Write Data
            writer.writerows(records)
        return True, f"Report successfully saved to:\n{file_path}"
    except Exception as e:
        return False, f"Error saving file: {str(e)}"
