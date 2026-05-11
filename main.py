from supabase import create_client
import os
from dotenv import load_dotenv
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

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
        # Username label
        self.login_screen.pack(fill="both", expand=True)
        self.username_label = tk.Label(self.login_screen, text="Username")
        self.username_label.pack(pady=5)

        # Username input
        self.username_entry = tk.Entry(self.login_screen)
        self.username_entry.pack(pady=5)

        # Password label
        self.password_label = tk.Label(self.login_screen, text="Password")
        self.password_label.pack(pady=5)

        # Password input
        self.password_entry = tk.Entry(self.login_screen, show="*")
        self.password_entry.pack(pady=5)

        # Login button
        login_button = tk.Button(self.login_screen, text="Login", command=self.login)
        login_button.pack(pady=20)
    
    def get_classes(self):
        # GEt the list of all the classes that the teacher is teaching
        response = database.table("classes").select("class_name").eq("teacher_id", self.active_userid).execute()
        if not response.data:
            return []
        return [class_['class_name'] for class_ in response.data]

    def build_main_screen(self):
        self.main_screen.pack(fill="both", expand=True)
         # ---------------- TITLE ----------------
        self.title = tk.Label(
            self.main_screen,
            text="Class Dashboard",
            font=("Arial", 16)
        )
        self.title.pack(pady=10)

        # ---------------- CLASS DROPDOWN ----------------
        class_label = tk.Label(
            self.main_screen,
            text="Select Class"
        )
        class_label.pack()

        # Example class list
        classes = self.get_classes()
        self.selected_class = tk.StringVar()

        self.class_dropdown = ttk.Combobox(
            self.main_screen,
            textvariable=self.selected_class,
            values=classes,
            state="readonly"
        )
        self.class_dropdown.pack(pady=10)
        

    def run(self):
        self.build_login_screen()
        self.root.mainloop()

ui = UI()
ui.run()


def load_students(self, event):

    selected_class = self.selected_class.get()

    # Clear existing rows
    for row in self.student_table.get_children():
        self.student_table.delete(row)

    # Add new rows
    students = self.class_students[selected_class]

    for student in students:
        self.student_table.insert("", tk.END, values=student)