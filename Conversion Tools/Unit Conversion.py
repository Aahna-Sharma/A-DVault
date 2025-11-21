# unit_converter_gui.py
import tkinter as tk
from tkinter import ttk, messagebox

# Optional image preview path (your uploaded file)
UPLOADED_IMAGE_PATH = "/mnt/data/2aeae6bd-2d72-4295-bb0d-4a0535a84e77.png"

class UnitConverterGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Unit Converter")
        self.geometry("460x360")
        self.resizable(False, False)
        self.configure(bg="#f3f6ff")

        self._setup_fonts()
        self._build_ui()

    def _setup_fonts(self):
        self.title_font = ("Segoe UI", 16, "bold")
        self.label_font = ("Segoe UI", 11)
        self.entry_font = ("Segoe UI", 14)
        self.result_font = ("Segoe UI", 18, "bold")
        self.btn_font = ("Segoe UI", 11, "bold")

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg="#2575fc", height=70)
        header.pack(fill="x")
        tk.Label(header, text="Unit Converter", bg="#2575fc", fg="white", font=self.title_font).pack(pady=18)

        # Main card
        card = tk.Frame(self, bg="white")
        card.place(x=20, y=80, width=420, height=220)

        # Category selection
        tk.Label(card, text="Category:", bg="white", font=self.label_font).place(x=16, y=14)
        self.category_var = tk.StringVar(value="Length")
        categories = ["Length", "Weight", "Temperature"]
        self.category_menu = ttk.Combobox(card, values=categories, state="readonly", textvariable=self.category_var)
        self.category_menu.place(x=110, y=12, width=150)
        self.category_menu.bind("<<ComboboxSelected>>", lambda e: self._update_unit_options())

        # From unit
        tk.Label(card, text="From unit:", bg="white", font=self.label_font).place(x=16, y=56)
        self.from_var = tk.StringVar()
        self.from_menu = ttk.Combobox(card, state="readonly", textvariable=self.from_var)
        self.from_menu.place(x=110, y=54, width=150)

        # To unit
        tk.Label(card, text="To unit:", bg="white", font=self.label_font).place(x=16, y=98)
        self.to_var = tk.StringVar()
        self.to_menu = ttk.Combobox(card, state="readonly", textvariable=self.to_var)
        self.to_menu.place(x=110, y=96, width=150)

        # Value entry
        tk.Label(card, text="Value:", bg="white", font=self.label_font).place(x=16, y=140)
        self.value_var = tk.StringVar(value="1")
        self.value_entry = tk.Entry(card, textvariable=self.value_var, font=self.entry_font, justify="center", bg="#e9edf8")
        self.value_entry.place(x=110, y=132, width=150, height=34)

        # Buttons
        convert_btn = tk.Button(card, text="Convert", bg="#28c76f", fg="white", font=self.btn_font,
                                bd=0, command=self.convert)
        convert_btn.place(x=280, y=50, width=110, height=40)

        clear_btn = tk.Button(card, text="Clear", bg="#f2f4f8", fg="#333", font=self.btn_font,
                              bd=0, command=self.clear)
        clear_btn.place(x=280, y=110, width=110, height=40)

        # Result area (big)
        self.result_label = tk.Label(self, text="", font=self.result_font, bg="#f3f6ff", fg="#0b3d91", anchor="center")
        self.result_label.place(x=20, y=310, width=420, height=36)

        # Initialize units for default category
        self._update_unit_options()

        # optional image preview (tk.PhotoImage supports PNG)
        try:
            if UPLOADED_IMAGE_PATH:
                img = tk.PhotoImage(file=UPLOADED_IMAGE_PATH)
                # scale down if too wide (PhotoImage.subsample requires integer factor)
                max_w = 100
                if img.width() > max_w:
                    factor = int(img.width() / max_w) + 1
                    img = img.subsample(factor, factor)
                img_lbl = tk.Label(card, image=img, bg="white")
                img_lbl.image = img
                img_lbl.place(x=360, y=8)
        except Exception:
            # ignore if the image can't be loaded; no Pillow required
            pass

        # Bind Enter key
        self.bind("<Return>", lambda e: self.convert())

        # focus the value entry
        self.value_entry.focus_set()

    def _update_unit_options(self):
        cat = self.category_var.get()
        if cat == "Length":
            units = ["cm", "m", "km"]
        elif cat == "Weight":
            units = ["g", "kg"]
        elif cat == "Temperature":
            units = ["C", "F"]
        else:
            units = []

        # set values for comboboxes and defaults
        self.from_menu['values'] = units
        self.to_menu['values'] = units
        if units:
            self.from_var.set(units[0])
            self.to_var.set(units[1] if len(units) > 1 else units[0])

    def convert(self):
        cat = self.category_var.get()
        frm = self.from_var.get()
        to = self.to_var.get()
        val_text = self.value_var.get().strip()

        # validate
        try:
            value = float(val_text)
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a numeric value.")
            return

        try:
            if cat == "Length":
                result_text = self._convert_length(value, frm, to)
            elif cat == "Weight":
                result_text = self._convert_weight(value, frm, to)
            elif cat == "Temperature":
                result_text = self._convert_temp(value, frm, to)
            else:
                result_text = "Unknown category."
        except Exception as e:
            result_text = f"Error: {e}"

        self.result_label.config(text=result_text)

    def _convert_length(self, value, frm, to):
        # convert everything to meters as intermediary
        to_m = {"cm": 0.01, "m": 1.0, "km": 1000.0}
        if frm not in to_m or to not in to_m:
            raise ValueError("Unsupported length unit.")
        meters = value * to_m[frm]
        converted = meters / to_m[to]
        return f"{value} {frm} = {converted:.6g} {to}"

    def _convert_weight(self, value, frm, to):
        # grams <-> kilograms
        to_g = {"g": 1.0, "kg": 1000.0}
        if frm not in to_g or to not in to_g:
            raise ValueError("Unsupported weight unit.")
        grams = value * to_g[frm]
        converted = grams / to_g[to]
        return f"{value} {frm} = {converted:.6g} {to}"

    def _convert_temp(self, value, frm, to):
        if frm == to:
            converted = value
        elif frm == "C" and to == "F":
            converted = (value * 9/5) + 32
        elif frm == "F" and to == "C":
            converted = (value - 32) * 5/9
        else:
            raise ValueError("Unsupported temperature conversion.")
        return f"{value:.2f}°{frm} = {converted:.2f}°{to}"

    def clear(self):
        self.value_var.set("")
        self.result_label.config(text="")

if __name__ == "__main__":
    app = UnitConverterGUI()
    app.mainloop()
