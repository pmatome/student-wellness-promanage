import tkinter as tk
from tkinter import messagebox, ttk
import database
import clients
import services

def attempt_login():
    username = entry_user.get()
    password = database.hash_password(entry_pass.get())
    
    conn = database.create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        login_window.destroy()
        open_dashboard()
    else:
        messagebox.showerror("Access Denied", "Invalid Username or Password.")

def open_dashboard():
    root = tk.Tk()
    root.title("ProManage | Student Wellness Center")
    root.geometry("900x600")

    tk.Label(root, text="Student Wellness & Counseling Center", font=("Arial", 18, "bold"), bg="#003366", fg="white", pady=10).pack(fill="x")

    notebook = ttk.Notebook(root)
    notebook.pack(pady=10, padx=10, fill="both", expand=True)

    # TAB 1: Register Student
    tab_register = ttk.Frame(notebook)
    notebook.add(tab_register, text="Register Student")
    
    tk.Label(tab_register, text="Student ID:").place(x=50, y=50)
    ent_sid = tk.Entry(tab_register, width=30); ent_sid.place(x=150, y=50)
    
    tk.Label(tab_register, text="Full Name:").place(x=50, y=100)
    ent_name = tk.Entry(tab_register, width=30); ent_name.place(x=150, y=100)
    
    tk.Label(tab_register, text="Email:").place(x=50, y=150)
    ent_email = tk.Entry(tab_register, width=30); ent_email.place(x=150, y=150)
    
    tk.Label(tab_register, text="Department:").place(x=50, y=200)
    ent_dept = tk.Entry(tab_register, width=30); ent_dept.place(x=150, y=200)

    def submit_student():
        success, msg = clients.register_student(ent_sid.get(), ent_name.get(), ent_email.get(), ent_dept.get())
        if success:
            messagebox.showinfo("Success", msg)
            ent_sid.delete(0, tk.END); ent_name.delete(0, tk.END)
            ent_email.delete(0, tk.END); ent_dept.delete(0, tk.END)
        else:
            messagebox.showerror("Error", msg)

    tk.Button(tab_register, text="Register Student", command=submit_student, bg="#4CAF50", fg="white").place(x=150, y=250)

    # TAB 2: Log Session
    tab_session = ttk.Frame(notebook)
    notebook.add(tab_session, text="Log Counseling Session")

    tk.Label(tab_session, text="Student Name:").place(x=50, y=50)
    ent_s_name = tk.Entry(tab_session, width=30); ent_s_name.place(x=150, y=50)

    tk.Label(tab_session, text="Counselor:").place(x=50, y=100)
    ent_c_name = tk.Entry(tab_session, width=30); ent_c_name.place(x=150, y=100)

    tk.Label(tab_session, text="Service:").place(x=50, y=150)
    ent_service = tk.Entry(tab_session, width=30); ent_service.place(x=150, y=150)

    tk.Label(tab_session, text="Notes:").place(x=50, y=200)
    ent_notes = tk.Entry(tab_session, width=50); ent_notes.place(x=150, y=200)

    def submit_session():
        success, msg = services.log_session(ent_s_name.get(), ent_c_name.get(), ent_service.get(), ent_notes.get())
        if success:
            messagebox.showinfo("Success", msg)
            ent_s_name.delete(0, tk.END); ent_c_name.delete(0, tk.END)
            ent_service.delete(0, tk.END); ent_notes.delete(0, tk.END)
        else:
            messagebox.showerror("Error", msg)

    tk.Button(tab_session, text="Save Record", command=submit_session, bg="#2196F3", fg="white").place(x=150, y=250)

    # TAB 3: View Records
    tab_records = ttk.Frame(notebook)
    notebook.add(tab_records, text="View Reports")

    columns = ("Student", "Counselor", "Service", "Date", "Notes")
    tree = ttk.Treeview(tab_records, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    def load_records():
        for row in tree.get_children():
            tree.delete(row)
        records = services.get_all_records()
        for record in records:
            tree.insert("", tk.END, values=record)

    tk.Button(tab_records, text="Refresh Data", command=load_records).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    database.setup_database()

    login_window = tk.Tk()
    login_window.title("ProManage Login")
    login_window.geometry("300x200")

    tk.Label(login_window, text="Admin Login", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(login_window, text="Username").pack()
    entry_user = tk.Entry(login_window)
    entry_user.pack()

    tk.Label(login_window, text="Password").pack()
    entry_pass = tk.Entry(login_window, show="*")
    entry_pass.pack()

    tk.Button(login_window, text="Login", command=attempt_login, bg="#003366", fg="white").pack(pady=15)

    login_window.mainloop()
