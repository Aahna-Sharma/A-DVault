import tkinter as tk
import random

def toss_coin():
    result = random.choice(["Heads", "Tails"])
    result_label.config(text=f"Result: {result}")

# Window
win = tk.Tk()
win.title("Coin Toss")
win.geometry("330x260")
win.configure(bg="#f3f3f3")
win.resizable(False, False)

# Title Label
title_label = tk.Label(
    win, 
    text="Coin Toss Simulator",
    font=("Helvetica", 20, "bold"),
    bg="#f3f3f3",
    fg="#333"
)
title_label.pack(pady=15)

# Toss Button (simple styling)
toss_button = tk.Button(
    win,
    text="Toss Coin",
    font=("Helvetica", 14, "bold"),
    bg="#4a90e2",
    fg="white",
    activebackground="#357ABD",
    activeforeground="white",
    width=12,
    height=1,
    relief="raised",
    bd=3,
    command=toss_coin
)
toss_button.pack(pady=20)

# Result Label
result_label = tk.Label(
    win,
    text="Result: ",
    font=("Helvetica", 18),
    bg="#f3f3f3",
    fg="#444"
)
result_label.pack(pady=10)

win.mainloop()
