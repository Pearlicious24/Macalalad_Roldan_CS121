import tkinter as tk
from tkinter import messagebox
import subprocess
import mysql.connector
from hashlib import sha256

def submit_signup():
    full_name = full_name_entry.get()
    contact_no = contact_no_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    if not full_name or not contact_no or not username or not password or not confirm_password:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    if len(contact_no) != 11 or not contact_no.isdigit():
        messagebox.showerror("Input Error", "Contact number must be a 11-digit number.")
        return

    if password != confirm_password:
        messagebox.showerror("Password Mismatch", "Passwords do not match.")
        return

    hashed_password = sha256(password.encode()).hexdigest()

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="rentsdb"
        )
        cursor = conn.cursor()

        query = "INSERT INTO users (full_name, contact_no, username, password_hash) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (full_name, contact_no, username, hashed_password))
        conn.commit()

        messagebox.showinfo("Sign Up Successful", "You have successfully signed up!")
        open_login() 
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def open_login():
    try:
        subprocess.Popen(['python', "C:\\Users\\danma\\OneDrive\\Desktop\\Phyton Project\\Home.py"])
        root.destroy()
    except FileNotFoundError:
        print("Error: login.py not found.")

def open_acc():
    try:
        subprocess.Popen(['python', "C:\\Users\\danma\\OneDrive\\Desktop\\Phyton Project\\login.py"])
        root.destroy()
    except FileNotFoundError:
        print("Error: login.py not found.")

root = tk.Tk()
root.title("RENTS: Create Account")

icon = tk.PhotoImage(file="C:\\Users\\danma\\OneDrive\\Desktop\\Phyton Project\\images\\house.png")
root.iconphoto(True, icon)

bg_photo = tk.PhotoImage(file="C:\\Users\\danma\\OneDrive\\Desktop\\Phyton Project\\images\\3.png")
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
center_frame.place(height= 400, width=700, x=150, y=100)

title_label = tk.Label(center_frame, text="Create Account", font=("Arial", 24, "bold"), bg="slateblue4", fg="white")
title_label.pack(pady=20)

full_name_label = tk.Label(center_frame, text="Full Name:", font=("Arial", 12, "bold"), bg="slateblue4", fg="white")
full_name_label.place(x=85, y=93)
full_name_entry = tk.Entry(center_frame, font=("Arial", 14), width=30)
full_name_entry.pack(pady=10)

contact_no_label = tk.Label(center_frame, text="Contact No:", font=("Arial", 12, "bold"), bg="slateblue4", fg="white")
contact_no_label.place(x=75, y=139)
contact_no_entry = tk.Entry(center_frame, font=("Arial", 14), width=30)
contact_no_entry.pack(pady=10)

username_label = tk.Label(center_frame, text="Username:", font=("Arial", 12, "bold"), bg="slateblue4", fg="white")
username_label.place(x=85, y=185)
username_entry = tk.Entry(center_frame, font=("Arial", 14), width=30)
username_entry.pack(pady=10)

password_label = tk.Label(center_frame, text="Password:", font=("Arial", 12, "bold"), bg="slateblue4", fg="white")
password_label.place(x=85, y=230)
password_entry = tk.Entry(center_frame, font=("Arial", 14), width=30, show="*")
password_entry.pack(pady=10)

confirm_password_label = tk.Label(center_frame, text="Confirm Password:", font=("Arial", 12, "bold"), bg="slateblue4", fg="white")
confirm_password_label.place(x=20, y=270)
confirm_password_entry = tk.Entry(center_frame, font=("Arial", 14), width=30, show="*")
confirm_password_entry.pack(pady=10)

button_frame = tk.Frame(center_frame, bg="slateblue4")
button_frame.pack(pady=20)
button_frame.place(x=380, y=330)

done_button = tk.Button(button_frame, text="Done", font=("Arial", 14, "bold"), bg="blue", fg="white", width=10, command=submit_signup)
done_button.grid(row=0, column=0, padx=10)

back_button = tk.Button(button_frame, text="Back", font=("Arial", 14, "bold"), command=open_login, bg="red", fg="white", width=10)
back_button.grid(row=0, column=1, padx=10)

already_account_label = tk.Label(center_frame, text="Already have an account?", font=("Arial", 12, "bold"), bg="slateblue4", fg="white", cursor="hand2")
already_account_label.place(x=40, y=340)
already_account_label.bind("<Button-1>", lambda e: open_acc())

root.mainloop()