import tkinter as tk
from tkinter import messagebox, ttk
import database
import clients
import services
import reports

# --- LOGIN WINDOW ---
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
    root.geometry("1000x700")
    
    # Apply a modern theme
    style = ttk.Style()
    style.theme_use('clam') # 'clam' looks much better than the default
    
    # Customizing the Notebook (Tabs)
    style.configure("TNotebook", background="#f0f0f0", borderwidth=0)
    style.configure("TNotebook.Tab", padding=[20, 10], font=('Arial', 10, 'bold'))
    style.map("TNotebook.Tab", background=[("selected", "#003366")], foreground=[("selected", "white")])

    # Header
    header_frame = tk.Frame(root, bg="#003366", pady=15)
    header_frame.pack(fill="x")
    tk.Label(header_frame, text="Student Wellness & Counseling Center", font=("Arial", 20, "bold"), bg="#003366", fg="white").pack()

    # Main Container
    notebook = ttk.Notebook(root)
    notebook.pack(pady=15, padx=20, fill="both", expand=True)

    # ==========================================
    # TAB 1: Register Student
    # ==========================================
    tab_register = ttk.Frame(notebook, padding=20)
    notebook.add(tab_register, text="Register Student")
    
    # Form Frame
    form_frame = tk.Frame(tab_register)
    form_frame.pack(pady=20)

    tk.Label(form_frame, text="Student ID:", font=("Arial", 11)).grid(row=0, column=0, sticky="e", pady=5, padx=5)
    ent_sid = ttk.Entry(form_frame, width=30, font=("Arial", 11)); ent_sid.grid(row=0, column=1, pady=5)
    
    tk.Label(form_frame, text="Full Name:", font=("Arial", 11)).grid(row=1, column=0, sticky="e", pady=5, padx=5)
    ent_name = ttk.Entry(form_frame, width=30, font=("Arial", 11)); ent_name.grid(row=1, column=1, pady=5)
    
    tk.Label(form_frame, text="Email:", font=("Arial", 11)).grid(row=2, column=0, sticky="e", pady=5, padx=5)
    ent_email = ttk.Entry(form_frame, width=30, font=("Arial", 11)); ent_email.grid(row=2, column=1, pady=5)
    
    tk.Label(form_frame, text="Department:", font=("Arial", 11)).grid(row=3, column=0, sticky="e", pady=5, padx=5)
    ent_dept = ttk.Entry(form_frame, width=30, font=("Arial", 11)); ent_dept.grid(row=3, column=1, pady=5)

    def submit_student():
        success, msg = clients.register_student(ent_sid.get(), ent_name.get(), ent_email.get(), ent_dept.get())
        if success:
            messagebox.showinfo("Success", msg)
            ent_sid.delete(0, tk.END); ent_name.delete(0, tk.END)
            ent_email.delete(0, tk.END); ent_dept.delete(0, tk.END)
        else:
            messagebox.showerror("Error", msg)

    ttk.Button(tab_register, text="Register Student", command=submit_student).pack(pady=10)

    # ==========================================
    # TAB 2: Log Counseling Session
    # ==========================================
    tab_session = ttk.Frame(notebook, padding=20)
    notebook.add(tab_session, text="Log Counseling Session")

    session_frame = tk.Frame(tab_session)
    session_frame.pack(pady=20)

    tk.Label(session_frame, text="Student Name:", font=("Arial", 11)).grid(row=0, column=0, sticky="e", pady=5, padx=5)
    ent_s_name = ttk.Entry(session_frame, width=30, font=("Arial", 11)); ent_s_name.grid(row=0, column=1, pady=5)

    tk.Label(session_frame, text="Counselor:", font=("Arial", 11)).grid(row=1, column=0, sticky="e", pady=5, padx=5)
    # Combobox for Counselors (Professions)
    counselor_var = tk.StringVar()
    combo_counselor = ttk.Combobox(session_frame, textvariable=counselor_var, width=28, state="readonly", font=("Arial", 11))
    combo_counselor.grid(row=1, column=1, pady=5)
    
    # Fetch counselors from database to populate dropdown
    conn = database.create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM counselors")
    counselors = [row[0] for row in cursor.fetchall()]
    conn.close()
    combo_counselor['values'] = counselors

    tk.Label(session_frame, text="Service:", font=("Arial", 11)).grid(row=2, column=0, sticky="e", pady=5, padx=5)
    # Combobox for Services
    service_var = tk.StringVar()
    combo_service = ttk.Combobox(session_frame, textvariable=service_var, width=28, state="readonly", font=("Arial", 11))
    combo_service.grid(row=2, column=1, pady=5)
    
    conn = database.create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT service_name FROM services")
    services_list = [row[0] for row in cursor.fetchall()]
    conn.close()
    combo_service['values'] = services_list

    tk.Label(session_frame, text="Notes:", font=("Arial", 11)).grid(row=3, column=0, sticky="ne", pady=5, padx=5)
    ent_notes = tk.Text(session_frame, width=30, height=4, font=("Arial", 11))
    ent_notes.grid(row=3, column=1, pady=5)

    def submit_session():
        success, msg = services.log_session(
            ent_s_name.get(), 
            counselor_var.get(), 
            service_var.get(), 
            ent_notes.get("1.0", tk.END).strip()
        )
        if success:
            messagebox.showinfo("Success", msg)
            ent_s_name.delete(0, tk.END)
            counselor_var.set(''); service_var.set('')
            ent_notes.delete("1.0", tk.END)
        else:
            messagebox.showerror("Error", msg)

    ttk.Button(tab_session, text="Save Record", command=submit_session).pack(pady=10)

    # ==========================================
    # TAB 3: View Reports
    # ==========================================
    tab_records = ttk.Frame(notebook, padding=20)
    notebook.add(tab_records, text="View Reports")

    # Treeview (Table)
    columns = ("Student", "Counselor", "Service", "Date", "Notes")
    tree = ttk.Treeview(tab_records, columns=columns, show="headings", style="Treeview")
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")
    
    # Scrollbar for the table
    scrollbar = ttk.Scrollbar(tab_records, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    
    tree.pack(side=tk.LEFT, fill="both", expand=True)
    scrollbar.pack(side=tk.RIGHT, fill="y")

    def load_records():
        # Clear existing data in table
        for row in tree.get_children():
            tree.delete(row)
        # Fetch new data
        records = reports.get_all_records()
        for record in records:
            tree.insert("", tk.END, values=record)

    def export_data():
        success, msg = reports.export_to_csv()
        if success:
            messagebox.showinfo("Export Successful", msg)
        else:
            if msg != "Export cancelled by user.":
                messagebox.showerror("Export Failed", msg)

    # Buttons below the table
    btn_frame = tk.Frame(tab_records)
    btn_frame.pack(side=tk.BOTTOM, fill="x", pady=10)

    ttk.Button(btn_frame, text="Refresh Data", command=load_records).pack(side=tk.LEFT, padx=10)
    ttk.Button(btn_frame, text="Export to CSV", command=export_data).pack(side=tk.LEFT, padx=10)

    root.mainloop()

# --- START APP ---
if __name__ == "__main__":
    database.setup_database() # Ensure DB is ready

    # Login Window UI Setup
    login_window = tk.Tk()
    login_window.title("ProManage Login")
    login_window.geometry("350x250")
    login_window.configure(bg="#f0f0f0")

    login_frame = tk.Frame(login_window, bg="#f0f0f0", padx=20, pady=20)
    login_frame.pack(expand=True)

    tk.Label(login_frame, text="Admin Login", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#003366").pack(pady=(0, 15))
    
    tk.Label(login_frame, text="Username", bg="#f0f0f0").pack(anchor="w")
    entry_user = ttk.Entry(login_frame, width=30)
    entry_user.pack(pady=(0, 10))

    tk.Label(login_frame, text="Password", bg="#f0f0f0").pack(anchor="w")
    entry_pass = ttk.Entry(login_frame, show="*", width=30)
    entry_pass.pack(pady=(0, 15))

    ttk.Button(login_frame, text="Login", command=attempt_login).pack(fill="x")

    login_window.mainloop()
