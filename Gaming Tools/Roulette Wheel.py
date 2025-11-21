import tkinter as tk
import random

def spin_wheel():
    text = entry.get().strip()
    
    if not text:
        result_label.config(text="❌ Please enter some options!")
        return

    # Split user input into list
    options = [opt.strip() for opt in text.split(",") if opt.strip()]

    if len(options) < 2:
        result_label.config(text="⚠️ Enter at least 2 options separated by commas.")
        return

    # Random choice
    result = random.choice(options)
    result_label.config(text=f"🎉 The wheel selected: {result}", fg="#2b7a0b")


# GUI Window
root = tk.Tk()
root.title("Spin the Wheel")
root.geometry("450x330")
root.configure(bg="#f7f7f7")
root.resizable(False, False)

# Title
title = tk.Label(root,
                 text="Enter Options (comma-separated):",
                 font=("Helvetica", 14, "bold"),
                 bg="#f7f7f7",
                 fg="#333")
title.pack(pady=15)

# Entry Box
entry = tk.Entry(root,
                 font=("Helvetica", 13),
                 width=35,
                 justify="center")
entry.pack(pady=10)
entry.insert(0, "Bangalore, Mohali, Noida")  # default example

# Spin Button
spin_btn = tk.Button(root,
                     text="Spin the Wheel",
                     font=("Helvetica", 13, "bold"),
                     bg="#4a90e2",
                     fg="white",
                     activebackground="#357ABD",
                     width=18,
                     height=2,
                     relief="raised",
                     bd=3,
                     command=spin_wheel)
spin_btn.pack(pady=20)

# Result Label
result_label = tk.Label(root,
                        text="",
                        font=("Helvetica", 14, "bold"),
                        bg="#f7f7f7",
                        fg="#333")
result_label.pack(pady=10)

root.mainloop()
