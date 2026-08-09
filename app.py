import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import quotation # මීට පෙර ඔබ හැදූ quotation.py ගොනුව මෙතැනින් සම්බන්ධ වේ

# භාණ්ඩ ගබඩා කර තබා ගැනීමට හිස් ලැයිස්තුවක් (List)
invoice_items_list = []

def add_item():
    desc = desc_entry.get()
    
    if not desc:
        messagebox.showwarning("Warning", "කරුණාකර Description එක ඇතුළත් කරන්න.")
        return
        
    try:
        qty = float(qty_entry.get())
        price = float(price_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Quantity සහ Price සඳහා අංක පමණක් ඇතුළත් කරන්න.")
        return

    # List එකට අලුත් භාණ්ඩය එකතු කිරීම
    invoice_items_list.append({"desc": desc, "qty": qty, "unit_price": price})
    
    # Treeview (UI වගුව) වෙත දත්ත ඇතුළත් කිරීම (Amount එකද ගණනය කර පෙන්වයි)
    amount = qty * price
    # Display quantity as whole number when it's an integer (no trailing .0)
    try:
        display_qty = str(int(qty)) if float(qty).is_integer() else str(qty)
    except Exception:
        display_qty = str(qty)

    # Format price and amount for display
    display_price = f"{price:,.2f}"
    display_amount = f"{amount:,.2f}"

    tree.insert("", tk.END, values=(desc, display_qty, display_price, display_amount))
    
    # ඊළඟ භාණ්ඩය ඇතුළත් කිරීමට පහසු වීමට, කොටු හිස් කිරීම
    desc_entry.delete(0, tk.END)
    qty_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    desc_entry.focus() # නැවත Description කොටුවට Cursor එක ගෙන යාම

def delete_selected_item():
    # වගුවෙන් තෝරාගෙන ඇති පේළි ලබා ගැනීම
    selected_items = tree.selection()
    
    if not selected_items:
        messagebox.showwarning("Warning", "කරුණාකර මකා දැමීමට අවශ්‍ය භාණ්ඩය වගුවෙන් තෝරන්න.")
        return
        
    # List එකෙන් මකා දැමීමේදී ගැටළුවක් ඇති නොවීම සඳහා Index අගයන් විශාල සිට කුඩා අනුපිළිවෙලට සකසා ගැනීම
    indices_to_delete = sorted([tree.index(item) for item in selected_items], reverse=True)
    
    # List එකෙන් අදාළ දත්ත ඉවත් කිරීම
    for index in indices_to_delete:
        del invoice_items_list[index]
        
    # UI එකේ වගුවෙන් අදාළ පේළි ඉවත් කිරීම
    for item in selected_items:
        tree.delete(item)

def create_pdf():
    c_name = name_entry.get()
    c_address = address_entry.get()
    c_phone = phone_entry.get()
    c_date = date_entry.get()

    if not c_name:
        messagebox.showwarning("Warning", "කරුණාකර පාරිභෝගිකයාගේ නම ඇතුළත් කරන්න.")
        return

    # භාණ්ඩ එකක් හෝ ඇතුළත් කර ඇත්දැයි බැලීම
    if len(invoice_items_list) == 0:
        messagebox.showwarning("Warning", "කරුණාකර එක් භාණ්ඩයක් හෝ ඇතුළත් කරන්න.")
        return

    customer_info = {
        "date": c_date,
        "name": c_name,
        "address": c_address,
        "phone": c_phone
    }

    try:
        # Read optional remarks and terms from the UI
        remarks = remarks_text.get("1.0", tk.END).strip()
        terms_raw = terms_text.get("1.0", tk.END).strip()
        terms_list = [line.strip() for line in terms_raw.splitlines() if line.strip()]

        # quotation.py හි ඇති ෆන් sähන් එකට දත්ත යැවීම (terms_list සහ remarks සමඟ)
        quotation.generate_quotation_pdf("Sivilima_Quotation.pdf", customer_info, invoice_items_list, terms_list, remarks=remarks)
        messagebox.showinfo("Success", "PDF එක සාර්ථකව නිර්මාණය විය!")
    except Exception as e:
        messagebox.showerror("Error", f"ගැටළුවක් මතු විය: {e}")

def clear_all():
    # සියලුම දත්ත මකා මුල සිට ආරම්භ කිරීම
    invoice_items_list.clear()
    for item in tree.get_children():
        tree.delete(item)
    
    name_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    messagebox.showinfo("Cleared", "සියලුම දත්ත මකා දමන ලදී.")

# --- ප්‍රධාන කවුළුව නිර්මාණය කිරීම ---
root = tk.Tk()
root.title("Sivilima - Quotation Generator")
root.geometry("550x740") # බොත්තමක් වැඩි වූ නිසා කවුළුව තවත් මඳක් දිගු කර ඇත

# 1. පාරිභෝගික දත්ත අංශය
tk.Label(root, text="Customer Details", font=("Helvetica", 12, "bold"), fg="#632c8b").pack(pady=(10, 5))

frame_customer = tk.Frame(root)
frame_customer.pack(pady=5)

tk.Label(frame_customer, text="Date:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
date_entry = tk.Entry(frame_customer, width=30)
date_entry.insert(0, "2026-08-02")
date_entry.grid(row=0, column=1, pady=2)

tk.Label(frame_customer, text="Name:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
name_entry = tk.Entry(frame_customer, width=30)
name_entry.grid(row=1, column=1, pady=2)

tk.Label(frame_customer, text="Address:").grid(row=2, column=0, sticky="e", padx=5, pady=2)
address_entry = tk.Entry(frame_customer, width=30)
address_entry.grid(row=2, column=1, pady=2)

tk.Label(frame_customer, text="Phone:").grid(row=3, column=0, sticky="e", padx=5, pady=2)
phone_entry = tk.Entry(frame_customer, width=30)
phone_entry.grid(row=3, column=1, pady=2)

# 2. භාණ්ඩ දත්ත අංශය
tk.Label(root, text="Add Items", font=("Helvetica", 12, "bold"), fg="#632c8b").pack(pady=(15, 5))

frame_items = tk.Frame(root)
frame_items.pack(pady=5)

tk.Label(frame_items, text="Description").grid(row=0, column=0, padx=5)
tk.Label(frame_items, text="Quantity").grid(row=0, column=1, padx=5)
tk.Label(frame_items, text="Unit Price").grid(row=0, column=2, padx=5)

desc_entry = tk.Entry(frame_items, width=25)
desc_entry.grid(row=1, column=0, padx=5)

qty_entry = tk.Entry(frame_items, width=10)
qty_entry.grid(row=1, column=1, padx=5)

price_entry = tk.Entry(frame_items, width=15)
price_entry.grid(row=1, column=2, padx=5)

# Add Item බොත්තම
tk.Button(root, text="➕ Add Item", bg="#10b981", fg="white", font=("Helvetica", 9, "bold"), command=add_item).pack(pady=10)

# 3. ඇතුළත් කළ භාණ්ඩ පෙන්වන වගුව (Treeview)
columns = ("desc", "qty", "price", "amount")
tree = ttk.Treeview(root, columns=columns, show="headings", height=8)

tree.heading("desc", text="Description")
tree.heading("qty", text="Qty")
tree.heading("price", text="Price")
tree.heading("amount", text="Amount")

tree.column("desc", width=200)
tree.column("qty", width=60, anchor="center")
tree.column("price", width=90, anchor="e")
tree.column("amount", width=100, anchor="e")

tree.pack(pady=(10, 5), padx=20, fill="x")

# --- අලුතින් එක් කරන ලද "Delete Selected Item" බොත්තම ---
tk.Button(root, text="❌ Delete Selected Item", bg="#f59e0b", fg="white", font=("Helvetica", 9, "bold"), command=delete_selected_item).pack(pady=(0, 15))

# Remarks and Terms sections (Optional) - appear only if filled
tk.Label(root, text="Remarks (Optional):", font=("Helvetica",10,"bold"), fg="#632c8b").pack(anchor="w", padx=20)
remarks_text = tk.Text(root, height=4, width=60)
remarks_text.pack(padx=20, pady=(0,10))

tk.Label(root, text="Terms & Conditions (Optional):", font=("Helvetica",10,"bold"), fg="#632c8b").pack(anchor="w", padx=20)
terms_text = tk.Text(root, height=4, width=60)
terms_text.pack(padx=20, pady=(0,10))

# 4. Generate සහ Clear බොත්තම්
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="🗑️ Clear All", bg="#ef4444", fg="white", font=("Helvetica", 10, "bold"), command=clear_all).grid(row=0, column=0, padx=10)
tk.Button(frame_buttons, text="📄 Generate Quotation PDF", bg="#632c8b", fg="white", font=("Helvetica", 10, "bold"), command=create_pdf).grid(row=0, column=1, padx=10)

# මෘදුකාංගය Run කිරීම
root.mainloop()