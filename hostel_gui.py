import tkinter as tk
from tkinter import font
from tkinter import *
from datetime import datetime
from tkinter import ttk
import sqlite3
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
main_window=tk.Tk()
main_window.minsize(800,700)
main_window.title("Hotel Management")
option=[
    "Cold coffie 250",
    "Margarita pizza 500",
    "Cheese cake 350",
    "Italian pasta 600",
    "Spicy noodles 400",
    "Veg burger 200"
    ]
added_items = []
def create_tables():
    try:
        con = sqlite3.connect('hotel.db')
        cur = con.cursor()
        query1 = "CREATE TABLE IF NOT EXISTS Bill (personid INTEGER PRIMARY KEY, tableno INTEGER,coffie INTEGER DEFAULT 0,pizza INTEGER DEFAULT 0,cake INTEGER DEFAULT 0,pasta INTEGER DEFAULT 0,noodles INTEGER DEFAULT 0,burger INTEGER DEFAULT 0, total INTEGER)"
        cur.execute(query1)     
    except sqlite3.Error as e:
        print('Error:', e)
    finally:
        con.close()

def add():
    create_tables()
    con = sqlite3.connect('hotel.db')
    cur = con.cursor()
    selected_menu = intial_val.get().split()[1]
    quantity = int(Quantity_val.get())
    print(selected_menu)
    update_query = f"UPDATE Bill SET {selected_menu} = {selected_menu} + ? WHERE personid = ?"
    cur.execute(update_query, (quantity, id))
    con.commit()
    update_tree(intial_val.get(),quantity)
    update_piechart()
    temp_total=calculate_total()
    print(temp_total)
    updated_text='Total: '+str(temp_total)
    print(updated_text)
    label1_frame2_3.config(text=updated_text)

def update_tree(selected_menu, quantity):

    for item_id in tree.get_children():

        if tree.item(item_id, 'values')[0] == selected_menu:
            
            current_quantity = int(tree.item(item_id, 'values')[1])
            current_cost = int(tree.item(item_id, 'values')[2])

            updated_quantity = current_quantity + quantity
            updated_cost = updated_quantity * int(selected_menu.split()[2])

            tree.item(item_id, values=(selected_menu, updated_quantity, updated_cost))
            break  # No need to continue iterating once the item is found-

def calculate_total():
    total = 0
    for item_id in tree.get_children():
        cost_value = tree.item(item_id, 'values')[2]  
        total += int(cost_value)
    return total

def total_income():
    try:
        con = sqlite3.connect('hotel.db')
        cur = con.cursor()
        cur.execute("SELECT total FROM Bill")
        total_values = cur.fetchall()
        total_revenue = sum(total_values, ())
        tk.messagebox.showinfo("Total Revenue", f"Total Revenue: {total_revenue}") 
    except sqlite3.Error as e:
        print('Error:', e)
    finally:
        con.close()

def confirm():
    total_amount = calculate_total()
    tableno=text1_frame2_2.get()
    
    pay_dialog = tk.Toplevel(main_window)
    pay_dialog.title("Order Placed")
    message_label = tk.Label(pay_dialog, text=f"Customer ID:{id}\nTable Number:{tableno}\nYour order has been placed!\nTotal Amount: {total_amount}",font=('Helvetica', 14, 'bold'))
    message_label.pack(padx=10, pady=10)
    pay_button = tk.Button(pay_dialog, text="Pay", command=lambda: (print("Payment processed successfully!"), pay_dialog.destroy()),bg="green", fg="white", font=('Helvetica', 12, 'bold'))
    pay_button.pack(padx=10, pady=10)
    
    try:
        con = sqlite3.connect('hotel.db')
        cur = con.cursor()
        # Insert a new record with the incremented customer ID and total set to zero
        query_update = "UPDATE Bill SET tableno = ?, total = ? WHERE personid = ?"
        cur.execute(query_update, (tableno, total_amount, id))
        con.commit()
        print(id)
    except sqlite3.Error as e:
        print(e)

def update_piechart():

    data = [(tree.item(item, 'values')[0], int(tree.item(item, 'values')[2])) for item in tree.get_children()if int(tree.item(item, 'values')[1]) != 0]
    print(data)
    if not data:
        return
   
    figure = Figure(figsize=(4, 4), dpi=100)
    ax = figure.add_subplot(111)

    labels = [item[0] for item in data]
    cost_values = [item[1] for item in data]

    ax.pie(cost_values, labels=labels, autopct=lambda p: f'{p:.1f}% ({int(p * sum(cost_values) / 100)})', startangle=90,labeldistance=1.1)
    ax.axis('equal')  
    if hasattr(update_piechart, 'canvas'):
        update_piechart.canvas.get_tk_widget().destroy()
    update_piechart.canvas = FigureCanvasTkAgg(figure, master=frame1)
    update_piechart.canvas.draw()# Pack the canvas into the frame
    update_piechart.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def new():
    Quantity_val.delete(0, tk.END)  # Clear the current value
    Quantity_val.insert(0, 1) 
    text2_frame2_2.delete(0, tk.END)
    text1_frame2_2.delete(0, tk.END)
    intial_val.set(option[0])
    for item_id in tree.get_children():
        tree.delete(item_id)
    for item in option:
            tree.insert('', 'end', values=(item.split(), 0, 0))
    try:
        con = sqlite3.connect('hotel.db')
        cur = con.cursor()
        cur.execute("SELECT MAX(personid) FROM Bill")
        latest_person_id = cur.fetchone()[0]
        if latest_person_id is None:
            new_person_id = 1
        else:
            new_person_id = latest_person_id + 1
        query_insert = "INSERT INTO Bill (personid) VALUES (?)"
        cur.execute(query_insert, (str(new_person_id),))
        global id
        id=new_person_id
        con.commit()
    except sqlite3.Error as e:
            print(e)

    id=new_person_id
    label2_frame2_2.config(text=id)
    update_piechart()


id=1
intial_val = StringVar()
intial_val.set(option[0])
main_window.columnconfigure(0, weight=1)
main_window.columnconfigure(1, weight=1)
main_window.rowconfigure(0, weight=1)
# Frame 1
frame1 = tk.Frame(main_window, borderwidth=2, relief="groove", width='1526', height='915')
frame1.grid(row=0, column=0, sticky="nsew")

label1_frame1 = tk.Label(frame1, text="Menu Card", font=('Helvetica', 16, 'bold'),width=40)
label1_frame1.pack(padx=10, pady=10)

menu_list = tk.OptionMenu(frame1, intial_val, *option)
menu_list.pack(padx=10, pady=10)
menu_list.config(font=('Helvetica', 12), width=30)

label2_frame1 = tk.Label(frame1, text="Quantity", font=('Helvetica', 12),width=30)
label2_frame1.pack(padx=10, pady=10)

Quantity_val = Spinbox(frame1, from_=1, to=50,width=32, font=('Helvetica', 12, 'bold'))
Quantity_val.pack(padx=10, pady=10)

add_btn = tk.Button(frame1, text="Add", command=add, bg="green", fg="white", font=('Helvetica', 12, 'bold'),width=20)
add_btn.pack(padx=10, pady=10)

figure = Figure(figsize=(4, 4), dpi=100)
canvas = FigureCanvasTkAgg(figure, master=frame1)
canvas.draw()

# Frame 2
frame2 = tk.Frame(main_window, borderwidth=2, relief="groove")
frame2.grid(row=0, column=1, sticky="nsew")

label_frame2 = tk.Label(frame2, text="Order Information", font=('Helvetica', 16, 'bold'))
label_frame2.grid(row=0, column=0, padx=0, pady=0)

frame2_2 = tk.Frame(frame2, borderwidth=2, relief="groove", width='400', height='300')
frame2_2.grid(row=1, column=0,columnspan=2,sticky="nsew")

label1_frame2_2 = tk.Label(frame2_2, text="Date", font=('Helvetica', 12),width=30)
label1_frame2_2.grid(row=0, column=0, padx=10, pady=10,sticky="nsew")

current_datetime = datetime.now()
current_date = current_datetime.date()

label2_frame2_2 = tk.Label(frame2_2, text=current_date, font=('Helvetica', 12, 'italic'),width=30)
label2_frame2_2.grid(row=0, column=1, padx=10, pady=10)

label1_frame2_2 = tk.Label(frame2_2, text="Customer ID", font=('Helvetica', 12))
label1_frame2_2.grid(row=1, column=0, padx=10, pady=10)

label2_frame2_2 = tk.Label(frame2_2, text=id, font=('Helvetica', 12, 'bold'),width=30)
label2_frame2_2.grid(row=1, column=1, padx=10, pady=10)

label1_frame2_2 = tk.Label(frame2_2, text="Table Number", font=('Helvetica', 12),width=30)
label1_frame2_2.grid(row=2, column=0, padx=10, pady=10)

text1_frame2_2 = Entry(frame2_2,width=40)
text1_frame2_2.grid(row=2, column=1, padx=10, pady=10)

label1_frame2_2 = tk.Label(frame2_2, text="Payment Method", font=('Helvetica', 12))
label1_frame2_2.grid(row=3, column=0, padx=10, pady=10)

text2_frame2_2 = Entry(frame2_2,width=40)
text2_frame2_2.grid(row=3, column=1, padx=10, pady=10)

frame2_3 = tk.Frame(frame2, borderwidth=2, relief="groove", width='440', height='300')
frame2_3.grid(row=2, columnspan=2,sticky="nsew")

columns = ('Item', 'Quantity', 'Cost')

tree = ttk.Treeview(frame2_3, columns=columns, show='headings')
tree.heading('Item', text='Item')
tree.heading('Quantity', text='Quantity')
tree.heading('Cost', text='Cost')
tree.grid(row=0, column=0,columnspan=4, sticky='nsew')
style = ttk.Style()
style.configure("Treeview.Heading", font=('Helvetica', 12))

style.configure("Treeview", font=('Helvetica', 10))
label1_frame2_3 = tk.Label(frame2_3, text="Total:", font=('Helvetica', 12, 'bold'))
label1_frame2_3.grid(row=1, column=0, padx=10, pady=10)

update_btn = tk.Button(frame2_3, text="Confirm Order!!", command=confirm, bg="blue", fg="white", font=('Helvetica', 12, 'bold'),width=30)
update_btn.grid(row=3, column=0, padx=10, pady=10,sticky="nsew")

update_btn = tk.Button(frame2_3, text="New Order!!", command=new, bg="orange", fg="white", font=('Helvetica', 12, 'bold'),width=30)
update_btn.grid(row=3, column=1, padx=10, pady=10,sticky="nsew")

main_window.rowconfigure(0, weight=1)
frame1.columnconfigure(0, weight=1)
frame1.rowconfigure(0, weight=1)
frame2.columnconfigure(0, weight=1)
frame2.rowconfigure(0, weight=1)
main_window.mainloop()