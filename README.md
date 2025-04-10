# 🏫 Intra-School Event Management System

A role-based desktop application to streamline the creation, participation, and management of school-level events. Built using Python Flask for the backend and Tkinter for the desktop-based user interface.

## ✨ Features

- 🔐 Role-Based Login for Admin, Teacher, and Student
- 🗓️ Event Creation and Management (Admin/Teacher)
- 🎯 Assign Students to Events (Admin/Teacher)
- 👥 View My Events (Student)
- 📤 File Upload (Student)
- 📡 Backend integration using Flask and PostgreSQL
- 🖥️ Desktop GUI built using Tkinter

## 📁 Project Structure

project/  
├── backend/  
│   ├── app.py                 # Main Flask app  
│   ├── auth.py                # Authentication logic  
│   ├── event.py               # Event management routes  
│   ├── db_config.py           # PostgreSQL connection setup  
│   └── ...  
├── frontend/  
│   └── gui.py                 # Tkinter desktop interface  
├── requirements.txt  
└── README.md  

## 👤 User Roles & Capabilities

| Role     | Capabilities                               |
|----------|--------------------------------------------|
| Admin    | Create Events, Manage Events, Assign Users |
| Teacher  | Manage Events, Assign Students             |
| Student  | View Events, Upload Files                  |

## 🚀 Getting Started

### 1️⃣ Backend Setup (Flask + PostgreSQL)

- Create virtual environment & install dependencies:

  pip install -r requirements.txt

- Update database credentials in db_config.py

- Start the Flask server:

  python app.py

The Flask app will run at http://127.0.0.1:5000

### 2️⃣ Frontend Setup (Tkinter GUI)

- Ensure Python Tkinter is installed (usually comes preinstalled with Python)
- Run the desktop app:

  python gui.py

## 🔗 API Endpoints (Flask)

| Method | Endpoint                   | Description                          |
|--------|----------------------------|--------------------------------------|
| POST   | /auth/login                | Login user                           |
| POST   | /auth/register/student     | Register a new student               |
| POST   | /auth/register/teacher     | Register a new teacher               |
| POST   | /auth/register/admin       | Register a new admin                 |
| POST   | /event/create_event        | Create a new event (Admin/Teacher)   |
| GET    | /event/list                | List all events                      |
| POST   | /event/assign              | Assign a student to an event         |

## ✅ Prerequisites

- Python 3.8+
- PostgreSQL
- Flask
- requests (Python library)
- Tkinter (usually comes with Python)

## 📷 Screenshots

You can add screenshots here (e.g., .png files):

- Login Page  
- Admin Dashboard  
- Student Dashboard  
- Event Creation Form

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to improve.

## 📃 License

This project is licensed under the MIT License.
