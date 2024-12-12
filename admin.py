import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import Toplevel
import win32print
import win32ui
import subprocess
import mysql.connector

def add_entry():
    selected_room = room_selector.get()
    if not validate_fields():
        return

    used_rooms = [table.item(child)["values"][0] for child in table.get_children()]
    if selected_room in used_rooms:
        conflicting_item = next(child for child in table.get_children() if table.item(child)["values"][0] == selected_room)
        table.selection_set(conflicting_item)
        table.focus(conflicting_item)
        messagebox.showerror("Error", f"Room {selected_room} is already assigned!")
        return

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',  
            password='',  
            database='rentsdb' 
        )
        cursor = conn.cursor()

        cursor.execute("SELECT room_no FROM bookings WHERE room_no = %s", (selected_room,))
        existing_room = cursor.fetchone()

        if existing_room:
            messagebox.showerror("Error", f"Room {selected_room} is already booked!")
            return

        query = """
            INSERT INTO bookings (room_no, first_name, last_name, days, total)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (selected_room, first_name_entry.get(), last_name_entry.get(), days_entry.get(), total_entry.get())

        cursor.execute(query, values)
        conn.commit()

        table.insert("", "end", values=(selected_room, first_name_entry.get(), last_name_entry.get(), days_entry.get(), total_entry.get()))

        clear_fields()

        update_room_choices()

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error inserting into database: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def open_home():
    try:
        subprocess.Popen(['python', "C:\\Users\\danma\\OneDrive\\Desktop\\Phyton Project\\Home.py"])
        root.destroy()
    except FileNotFoundError:
        print("Error: Home.py not found.")

def open_customer():
    try:
        subprocess.Popen(['python', "C:\\Users\\danma\\OneDrive\\Desktop\\Phyton Project\\room.py"])
        root.destroy()
    except FileNotFoundError:
        print("Error: Home.py not found.")

def update_room_choices():
    used_rooms = [table.item(child)["values"][0] for child in table.get_children()]
    available_rooms = [room for room in room_numbers if room not in used_rooms]
    room_selector["values"] = available_rooms
    if available_rooms:
        room_selector["state"] = "readonly"
        room_selector.set(available_rooms[0])
    else:
        room_selector["state"] = "disabled"
        room_selector.set("No Rooms Available")

def populate_table():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  
            database='rentsdb'  
        )
        cursor = conn.cursor()

        cursor.execute("SELECT room_no, first_name, last_name, days, total FROM bookings")
        rows = cursor.fetchall()

        for row in table.get_children():
            table.delete(row)

        for row in rows:
            table.insert("", "end", values=row)

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error fetching data from database: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()



def validate_fields(check_room=True):
    if check_room and (not room_selector.get() or room_selector.get() == "No Rooms Available"):
        messagebox.showerror("Error", "Please select a valid room number!")
        return False
    if not first_name_entry.get().strip():
        messagebox.showerror("Error", "First Name cannot be empty!")
        return False
    if not last_name_entry.get().strip():
        messagebox.showerror("Error", "Last Name cannot be empty!")
        return False
    if not days_entry.get().strip().isdigit():
        messagebox.showerror("Error", "Days must be a valid number!")
        return False
    if not total_entry.get().strip().isdigit():
        messagebox.showerror("Error", "Amount must be a valid number!")
        return False
    return True


def delete_entry():
    selected_item = table.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select an item to delete.")
        return
    
    confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected booking?")
    if not confirm:
        return
    room_no = table.item(selected_item)["values"][0]
    
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='rentsdb'  
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bookings WHERE room_no = %s", (room_no,))
        conn.commit() 

        table.delete(selected_item)

        messagebox.showinfo("Success", "Booking deleted successfully.")
        
        populate_table()

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error deleting record: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def update_entry():
    selected_item = table.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "No row selected to update!")
        return

    selected_room = room_selector.get()
    if not validate_fields(check_room=False):
        return

    used_rooms = [table.item(child)["values"][0] for child in table.get_children() if child != selected_item[0]]
    if selected_room in used_rooms:
        conflicting_item = next(child for child in table.get_children() if table.item(child)["values"][0] == selected_room)
        table.selection_set(conflicting_item)
        table.focus(conflicting_item)
        messagebox.showerror("Error", f"Room {selected_room} is already assigned to another entry!")
        return

    old_room_no = table.item(selected_item)["values"][0]
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    days = days_entry.get()
    total = total_entry.get()

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',  
            password='',  
            database='rentsdb' 
        )
        cursor = conn.cursor()

        update_query = """
            UPDATE bookings
            SET room_no = %s, first_name = %s, last_name = %s, days = %s, total = %s
            WHERE room_no = %s
        """
        cursor.execute(update_query, (selected_room, first_name, last_name, days, total, old_room_no))
        conn.commit()

        table.item(selected_item, values=(selected_room, first_name, last_name, days, total))

        clear_fields()
        update_room_choices()

        messagebox.showinfo("Success", "Booking updated successfully!")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error updating record: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def clear_fields():
    first_name_entry.delete(0, tk.END)
    last_name_entry.delete(0, tk.END)
    days_entry.delete(0, tk.END)
    total_entry.delete(0, tk.END)

def show_receipt():
    selected_item = table.selection()
    if not selected_item:
        messagebox.showwarning("Warning", "No row selected to generate receipt!")
        return

    selected_data = table.item(selected_item, "values")
    room_no, first_name, last_name, days, total = selected_data

    receipt_window = Toplevel(root)
    receipt_window.title("Receipt")
    receipt_window.geometry("400x500")
    receipt_window.configure(bg="white")
    receipt_window.resizable(False, False)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 400
    window_height = 500
    position_top = (screen_height // 2) - (window_height // 2)
    position_left = (screen_width // 2) - (window_width // 2)
    receipt_window.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')

    tk.Label(receipt_window, text="RENTS: Rental Estate Navigation\n and Tracking System", font=("fixedsys", 10, "bold"), bg="white").pack(pady=10)
    tk.Label(receipt_window, text="---------------------------------------------------", font=("fixedsys", 15, "bold"), bg="white").pack(pady=0)
    tk.Label(receipt_window, text="Sale Receipt", font=("fixedsys", 20, "bold"), bg="white").pack(pady=5)
    tk.Label(receipt_window, text="---------------------------------------------------", font=("fixedsys", 15, "bold"), bg="white").pack(pady=0)
    tk.Label(receipt_window, text=f"Room No: {room_no}", font=("fixedsys", 14), bg="white").pack(anchor="w", padx=20, pady=5)
    tk.Label(receipt_window, text=f"Name: {first_name} {last_name}", font=("fixedsys", 14), bg="white").pack(anchor="w", padx=20, pady=5)
    tk.Label(receipt_window, text=f"Days: {days}", font=("fixedsys", 14), bg="white").pack(anchor="w", padx=20, pady=5)
    tk.Label(receipt_window, text="---------------------------------------------------", font=("fixedsys", 15, "bold"), bg="white").pack(pady=0)
    tk.Label(receipt_window, text=f"Total: \t\t PHP {total}\t", font=("fixedsys", 14, "bold"), bg="white").pack(anchor="w", padx=20, pady=5)
    tk.Label(receipt_window, text="---------------------------------------------------", font=("fixedsys", 15, "bold"), bg="white").pack(pady=0)
    tk.Label(receipt_window, text="Thank you!", font=("fixedsys", 10, "bold"), bg="white").pack(pady=10)

    button_frame = tk.Frame(receipt_window, bg="white")
    button_frame.pack(pady=20)

    def print_receipt():
        messagebox.showinfo("Print", "Printing receipt...")
        print_dialog(selected_data, first_name, last_name, days, total)

    def go_back():
        receipt_window.destroy()

    print_button = tk.Button(button_frame, text="Print", command=print_receipt, bg="purple2", fg="white", font=("Arial", 12, "bold"))
    print_button.pack(side="left", padx=10)

    back_button = tk.Button(button_frame, text="Back", command=go_back, bg="red", fg="white", font=("Arial", 12, "bold"))
    back_button.pack(side="left", padx=10)

def print_dialog(selected_room, first_name, last_name, days, total):
    try:
        printer_name = win32print.GetDefaultPrinter()
        printer_dc = win32ui.CreateDC()
        printer_dc.CreatePrinterDC(printer_name)
        printer_dc.StartDoc("Receipt")
        printer_dc.StartPage()

        line_height = 40  # Adjust this value to fine-tune spacing
        y_position = 100

        # Using TextOut for printing
        printer_dc.TextOut(100, y_position, "RENTS: Rental Estate Navigation and Tracking System")
        y_position += line_height
        printer_dc.TextOut(100, y_position, "---------------------------------------------------")
        y_position += line_height
        printer_dc.TextOut(100, y_position, "Sale Receipt")
        y_position += line_height
        printer_dc.TextOut(100, y_position, "---------------------------------------------------")
        y_position += line_height
        printer_dc.TextOut(100, y_position, f"Room No: {selected_room}")
        y_position += line_height
        printer_dc.TextOut(100, y_position, f"Name: {first_name} {last_name}")
        y_position += line_height
        printer_dc.TextOut(100, y_position, f"Days: {days}")
        y_position += line_height
        printer_dc.TextOut(100, y_position, "---------------------------------------------------")
        y_position += line_height
        printer_dc.TextOut(100, y_position, f"Total: PHP {total}")
        y_position += line_height
        printer_dc.TextOut(100, y_position, "---------------------------------------------------")
        y_position += line_height
        printer_dc.TextOut(100, y_position, "Thank you!")

        printer_dc.EndPage()
        printer_dc.EndDoc()
        printer_dc.DeleteDC()

        messagebox.showinfo("Success", "Receipt printed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to print receipt: {e}")



root = tk.Tk()
root.title("RENTS: Admin View")

icon = tk.PhotoImage(file="C:\\Users\\danma\\OneDrive\\Desktop\\Phyton Project\\images\\house.png")
root.iconphoto(True, icon)

height = 600
width = 1000
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f'{width}x{height}+{x}+{y}')
root.resizable(False, False)

try:
    bg_image = tk.PhotoImage(file="C:\\Users\\danma\\OneDrive\\Desktop\\Phyton Project\\images\\Admin.png")
    bg_label = tk.Label(root, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)
except Exception:
    bg_label = tk.Label(root, bg="slateblue4")
    bg_label.place(relwidth=1, relheight=1)

table_frame = tk.Frame(root, bg="slateblue4")
table_frame.place(height=250, width=800, x=100, y=250)
columns = ("Room No", "First Name", "Last Name", "Day", "Total")
table = ttk.Treeview(table_frame, columns=columns, show="headings")
table.pack(fill="both", expand=True)

for col in columns:
    table.heading(col, text=col)
    table.column(col, width=150, anchor="center")

input_frame = tk.Frame(root, bg="slateblue4")
input_frame.place(x=60, y=165)

room_numbers = [str(room) for room in range(2021, 2031)]
tk.Label(input_frame, text="Room No:", bg="slateblue4", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5, pady=5)
room_selector = ttk.Combobox(input_frame, state="readonly", font=("Arial", 12))
room_selector.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="First Name:", bg="slateblue4", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=5, pady=5)
first_name_entry = tk.Entry(input_frame, font=("Arial", 12))
first_name_entry.grid(row=0, column=3, padx=5, pady=5)

tk.Label(input_frame, text="Last Name:", bg="slateblue4", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=4, padx=5, pady=0)
last_name_entry = tk.Entry(input_frame, font=("Arial", 12))
last_name_entry.grid(row=0, column=5, padx=5, pady=5)

tk.Label(input_frame, text="Days:", bg="slateblue4", fg="white", font=("Arial", 12, "bold")).grid(row=1, column=2, padx=5, pady=5)
days_entry = tk.Entry(input_frame, font=("Arial", 12))
days_entry.grid(row=1, column=3, padx=5, pady=5)

tk.Label(input_frame, text="Total:", bg="slateblue4", fg="white", font=("Arial", 12, "bold")).grid(row=1, column=4, padx=5, pady=5)
total_entry = tk.Entry(input_frame, font=("Arial", 12))
total_entry.grid(row=1, column=5, padx=5, pady=5)

button_frame = tk.Frame(root, bg="slateblue4")
button_frame.place(x=570, y=510)
add_button = tk.Button(button_frame, text="Add", command=add_entry, bg="green", fg="white", font=("Arial", 12, "bold"))
add_button.pack(side="left", padx=10, pady=10)

delete_button = tk.Button(button_frame, text="Delete", command=delete_entry, bg="red", fg="white", font=("Arial", 12, "bold"))
delete_button.pack(side="left", padx=10, pady=10)

update_button = tk.Button(button_frame, text="Update", command=update_entry, bg="blue", fg="white", font=("Arial", 12, "bold"))
update_button.pack(side="left", padx=10, pady=10)

receipt_button = tk.Button(button_frame, text="Receipt", command=show_receipt, bg="orange", fg="white", font=("Arial", 12, "bold"))
receipt_button.pack(side="left", padx=10, pady=10)

home_button = tk.Button(root, text="Home", command=open_home, bg="cyan", fg="white", font=("Arial", 12, "bold"))
home_button.place(x=800, y=50)

customer_button = tk.Button(root, text="Rooms", command=open_customer, bg="blue", fg="white", font=("Arial", 12, "bold"))
customer_button.place(x=880, y=50)

populate_table()

update_room_choices()
root.mainloop()