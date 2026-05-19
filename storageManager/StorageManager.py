import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox

def create_table():
    conn = sqlite3.connect("store.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS products(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NO NULL UNIQUE,price REAL NO NULL,stock INTEGER NO NULL)""")
    conn.commit()
    conn.close()
def get_all_products():
    conn =sqlite3.connect("store.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products ORDER BY NAME")
    products = cursor.fetchall()
    conn.close()
    return [dict(p) for p in products]
def add_products(name,price,stock):
   conn = sqlite3.connect("store.db")
   cursor = conn.cursor()
   cursor.execute("INSERT INTO products(name,price,stock) VALUES(?,?,?)",(name,price,stock))
   conn.commit()
   conn.close()
create_table()

root  = tk.Tk()
root.title("Store Manager")
root.geometry("600x400")
root.configure(bg="#1e1e2e")
top  = tk.Frame(root , bg="#1e1e2e")
top.pack(pady=10)
tk.Label(top, text="Name" , bg="#1e1e2e" ,fg="white").grid(row=0,column=0,padx=5)
tk.Label(top, text="Price" , bg="#1e1e2e" ,fg="white").grid(row=0,column=1,padx=5)
tk.Label(top, text="Stock" , bg="#1e1e2e" ,fg="white").grid(row=0,column=2,padx=5)
button_frame = tk.Frame(root,bg="#1e1e2e")
button_frame.pack(pady=5)


entry_name = tk.Entry(top,width=15)
entry_name.grid(row=1,column=0,padx=5)
entry_price = tk.Entry(top,width=15)
entry_price.grid(row=1,column=1,padx=5)
entry_stock = tk.Entry(top,width=15)
entry_stock.grid(row=1,column=2,padx=5)
status = tk.Label(root,text="" ,bg="#1e1e2e",fg="#00e5a0")
status.pack(padx=5)
def add():
    try:
     name = entry_name.get()
     if not name:
        messagebox.showwarning("Warning", "Product name can't be empty")
        return
     price = float(entry_price.get())
     stock = int(entry_stock.get())
     add_products(name,price,stock)
     status.config(text=f"✓ {name} added", fg="#00e5a0")
     messagebox.showinfo("Added it",f"with name : {name} , price : {price} , stock{stock} succesfully")
     refresh_list()
     clear_entries()
    except ValueError:
        messagebox.showerror("Invalid","Sintaxis Error")
        status.config(text="x invalid sintaxis" ,fg="#ff6a6a")
def delete():
    name = entry_name.get()
    if not name:
        messagebox.showwarning("Warning", "Enter a product name first")
        status.config(text="✗ Enter a product name", fg="#ff6a6a")
        return
    if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{name}'?"):
       return
       
    conn = sqlite3.connect("store.db")
    cursor =  conn.cursor()
    cursor.execute("DELETE FROM products WHERE LOWER(name) = LOWER(?)",(name,))
    conn.commit()
    conn.close()
    clear_entries()
    if cursor.rowcount == 0:
        messagebox.showwarning("Not Found", f"Product '{name}' doesn't exist")
    else:
     status.config(text=f"✓ {name} deleted", fg="#00e5a0")
     refresh_list()
def search():
    name = entry_name.get()
    conn = sqlite3.connect("store.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE LOWER(name) = LOWER(?)",(name,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        result = dict(result)
        status.config(text=f"Found: {result['name']} - S/ {result['price']} - Stock: {result['stock']}",
            fg="#00e5a0")
    else :
       status.config(text="✗ Product not found", fg="#ff6a6a") 
def update():
    try:
        name = entry_name.get()
        if not name:
            messagebox.showwarning("Warning", "Enter a product name first")
            return
        new_stock = int(entry_stock.get())
        conn = sqlite3.connect("store.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE products SET stock = ? WHERE LOWER(name) = LOWER(?)",(new_stock,name))
        conn.commit()
        if cursor.rowcount == 0:
         messagebox.showwarning("Not Found", f"Product '{name}' doesn't exist")
         status.config(text="✗ Product not found", fg="#ff6a6a")
        else:
         status.config(text=f"✓ Stock updated for {name}", fg="#00e5a0")
         refresh_list()
        conn.close()
    except ValueError:
        messagebox.showerror("Invalid Input", "Stock must be a whole number")
        status.config(text="✗ Invalid stock value", fg="#ff6a6a")

Button_add = tk.Button(button_frame,text="Add" , command=add ,  bg="#7c6aff", fg="white", width=12)
Button_add.pack(side="left",padx=4)
Button_delete = tk.Button(button_frame,text = "Delete", command=delete  ,bg="#54a0ff", fg="white", width=12)
Button_delete.pack(side="left" , padx=4)
Button_search = tk.Button(button_frame,text = "Search", command=search  ,bg="#ff9f43", fg="white", width=12)
Button_search.pack(side="left" , padx=4)
Button_upgrade = tk.Button(button_frame,text = "Upgrade", command=update  ,bg="#ff6a6a", fg="white", width=12)
Button_upgrade.pack(side="left" , padx=4)

tree = ttk.Treeview(root,columns=("id","name","price","stock"),show="headings")
tree.heading("id", text="ID")
tree.heading("name" , text="NAME")
tree.heading("price",text="PRICE")
tree.heading("stock",text="STOCK")
tree.column("id" , width=50)
tree.column("name",width=200)
tree.column("price",width=150)
tree.column("stock",width=150)
tree.pack(padx=10,pady=10)
def clear_entries():
   entry_name.delete(0,tk.END)
   entry_price.delete(0,tk.END)
   entry_stock.delete(0,tk.END)
def on_selected(event):
   selected = tree.focus()
   if selected:
      values =  tree.item(selected)["values"]
      entry_name.delete(0,tk.END)
      entry_name.insert(0,values[1])
      entry_price.delete(0,tk.END)
      entry_price.insert(0,values[2])
      entry_stock.delete(0,tk.END)
      entry_stock.insert(0,values[3])
tree.bind("<<TreeviewSelect>>",on_selected)


def refresh_list():
    for row in tree.get_children():
        tree.delete(row)
    for p in get_all_products():
        tree.insert("","end", values=(p["id"],p["name"],p["price"],p["stock"]))


refresh_list()



root.mainloop()

