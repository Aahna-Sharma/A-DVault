import tkinter as tk
from tkinter import font
import math

# ---------------- Window ----------------
root = tk.Tk()
root.title("Modern Calculator")
root.geometry("360x560")   # a bit taller so display is visible
root.config(bg="#1e1e1e")
root.resizable(False, False)

# ---------------- Fonts ----------------
display_font = ("Segoe UI", 26, "bold")
button_font_big = ("Segoe UI", 18, "bold")
button_font_small = ("Segoe UI", 14, "bold")

# ---------------- State ----------------
expression = tk.StringVar(value="")

# ---------------- Display ----------------
display_frame = tk.Frame(root, bg="#1e1e1e")
display_frame.pack(fill="x", padx=12, pady=(12, 6))

display_label = tk.Label(
    display_frame,
    textvariable=expression,
    font=display_font,
    bg="#2b2b2b",
    fg="#ffffff",
    anchor="e",
    relief="flat",
    padx=16,
    pady=18,
    wraplength=320,  # wrap if expression gets long
)
display_label.pack(fill="both", expand=True)

# ---------------- Actions ----------------
def press(val):
    expression.set(expression.get() + str(val))

def clear_all():
    expression.set("")

def backspace():
    expression.set(expression.get()[:-1])

def calculate():
    expr = expression.get()
    # Basic replacements & safety
    expr = expr.replace("^", "**").replace("×", "*").replace("÷", "/").replace("π", str(math.pi))
    try:
        # safe-ish evaluation using math functions
        allowed = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
        allowed.update({
            "sqrt": math.sqrt,
            "ln": math.log,
            "log": math.log10,
            "factorial": math.factorial,
            "pi": math.pi,
            "e": math.e,
        })
        result = eval(expr, {"__builtins__": None}, allowed)
        # Format result neatly
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        expression.set(str(result))
    except Exception:
        expression.set("Error")

# ---------------- Button grid ----------------
btn_frame = tk.Frame(root, bg="#1e1e1e")
btn_frame.pack(padx=12, pady=(6,12), fill="both", expand=False)

# button spec: (text, bg_color, font_to_use, command_lambda)
specs = [
    [("C","#d9534f",button_font_small, clear_all),
     ("⌫","#f0ad4e",button_font_small, backspace),
     ("%","#5bc0de",button_font_small, lambda: press("%")),
     ("÷","#5bc0de",button_font_small, lambda: press("÷"))],
    [("7","#4a4a4a",button_font_big, lambda: press("7")),
     ("8","#4a4a4a",button_font_big, lambda: press("8")),
     ("9","#4a4a4a",button_font_big, lambda: press("9")),
     ("×","#5bc0de",button_font_small, lambda: press("×"))],
    [("4","#4a4a4a",button_font_big, lambda: press("4")),
     ("5","#4a4a4a",button_font_big, lambda: press("5")),
     ("6","#4a4a4a",button_font_big, lambda: press("6")),
     ("-","#5bc0de",button_font_small, lambda: press("-"))],
    [("1","#4a4a4a",button_font_big, lambda: press("1")),
     ("2","#4a4a4a",button_font_big, lambda: press("2")),
     ("3","#4a4a4a",button_font_big, lambda: press("3")),
     ("+","#5bc0de",button_font_small, lambda: press("+"))],
    [("0","#4a4a4a",button_font_big, lambda: press("0")),
     (".","#4a4a4a",button_font_big, lambda: press(".")),
     ("^","#4a4a4a",button_font_small, lambda: press("^")),
     ("=","#5cb85c",button_font_small, calculate)],
]

# create grid with consistent padding and sizes
for r, row in enumerate(specs):
    for c, (txt, bg, fnt, cmd) in enumerate(row):
        btn = tk.Button(
            btn_frame,
            text=txt,
            bg=bg,
            fg="white",
            font=fnt,
            bd=0,
            activebackground="#555555",
            activeforeground="white",
            command=cmd
        )
        btn.grid(row=r, column=c, padx=8, pady=8, ipadx=6, ipady=12, sticky="nsew")

# make columns expand evenly so buttons are square-ish
for i in range(4):
    btn_frame.grid_columnconfigure(i, weight=1)

# Bind Enter and keyboard keys
def on_key(event):
    key = event.keysym
    if key in ("Return", "KP_Enter"):
        calculate()
    elif key == "BackSpace":
        backspace()
    else:
        # allow digits and operators
        char = event.char
        if char in "0123456789.+-*/^()%":
            # map / * to our visual operators if you want
            if char == "/":
                press("÷")
            elif char == "*":
                press("×")
            else:
                press(char)

root.bind("<Key>", on_key)

# Give focus so keyboard works immediately
display_label.focus_set()

root.mainloop()
