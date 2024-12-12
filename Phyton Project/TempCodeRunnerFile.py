import tkinter as tk
from tkinter import messagebox
import subprocess
import mysql.connector
from hashlib import sha256

def validate_login(username, password):
    try:
        # Connect to the RENTSDB database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="",  # Replace with your MySQL password
            database="rentsdb"
        )
        cursor = conn.cursor()

        # Hash the input password
        hashed_password = sha256(password.encode()).hexdigest()

        # Query to validate the username and password
        query = "SELECT * FROM users WHERE username = %s AND password_hash = %s"
        cursor.execute(query, (username, hashed_password))
        user = cursor.fetchone()

        if user:
            return True
        else:
            return False

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))
        return False

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def handle_login():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showwarning("Input Error", "Please enter both username and password.")
        return

    if validate_login(username, password):
        messagebox.showinfo("Login Successful", "Welcome to RENTS!")
        # You can proceed to open the home window or another application
        open_home()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

def open_home():
    try:
        subprocess.Popen(['python', "C:\\Users\\danma\\OneDrive\\Desktop\\Phyton Project\\Home.py"])
        root.destroy()
    except FileNotFoundError:
        messagebox.showerror("Error", "Home.py not found.")

def open_signup():
    try:
        subprocess.Popen(['python', "C:\\Users\\danma\\OneDrive\\Desktop\\Phyton Project\\signup.py"])
        root.destroy() 
    except FileNotFoundError:
        messagebox.showerror("Error", "signup.py not found.")

def toggle_password():
    if show_password_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")
        
def create_user(username, password):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="RENTSDB"
        )
        cursor = conn.cursor()

        # Hash the password
        hashed_password = sha256(password.encode()).hexdigest()

        # Insert user without specifying employeeID
        query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
        cursor.execute(query, (username, hashed_password))
        conn.commit()

        print("User created successfully!")
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# Tkinter GUI setup
root = tk.Tk()
root.title("RENTS: Admin Login")

icon = tk.PhotoImage(file="C:\\Users\\danma\\OneDrive\\Desktop\\Phyton Project\\images\\house.png")
root.iconphoto(True, icon)

bg_photo = tk.PhotoImage(file="C:\\Users\\danma\\OneDrive\\Desktop\\Phyton Project\\images\\2.png")
background_label = tk.Label(root, image=bg_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

height = 600
width = 1000
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f'{width}x{height}+{x}+{y}')
root.resizable(False, False)

root.configure(bg="slateblue4")

center_frame = tk.Frame(root, bg="slateblue4")
center_frame.place(x=280, y=180)

title_label = tk.Label(center_frame, text="Admin Login", font=("Arial", 24, "bold"), bg="slateblue4", fg="white")
title_label.pack(pady=20)

username_label = tk.Label(center_frame, text="Username:", font=("Arial", 12, "bold"), bg="slateblue4", fg="white")
username_label.pack(anchor="w", padx=10)
username_entry = tk.Entry(center_frame, font=("Arial", 14), width=30)
username_entry.pack(pady=10)

password_label = tk.Label(center_frame, text="Password:", font=("Arial", 12, "bold"), bg="slateblue4", fg="white")
password_label.pack(anchor="w", padx=10)
password_entry = tk.Entry(center_frame, font=("Arial", 14), width=30, show="*")
password_entry.pack(pady=10)

show_password_var = tk.BooleanVar()
show_password_checkbox = tk.Checkbutton(center_frame, text="Show Password", font=("Arial", 12, "bold"),
                                        bg="slateblue4", fg="white", variable=show_password_var,
                                        command=toggle_password)
show_password_checkbox.pack(pady=5)

button_frame = tk.Frame(center_frame, bg="slateblue4")
button_frame.pack(pady=20)

login_button = tk.Button(button_frame, text="Login", font=("Arial", 14, "bold"), bg="blue", fg="white", width=10, command=handle_login)
login_button.grid(row=0, column=0, padx=10)

signup_button = tk.Button(button_frame, text="Sign Up", font=("Arial", 14, "bold"), bg="red", fg="white", width=10, command=open_signup)
signup_button.grid(row=0, column=1, padx=10)

back_button = tk.Button(button_frame, text="Back", font=("Arial", 14, "bold"), bg="cyan", fg="white", width=10, command=open_home)
back_button.grid(row=0, column=2, padx=10)

root.mainloop()