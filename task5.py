import sqlite3
import tkinter as tk
from tkinter import messagebox

conn = sqlite3.connect('contacts.db')
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS contacts
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              phone TEXT,
              email TEXT,
              address TEXT)''')
conn.commit()

def add_contact(name, phone, email, address):
    c.execute("INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?)", (name, phone, email, address))
    conn.commit()
    messagebox.showinfo("Success", "Contact added successfully.")

def view_contacts():
    c.execute("SELECT id, name, phone FROM contacts")
    rows = c.fetchall()
    return rows

def search_contact(search_term):
    c.execute("SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ?", ('%' + search_term + '%', '%' + search_term + '%'))
    rows = c.fetchall()
    return rows

def update_contact(contact_id, name, phone, email, address):
    c.execute("UPDATE contacts SET name = ?, phone = ?, email = ?, address = ? WHERE id = ?", (name, phone, email, address, contact_id))
    conn.commit()
    messagebox.showinfo("Success", "Contact updated successfully.")

def delete_contact(contact_id):
    c.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    messagebox.showinfo("Success", "Contact deleted successfully.")

def clear_entries():
    entry_name.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_address.delete(0, tk.END)

def add_contact_ui():
    name = entry_name.get()
    phone = entry_phone.get()
    email = entry_email.get()
    address = entry_address.get()
    add_contact(name, phone, email, address)
    clear_entries()

def view_contacts_ui():
    contacts = view_contacts()
    listbox_contacts.delete(0, tk.END)
    for contact in contacts:
        listbox_contacts.insert(tk.END, contact)

def search_contact_ui():
    search_term = entry_search.get()
    contacts = search_contact(search_term)
    listbox_contacts.delete(0, tk.END)
    for contact in contacts:
        listbox_contacts.insert(tk.END, contact)

def update_contact_ui():
    selected_contact = listbox_contacts.get(tk.ACTIVE)
    if selected_contact:
        contact_id = selected_contact[0]
        name = entry_name.get()
        phone = entry_phone.get()
        email = entry_email.get()
        address = entry_address.get()
        update_contact(contact_id, name, phone, email, address)
        clear_entries()

def delete_contact_ui():
    selected_contact = listbox_contacts.get(tk.ACTIVE)
    if selected_contact:
        contact_id = selected_contact[0]
        delete_contact(contact_id)
        view_contacts_ui()


root = tk.Tk()
root.title("Contact Management System")

tk.Label(root, text="Name:").grid(row=0, column=0, padx=10, pady=10)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Phone:").grid(row=1, column=0, padx=10, pady=10)
entry_phone = tk.Entry(root)
entry_phone.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Email:").grid(row=2, column=0, padx=10, pady=10)
entry_email = tk.Entry(root)
entry_email.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Address:").grid(row=3, column=0, padx=10, pady=10)
entry_address = tk.Entry(root)
entry_address.grid(row=3, column=1, padx=10, pady=10)

tk.Button(root, text="Add Contact", command=add_contact_ui).grid(row=4, column=0, columnspan=2, pady=10)
tk.Button(root, text="Update Contact", command=update_contact_ui).grid(row=5, column=0, columnspan=2, pady=10)
tk.Button(root, text="Delete Contact", command=delete_contact_ui).grid(row=6, column=0, columnspan=2, pady=10)

tk.Label(root, text="Search:").grid(row=7, column=0, padx=10, pady=10)
entry_search = tk.Entry(root)
entry_search.grid(row=7, column=1, padx=10, pady=10)
tk.Button(root, text="Search", command=search_contact_ui).grid(row=7, column=2, padx=10, pady=10)

tk.Button(root, text="View All Contacts", command=view_contacts_ui).grid(row=8, column=0, columnspan=3, pady=10)

listbox_contacts = tk.Listbox(root, width=50)
listbox_contacts.grid(row=9, column=0, columnspan=3, padx=10, pady=10)


root.mainloop()

conn.close()
