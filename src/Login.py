import tkinter as tk
from tkinter import messagebox
import json
import os

def load_user_credentials():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as file:
            return json.load(file)
    else:
        return {}

def validate_login():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Login Error", "Both username and password must be filled.")
        return

    users = load_user_credentials()

    if username in users and users[username] == password:
        messagebox.showinfo("Login Success", "Welcome, " + username)
        root.destroy()
        open_main_app()
    else:
        messagebox.showerror("Login Error", "Invalid Credentials.")

def open_main_app():
    import Main
    Main.run()

def create_user():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Registration Error", "Both username and password must be filled.")
        return

    users = load_user_credentials()

    if username in users:
        messagebox.showerror("Registration Error", "Username already exists.")
    else:
        users[username] = password

        with open('users.json', 'w') as file:
            json.dump(users, file)

        messagebox.showinfo("Registration Success", "User registered successfully!")

def run():
    global root, username_entry, password_entry
    root = tk.Tk()
    root.title("Login")

    root.geometry("500x500")
    root.config(bg='#FFFFFF')

    header_label = tk.Label(root, text="Welcome to the Weather App", font=("Helvetica", 18, "bold"), fg="#ffffff", bg="Light blue", pady=10)
    header_label.pack(fill="x", pady=20)

    tk.Label(root, text="Username", font=("Helvetica", 14), fg="Black", bg="#fff").pack(pady=5)
    username_entry = tk.Entry(root, font=("Helvetica", 14), bg="#fff", fg="#000", relief="solid", bd=2)
    username_entry.pack(pady=10, ipadx=5, ipady=5)

    tk.Label(root, text="Password", font=("Helvetica", 14), fg="Black", bg="#fff").pack(pady=5)
    password_entry = tk.Entry(root, font=("Helvetica", 14), show="*", bg="#fff", fg="#000", relief="solid", bd=2)
    password_entry.pack(pady=10, ipadx=5, ipady=5)

    login_button = tk.Button(root, text="Login", font=("Helvetica", 14, "bold"), bg="#32CD32", fg="white", relief="raised", bd=5, command=validate_login)
    login_button.pack(pady=20, fill="x", padx=50)

    register_button = tk.Button(root, text="Register", font=("Helvetica", 14, "bold"), bg="#1E90FF", fg="white", relief="raised", bd=5, command=create_user)
    register_button.pack(pady=10, fill="x", padx=50)

    exit_button = tk.Button(root, text="Exit", font=("Helvetica", 14, "bold"), bg="#FF4500", fg="white", relief="raised", bd=5, command=root.quit)
    exit_button.pack(pady=10, fill="x", padx=50)

    root.mainloop()
