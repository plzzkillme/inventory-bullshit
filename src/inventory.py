import tkinter as tk
from tkinter import ttk, messagebox
import json

inventory = []

def add_item(sku, quantity, staff_price, normal_price, complimentary_price, promo_price):
        new_item = {"sku": sku, "quantity": quantity, "staff price": staff_price, "normal price": normal_price, "complimentary price": complimentary_price, "promo price": promo_price}
        inventory.append(new_item)
        messagebox.showinfo("Success", f"{sku} added to inventory")
        show_inventory()

def update_quantity(sku, new_quantity):
    for item in inventory:
        if item["sku"] == sku:
            item["quantity"] = new_quantity
            messagebox.showinfo("Success", f"Quantity of {sku} updated to {new_quantity}")
            show_inventory()
            return
    messagebox.showwarning("Not found", f"{sku} not found in inventory")    

def save_inventory(filename="inventory.json"):
    with open(filename, 'w') as f:
        json.dump(inventory, f, indent=4)
    messagebox.showinfo("Saved", "Inventory saved")

def load_inventory(filename="inventory.json"):
    global inventory
    try:
        with open(filename, 'r') as f:
            inventory = json.load(f)
        messagebox.showinfo("Loaded", "Inventory loaded")
        show_inventory()
    except FileNotFoundError:
        messagebox.showwarning("Error", "Inventory file not found")

def clear_entries():
    sku_entry.delete(0, tk.END)
    qty_entry.delete(0, tk.END)
    staff_entry.delete(0, tk.END)
    normal_entry.delete(0, tk.END)
    complimentary_entry.delete(0, tk.END)
    promo_entry.delete(0, tk.END)

def delete_selected_item():
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Error", "Please select a row to delete")
        return 
    item_id = selected[0]
    sku = tree.item(item_id, "values")[0]
    for item in inventory:
        if item["sku"] == sku:
            inventory.remove(item)
            break
    tree.delete(item_id)
    messagebox.showinfo("Deleted", f"{sku} removed from inventory")

def show_inventory():
    for row in tree.get_children():
        tree.delete(row)
    for item in inventory:
        tree.insert("", tk.END, values=(item["sku"], item["quantity"], item["staff price"], item["normal price"], item["complimentary price"], item["promo price"]))

def add_item_gui():
    try:
        sku = sku_entry.get()
        qty = int(qty_entry.get())
        staff_price = float(staff_entry.get())
        normal_price = float(normal_entry.get())
        complimentary_price = float(complimentary_entry.get())
        promo_price = float(promo_entry.get())
        add_item(sku, qty, staff_price, normal_price, complimentary_price, promo_price)
    except ValueError:
        messagebox.showerror("Input error", "Please enter valid numbers for quantity and prices")
    clear_entries()

def update_item_gui():
    try:
        sku = sku_entry.get()
        qty = int(qty_entry.get())
        update_quantity(sku, qty)
        show_inventory()    
    except ValueError:
        messagebox.showerror("Input error", "Plase enter valid numbers for quantity")
    clear_entries()

root = tk.Tk()
root.title("Inventory System")

tk.Label(root, text="SKU").grid(row=0, column=0, padx=5, pady=5)
sku_entry = tk.Entry(root)
sku_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Quantity").grid(row=1, column=0, padx=5, pady=5)
qty_entry = tk.Entry(root)
qty_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Staff Price").grid(row=2, column=0, padx=5, pady=5)
staff_entry = tk.Entry(root)
staff_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Normal Price").grid(row=3, column=0, padx=5, pady=5)
normal_entry = tk.Entry(root)
normal_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(root, text="Complimentary Price").grid(row=4, column=0, padx=5, pady=5)
complimentary_entry = tk.Entry(root)
complimentary_entry.grid(row=4, column=1, padx=5, pady=5)

tk.Label(root, text="Promo Price").grid(row=5, column=0, padx=5, pady=5)
promo_entry = tk.Entry(root)
promo_entry.grid(row=5, column=1, padx=5, pady=5)

tk.Button(root, text="Add Item", command=add_item_gui).grid(row=6, column=0, pady=5)
tk.Button(root, text="Update Quantity", command=update_item_gui).grid(row=6, column=1, pady=5)
tk.Button(root, text="Save Inventory", command=save_inventory).grid(row=7, column=0, pady=5)
tk.Button(root, text="Load Inventory", command=load_inventory).grid(row=7, column=1, pady=5)
tk.Button(root, text="Delete Item", command=delete_selected_item).grid(row=8, column=0, pady=5)

columns = ("SKU", "Quantity", "Staff Price", "Normal Price", "Complimentary Price", "Promo Price")
tree = ttk.Treeview(root, columns=columns, show="headings", height=12)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120, anchor="center")

tree.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

show_inventory()

root.mainloop()
