from supabase import create_client #importance 1
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import os #importance 4 good practice to import os for environment variables
from dotenv import load_dotenv #importance 4 to load environment variables from .env file


load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

database = create_client(SUPABASE_URL, SUPABASE_API_KEY)


class UI(object):
    def __init__(self):
        self.active_userid = None
        self.root = tk.Tk()
        self.login_screen = tk.Frame(self.root)
        self.main_screen = tk.Frame(self.root)
        self.root.title("Registration System Login")
        self.root.geometry("400x300")

    def login(self):
        username = self.username_entry.get()
        response = database.table("teachers").select("password").eq("name", username).execute()
        if not response.data:
            messagebox.showerror("Error", "Invalid username!")
            return
        else:
            CORRECT_PASSWORD = response.data[0]['password']
        password = self.password_entry.get()
        if password == CORRECT_PASSWORD:
            response = database.table("teachers").select("id").eq("name", username).execute()
            self.active_userid = response.data[0]['id']
            self.login_screen.pack_forget()
            messagebox.showinfo("Success", "Login successful!")
            self.build_main_screen()
        else:
            messagebox.showerror("Error", "Invalid password")

    def build_login_screen(self):
        self.login_screen.pack(fill="both", expand=True)

        tk.Label(self.login_screen, text="Username").pack(pady=5)
        self.username_entry = tk.Entry(self.login_screen)
        self.username_entry.pack(pady=5)

        tk.Label(self.login_screen, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(self.login_screen, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.login_screen, text="Login", command=self.login).pack(pady=20)

    def get_classes(self):
        response = database.table("classes").select("class_name").eq("teacher_id", self.active_userid).execute()
        if not response.data:
            return []
        return [c['class_name'] for c in response.data]

    def load_students(self, event=None):
        selected_class = self.selected_class.get()
        if not selected_class:
            return

        # Get the class_id for the selected class name
        response = database.table("classes").select("id").eq("class_name", selected_class).execute()
        if not response.data:
            return
        class_id = response.data[0]['id']

        # Fetch students in that class
        response = database.table("students").select("barcode", "student_name", "email").eq("class_id", class_id).execute()

        # Clear existing rows
        for row in self.student_table.get_children():
            self.student_table.delete(row)

        # Populate table — barcode maps to "Student ID" column
        for student in response.data:
            self.student_table.insert("", tk.END, values=(
                student['barcode'],
                student['student_name'],
                student['email']
            ))

    def build_main_screen(self):
        self.main_screen.pack(fill="both", expand=True)

        tk.Label(self.main_screen, text="Class Dashboard", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.main_screen, text="Select Class").pack()

        classes = self.get_classes()
        self.selected_class = tk.StringVar()

        self.class_dropdown = ttk.Combobox(
            self.main_screen,
            textvariable=self.selected_class,
            values=classes,
            state="readonly"
        )
        self.class_dropdown.pack(pady=10)

        # Table — "Student ID" header maps to barcode column
        self.student_table = ttk.Treeview(
            self.main_screen,
            columns=("Student ID", "Name", "Email"),
            show="headings",
            height=10
        )

        self.student_table.heading("Student ID", text="Student ID")
        self.student_table.heading("Name", text="Name")
        self.student_table.heading("Email", text="Email")

        self.student_table.column("Student ID", width=100)
        self.student_table.column("Name", width=150)
        self.student_table.column("Email", width=250)

        self.student_table.pack(pady=10)

        self.class_dropdown.bind("<<ComboboxSelected>>", self.load_students)

    def run(self):
        self.build_login_screen()
        self.root.mainloop()


ui = UI()
ui.run()