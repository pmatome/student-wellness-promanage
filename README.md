# ProManage | Student Wellness & Counseling Center 

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-orange)
![License](https://img.shields.io/badge/License-MIT-purple)

A robust, desktop-based Client Management System built specifically for a University Student Wellness and Counseling Center. Originally designed as a universal architecture, this application has been tailored to handle confidential student sessions, counselor assignments, and secure record-keeping.

##  System Architecture
This application strictly follows a multi-tier architecture to ensure separation of concerns, security, and scalability:

1. **Presentation Layer (`main.py`):** Built with Python's `Tkinter` and `ttk`. Provides a modern, tabbed interface (Login, Dashboard, Registrations, Settings).
2. **Application Logic Layer (`clients.py`, `services.py`, `reports.py`):** Handles input validation, business rules, and routing. 
3. **Data Access Layer:** Uses parameterized SQLite3 queries to prevent SQL injection.
4. **Database Layer (`promanage.db`):** A local SQLite file securely storing users, students, counselors, services, and session records.

##  Key Features
*   **Secure Authentication:** Admin login with SHA-256 password hashing.
*   **Client Management:** Register new students with unique IDs, search for them, and manage their profiles.
*   **Session Logging:** Log counseling sessions using dynamic dropdown menus (populated directly from the database).
*   **Reporting & Export:** View a live, scrollable dashboard of all past sessions and export the data directly to a `.csv` file for Excel.
*   **Dynamic Settings:** Add new Counselors and Services on the fly without touching the database code.
*   **Security First:** Includes a `.gitignore` to ensure the local database (`*.db`) is never pushed to version control.

##  How to Run Locally

### Prerequisites
Make sure you have Python installed on your computer. You can download it from [python.org](https://www.python.org/downloads/). *(Ensure "Add Python to PATH" is checked during installation).*

### Installation Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

   cd YOUR_REPO_NAME

   python main.py

 Default Login
Username: admin

Password: admin123

 Project Structure
text
├─ main.py           # Presentation Layer (GUI, Tabs, Login)
├─ database.py       # Database setup, connection, and password hashing
├─ clients.py        # Logic for registering and deleting students
├─ services.py       # Logic for logging counseling sessions
├─ reports.py        # Logic for fetching and exporting data to CSV
├─ .gitignore        # Prevents database and cache files from being uploaded
└─ README.md         # Project documentation




