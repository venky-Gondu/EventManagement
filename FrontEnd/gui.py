import tkinter as tk
from tkinter import messagebox
import requests

BASE_URL = "http://127.0.0.1:5000"  # Flask server URL

class EventManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Intra-School Event Management")
        self.root.geometry("400x500")
        self.root.configure(bg="#f0f8ff")  # Light blue background

        self.token = None  # Store JWT Token
        self.user_role = None  # Store User Role
        self.user_id = None  # Store User ID

        self.login_page()

    def center_widget(self, widget):
        """Helper function to center-align widgets"""
        widget.pack(pady=10)

    def style_button(self, button):
        """Helper function to style buttons"""
        button.configure(
            width=20,
            height=2,
            bg="#4CAF50",  # Green background
            fg="white",  # White text
            font=("Arial", 12, "bold"),
            relief="raised",
            bd=3
        )

    def login_page(self):
        """Login Page UI"""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Login", font=("Arial", 16, "bold"), bg="#f0f8ff").pack(pady=20)

        tk.Label(self.root, text="Username:", bg="#f0f8ff").pack()
        self.username_entry = tk.Entry(self.root)
        self.center_widget(self.username_entry)

        tk.Label(self.root, text="Password:", bg="#f0f8ff").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.center_widget(self.password_entry)

        login_button = tk.Button(self.root, text="Login", command=self.login)
        self.style_button(login_button)
        self.center_widget(login_button)

    def login(self):
        """Handle User Login"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required")
            return

        with requests.Session() as session:
            "username": username,
            "password": password
        })

        if response.status_code == 200:
            data = response.json()
            self.user_role = data.get("role")
            self.user_id = data.get("user_id")

            messagebox.showinfo("Success", "Login Successful!")
            self.dashboard()  # Open dashboard based on role
        else:
            messagebox.showerror("Error", response.json().get("error", "Login failed"))
    def dashboard(self):
        """Dashboard UI based on user role"""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"Dashboard - {self.user_role}", font=("Arial", 16, "bold"), bg="#f0f8ff").pack(pady=20)

        if self.user_role == "admin":
            self.create_dashboard_button("Create Event", self.create_event)
            self.create_dashboard_button("Manage Events", self.manage_events)
            self.create_dashboard_button("Assign Students", self.assign_students)

        elif self.user_role == "Teacher":
            self.create_dashboard_button("Manage Events", self.manage_events)
            self.create_dashboard_button("Assign Students", self.assign_students)

        elif self.user_role == "Student":
            self.create_dashboard_button("View My Events", self.view_my_events)
            self.create_dashboard_button("Upload File", self.upload_file)

        # Add the logout button for all roles
        logout_button = tk.Button(self.root, text="Logout", command=self.logout)
        self.style_button(logout_button)
        self.center_widget(logout_button)

    def create_dashboard_button(self, text, command):
        """Helper function to create styled dashboard buttons"""
        button = tk.Button(self.root, text=text, command=command)
        self.style_button(button)
        self.center_widget(button)

    def create_event(self):
        """Event Creation UI"""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Create Event", font=("Arial", 16, "bold"), bg="#f0f8ff").pack(pady=20)

        tk.Label(self.root, text="Event ID:", bg="#f0f8ff").pack()
        self.event_id_entry = tk.Entry(self.root)
        self.center_widget(self.event_id_entry)

        tk.Label(self.root, text="Event Name:", bg="#f0f8ff").pack()
        self.event_name_entry = tk.Entry(self.root)
        self.center_widget(self.event_name_entry)

        tk.Label(self.root, text="Event Date (YYYY-MM-DD):", bg="#f0f8ff").pack()
        self.event_date_entry = tk.Entry(self.root)
        self.center_widget(self.event_date_entry)

        tk.Label(self.root, text="Start Time (HH:MM:SS):", bg="#f0f8ff").pack()
        self.start_time_entry = tk.Entry(self.root)
        self.center_widget(self.start_time_entry)

        tk.Label(self.root, text="End Time (HH:MM:SS):", bg="#f0f8ff").pack()
        self.end_time_entry = tk.Entry(self.root)
        self.center_widget(self.end_time_entry)

        tk.Label(self.root, text="Venue:", bg="#f0f8ff").pack()
        self.event_venue_entry = tk.Entry(self.root)
        self.center_widget(self.event_venue_entry)

        create_button = tk.Button(self.root, text="Create", command=self.submit_event)
        self.style_button(create_button)
        self.center_widget(create_button)

        back_button = tk.Button(self.root, text="Back", command=self.dashboard)
        self.style_button(back_button)
        self.center_widget(back_button)

    def submit_event(self):
        """Send event data to the backend"""
        event_id = self.event_id_entry.get()
        if not event_id:
            messagebox.showerror("Error", "Event ID is required")
            return
        event_name = self.event_name_entry.get()
        event_date = self.event_date_entry.get()
        event_start_time = self.start_time_entry.get()
        event_end_time = self.end_time_entry.get()
        event_venue = self.event_venue_entry.get()

        if not all([event_id,event_name, event_date, event_start_time, event_end_time, event_venue]):
            messagebox.showerror("Error", "All fields are required")
            return

        response = requests.post(f"{BASE_URL}/event/create_event", json={
            "event_id": event_id,
            "event_name": event_name,
            "event_date": event_date,
            "event_start_time": event_start_time,
            "event_end_time": event_end_time,
            "event_venue": event_venue
        })

        if response.status_code == 201:
            messagebox.showinfo("Success", "Event created successfully!")
            self.dashboard()
        else:
            messagebox.showerror("Error", response.json().get("error", "Event creation failed"))

    def manage_events(self):
        """Manage events UI"""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Manage Events", font=("Arial", 16, "bold"), bg="#f0f8ff").pack(pady=20)

        view_events_button = tk.Button(self.root, text="View Events", command=self.view_events)
        self.style_button(view_events_button)
        self.center_widget(view_events_button)

        back_button = tk.Button(self.root, text="Back", command=self.dashboard)
        self.style_button(back_button)
        self.center_widget(back_button)

    def assign_students(self):
        """Placeholder for assigning students"""
        messagebox.showinfo("Feature", "Assign Students functionality coming soon!")

    def view_my_events(self):
        """View events for the logged-in student"""
        with requests.Session() as session:
            # Send the request to the backend
            response = session.get(f"{BASE_URL}/event/list_events", cookies=session.cookies)

            if response.status_code == 200:
                events = response.json().get("events", [])
                # Display events in the GUI
                self.display_events(events)
            else:
                messagebox.showerror("Error", response.json().get("error", "Failed to fetch events"))

    def upload_file(self):
        """Placeholder for file upload"""
        messagebox.showinfo("Feature", "Upload File functionality coming soon!")
    def logout(self):
        """Handle User Logout"""
       # get request
        response = requests.post(f"{BASE_URL}/auth/logout", headers={"Authorization": f"Bearer {self.token}"})
        if response.status_code == 200:
            messagebox.showinfo("Success", "You have been logged out successfully!")
            self.token = None  # Clear the token
            self.user_role = None  # Clear the user role
            self.user_id = None  # Clear the user ID
            self.login_page()  # Redirect to the login page
        else:
            messagebox.showerror("Error", response.json().get("error", "Logout failed"))

if __name__ == "__main__":
    root = tk.Tk()
    app = EventManagementApp(root)
    root.mainloop()
