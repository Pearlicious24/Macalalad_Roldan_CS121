import tkinter as tk
import subprocess

def open_login():
    try:
        subprocess.Popen(['python', "C:\\Users\\danma\\OneDrive\\Desktop\\Phyton Project\\login.py"])
        root.destroy()
    except FileNotFoundError:
        print("Error: login.py not found.")

def open_customer():
    try:
        subprocess.Popen(['python', "C:\\Users\\danma\\OneDrive\\Desktop\\Phyton Project\\room.py"])
        root.destroy() 
    except FileNotFoundError:
        print("Error: room.py not found.")

root = tk.Tk()
root.title("RENTS: Rental Estate Navigation and Tracking System")

icon = tk.PhotoImage(file="C:\\Users\\danma\\OneDrive\\Desktop\\Phyton Project\\images\\house.png")
root.iconphoto(True, icon)

height = 600
width = 1000
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
root.resizable(False, False)

bg_photo = tk.PhotoImage(file="C:\\Users\\danma\\OneDrive\\Desktop\\Phyton Project\\images\\RENT.png")
background_label = tk.Label(root, image=bg_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

color2 = '#8a2be2'  
color3 = '#65e7ff'  
color4 = 'WHITE'    

def on_enter(button):
    button.config(background=color3)

def on_leave(button):
    button.config(background=color2)

adminbtn = tk.Button(
    root,
    text='Admin',
    font=('fixedsys', 16, 'bold'),
    fg=color4,
    bg=color2,
    width=16,
    height=2,
    relief="sunken",
    bd=1,
    cursor="hand2",
    command=open_login,
    padx=20,
    pady=10
)
adminbtn.place(x=390, y=350)

adminbtn.bind("<Enter>", lambda e: on_enter(adminbtn))
adminbtn.bind("<Leave>", lambda e: on_leave(adminbtn))

customerbtn = tk.Button(
    root,
    text='Customer View',
    font=('fixedsys', 16, 'bold'),
    fg=color4,
    bg=color2,
    width=16,
    height=2,
    relief="sunken",
    bd=1,
    cursor="hand2",
    command=open_customer,
    padx=20,
    pady=10
)
customerbtn.place(x=390, y=450)

customerbtn.bind("<Enter>", lambda e: on_enter(customerbtn))
customerbtn.bind("<Leave>", lambda e: on_leave(customerbtn))

root.mainloop()