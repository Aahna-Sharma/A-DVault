import tkinter as tk
from tkinter import messagebox
import random
import string

def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation

    length_text = length_entry.get().strip()

    if not length_text.isdigit():
        messagebox.showwarning("Invalid Input", "Please enter a valid number.")
        return

    length = int(length_text)

    if length < 4 or length > 50:
        messagebox.showwarning("Invalid Length", "Choose a length between 4 and 50.")
        return

    password = "".join(random.choice(characters) for _ in range(length))
    
    result_entry.config(state="normal")
    result_entry.delete(0, tk.END)
    result_entry.insert(0, password)
    result_entry.config(state="readonly")

def copy_password():
    pwd = result_entry.get()
    if pwd:
        root.clipboard_clear()
        root.clipboard_append(pwd)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showwarning("No Password", "Generate a password first!")

def clear_all():
    length_entry.delete(0, tk.END)
    result_entry.config(state="normal")
    result_entry.delete(0, tk.END)
    result_entry.config(state="readonly")


# ------------------ GUI ---------------------
root = tk.Tk()
root.title("Password Generator")
# slightly taller so buttons won't be clipped on different DPI/font settings
root.geometry("420x300")
root.minsize(380, 280)
root.configure(bg="#f2f2f2")
root.resizable(False, False)

# use a content frame to keep central layout tidy
content = tk.Frame(root, bg="#f2f2f2")
content.pack(fill="both", expand=True, padx=16, pady=12)

title = tk.Label(content, text="Password Generator",
                 font=("Helvetica", 16, "bold"),
                 bg="#f2f2f2", fg="#333")
title.pack(pady=(4, 10))

tk.Label(content, text="Enter password length:",
         font=("Helvetica", 11),
         bg="#f2f2f2", fg="#444").pack()

length_entry = tk.Entry(content, font=("Helvetica", 12), justify="center", width=10)
length_entry.pack(pady=6)

generate_button = tk.Button(content,
                            text="Generate Password",
                            font=("Helvetica", 11, "bold"),
                            bg="#4a90e2",
                            fg="white",
                            activebackground="#357ABD",
                            width=20,
                            command=generate_password)
generate_button.pack(pady=(8, 12))

tk.Label(content, text="Generated Password:",
         font=("Helvetica", 11),
         bg="#f2f2f2", fg="#444").pack()

result_entry = tk.Entry(content, font=("Helvetica", 12),
                        justify="center", width=36, state="readonly")
result_entry.pack(pady=(6, 8))

# Buttons frame placed at bottom with extra padding so it never gets cut
btn_frame = tk.Frame(root, bg="#f2f2f2")
btn_frame.pack(side="bottom", fill="x", pady=(0, 14))

# Put buttons in columns 0 and 1 (start at 0)
copy_btn = tk.Button(btn_frame, text="Copy",
                     font=("Helvetica", 10, "bold"),
                     bg="#3aa374", fg="white",
                     width=12, command=copy_password)
copy_btn.grid(row=0, column=0, padx=(40, 10), pady=4)

clear_btn = tk.Button(btn_frame, text="Clear",
                      font=("Helvetica", 10, "bold"),
                      bg="#d9534f", fg="white",
                      width=12, command=clear_all)
clear_btn.grid(row=0, column=1, padx=10, pady=4)

# Add a spacer so buttons are centered-ish on wide windows
btn_frame.grid_columnconfigure(2, weight=1)

root.mainloop()
