# BMI Calculator.py
import tkinter as tk
from tkinter import messagebox
import math

class SimpleBMI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BMI Calculator")
        self.geometry("420x330")
        self.configure(bg="#f7fbff")
        self.resizable(False, False)

        self._setup_styles()
        self._build_ui()

    def _setup_styles(self):
        self.title_font = ("Segoe UI", 18, "bold")
        self.label_font = ("Segoe UI", 11)
        self.entry_font = ("Segoe UI", 14)
        self.bmi_font = ("Segoe UI", 26, "bold")
        self.btn_font = ("Segoe UI", 11, "bold")

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg="#2575fc", height=70)
        header.pack(fill="x")
        tk.Label(header, text="BMI Calculator", bg="#2575fc", fg="white",
                 font=self.title_font).pack(pady=14)

        # Card
        card = tk.Frame(self, bg="white")
        card.place(x=20, y=90, width=380, height=200)

        padx = 14

        # --- Weight ---
        tk.Label(card, text="Weight (kg)", font=self.label_font, bg="white").place(x=padx, y=12)
        self.weight_var = tk.StringVar(value="70")
        w_entry = tk.Entry(
            card,
            textvariable=self.weight_var,
            font=self.entry_font,
            bd=0,
            relief="flat",
            justify="center",
            bg="#e6e6e6",   # GREY BACKGROUND (valid!)
            fg="#000000"
        )
        w_entry.place(x=padx, y=40, width=150, height=34)

        # --- Height ---
        tk.Label(card, text="Height (m)", font=self.label_font, bg="white").place(x=padx+190, y=12)
        self.height_var = tk.StringVar(value="1.75")
        h_entry = tk.Entry(
            card,
            textvariable=self.height_var,
            font=self.entry_font,
            bd=0,
            relief="flat",
            justify="center",
            bg="#e6e6e6",  # GREY BACKGROUND
            fg="#000000"
        )
        h_entry.place(x=padx+190, y=40, width=150, height=34)

        # Buttons (use only 6-digit hex / color names)
        calc_btn = tk.Button(
            card, text="Calculate", font=self.btn_font,
            bg="#28c76f", fg="white", bd=0, activebackground="#22a25a",
            command=self.calculate_bmi
        )
        calc_btn.place(x=padx, y=92, width=150, height=40)

        clear_btn = tk.Button(
            card, text="Clear", font=self.btn_font,
            bg="#f2f4f8", fg="#333333", bd=0, activebackground="#e6e9ef",
            command=self.clear_inputs
        )
        clear_btn.place(x=padx+190, y=92, width=150, height=40)

        # Results
        self.bmi_label = tk.Label(card, text="", font=self.bmi_font, bg="white", fg="#0b3d91")
        self.bmi_label.place(x=padx, y=150)

        self.cat_label = tk.Label(card, text="", font=self.label_font, bg="white")
        self.cat_label.place(x=padx+200, y=160)

        # Bind Enter
        self.bind("<Return>", lambda e: self.calculate_bmi())
        w_entry.focus_set()

    def calculate_bmi(self):
        try:
            weight = float(self.weight_var.get())
            height = float(self.height_var.get())
            if weight <= 0 or height <= 0:
                raise ValueError
        except Exception:
            messagebox.showerror("Invalid Input", "Enter positive numbers for weight & height.")
            return

        bmi = weight / (height * height)
        category, color = self.bmi_category(bmi)

        self.bmi_label.config(text=f"BMI: {bmi:.2f}")
        # color must be a valid color name or 6-digit hex
        self.cat_label.config(text=category, bg=color, fg="white", padx=10, pady=4)

    def clear_inputs(self):
        self.weight_var.set("")
        self.height_var.set("")
        self.bmi_label.config(text="")
        self.cat_label.config(text="", bg="white")

    def bmi_category(self, bmi):
        if bmi < 18.5:
            return "Underweight", "#4da6ff"
        elif bmi < 24.9:
            return "Normal", "#28c76f"
        elif bmi < 29.9:
            return "Overweight", "#ffb020"
        else:
            return "Obesity", "#ff6b6b"

if __name__ == "__main__":
    app = SimpleBMI()
    app.mainloop()
