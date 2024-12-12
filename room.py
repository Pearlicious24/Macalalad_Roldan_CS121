import tkinter as tk
from tkinter import PhotoImage
import subprocess

room_images = {
    "Room 2021": "C:\\Users\\danma\\OneDrive\\Desktop\\Phyton Project\\images\\Room 2021.png",
    "Room 2022": "C:\\Users\\danma\\OneDrive\\Desktop\\Phyton Project\\images\\Room 2022.png",
    "Room 2023": "C:\\Users\\danma\\OneDrive\\Desktop\\Phyton Project\\images\\Room 2023.png",
    "Room 2024": "C:\\Users\\danma\\OneDrive\\Desktop\\Phyton Project\\images\\Room 2024.png",
    "Room 2025": "C:\\Users\\danma\\OneDrive\\Desktop\\Phyton Project\\images\\Room 2025.png",
    "Room 2026": "C:\\Users\\danma\\OneDrive\\Desktop\\Phyton Project\\images\\Room 2026.png",
    "Room 2027": "C:\\Users\\danma\\OneDrive\\Desktop\\Phyton Project\\images\\Room 2027.png",
    "Room 2028": "C:\\Users\\danma\\OneDrive\\Desktop\\Phyton Project\\images\\Room 2028.png",
    "Room 2029": "C:\\Users\\danma\\OneDrive\\Desktop\\Phyton Project\\images\\Room 2029.png",
    "Room 2030": "C:\\Users\\danma\\OneDrive\\Desktop\\Phyton Project\\images\\Room 2030.png"
}

def reset_image():
    image_label.config(image='', bg="white")
    image_label.image = None 
    description_label.config(text="Select a room to view details")

def display_image(room_name):
    global reset_timer

    if reset_timer:
        root.after_cancel(reset_timer)

    image_path = room_images.get(room_name, None)
    if image_path:
        try:
        
            image = PhotoImage(file=image_path)
            image_label.config(image=image, bg="white")
            image_label.image = image  
            
            description_label.config(text=f"Welcome to {room_name}")
        except Exception as e:
            description_label.config(text=f"Error loading image for {room_name}: {e}", fg="red")

    reset_timer = root.after(10000, reset_image)

def open_home():
    try:
        subprocess.Popen(['python', "C:\\Users\\danma\\OneDrive\\Desktop\\Phyton Project\\Home.py"])
        root.destroy()
    except FileNotFoundError:
        print("Error: Home.py not found.")

root = tk.Tk()
root.title("RENTS: Customer View")

icon_path = "C:\\Users\\danma\\OneDrive\\Desktop\\Phyton Project\\images\\Room 2021.png"
bg_path = "C:\\Users\\danma\\OneDrive\\Desktop\\Phyton Project\\images\\Customer.png"

icon = tk.PhotoImage(file=icon_path)
root.iconphoto(True, icon)

bg_photo = tk.PhotoImage(file=bg_path)
background_label = tk.Label(root, image=bg_photo)
background_label.image = bg_photo
background_label.place(x=0, y=0, relwidth=1, relheight=1)

height = 600
width = 1000  
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f'{width}x{height}+{x}+{y}')
root.resizable(False, False)

frame = tk.Frame(root, bg="slateblue4")
frame.place(x=80, y=110)

room_numbers = list(room_images.keys())
for i, room in enumerate(room_numbers):
    button = tk.Button(
        frame, bg="yellow",
        text=room,  
        command=lambda r=room: display_image(r),
        font=("Arial", 12, "bold"),
        fg="slateblue4",
        width=12,  
        height=3  
    )
    button.grid(row=i % 5, column=i // 5, padx=30, pady=10)

back_button = tk.Button(root, text="Back", command=open_home, font=("Arial", 12, "bold"), bg="purple2", fg="white")
back_button.place(x=850, y=20, width=100, height=50)

image_label = tk.Label(root, bg="white", borderwidth=2, relief="solid")
image_label.place(x=550, y=150, width=380, height=400)

description_label = tk.Label(root, text="Select a room to view details", font=("Arial", 16, "bold"), bg="yellow", fg="slateblue4")
description_label.place(x=565, y=550, width=350, height=30)

reset_timer = None

root.mainloop()