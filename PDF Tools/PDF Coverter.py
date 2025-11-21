# pdf_docx_converter_gui.py
import tkinter as tk
from tkinter import filedialog, messagebox
from pdf2docx import Converter
from docx2pdf import convert
import os

class PDFDOCXConverter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF & DOCX Converter")
        self.geometry("480x260")
        self.resizable(False, False)
        self.configure(bg="#f4f7ff")

        self.file_path = None

        self._build_ui()

    def _build_ui(self):
        header = tk.Frame(self, bg="#6a11cb", height=70)
        header.pack(fill="x")
        tk.Label(header, text="PDF ⇆ DOCX Converter", bg="#6a11cb", fg="white",
                font=("Segoe UI", 18, "bold")).pack(pady=18)

        card = tk.Frame(self, bg="white")
        card.place(x=20, y=90, width=440, height=140)

        # Pick file button
        pick_btn = tk.Button(
            card, text="Choose File", bg="#2575fc", fg="white",
            font=("Segoe UI", 12, "bold"), bd=0, command=self.pick_file
        )
        pick_btn.place(x=20, y=20, width=150, height=40)

        # Label to show file path
        self.path_label = tk.Label(
            card, text="No file selected", bg="white", fg="#444",
            font=("Segoe UI", 10), anchor="w"
        )
        self.path_label.place(x=190, y=28, width=230)

        # Convert button
        convert_btn = tk.Button(
            card, text="Convert", bg="#28c76f", fg="white",
            font=("Segoe UI", 12, "bold"), bd=0, command=self.convert_file
        )
        convert_btn.place(x=20, y=80, width=150, height=40)

        # Clear button
        clear_btn = tk.Button(
            card, text="Clear", bg="#f2f4f8", fg="#333",
            font=("Segoe UI", 12, "bold"), bd=0, command=self.clear
        )
        clear_btn.place(x=190, y=80, width=150, height=40)

    def pick_file(self):
        file = filedialog.askopenfilename(
            title="Select PDF or DOCX file",
            filetypes=[("PDF Files", "*.pdf"), ("Word Files", "*.docx")]
        )

        if file:
            self.file_path = file
            self.path_label.config(text=os.path.basename(file))

    def convert_file(self):
        if not self.file_path:
            messagebox.showerror("No File", "Please choose a file first.")
            return

        ext = os.path.splitext(self.file_path)[1].lower()

        try:
            if ext == ".pdf":
                output = self.file_path.replace(".pdf", ".docx")
                self.convert_pdf_to_docx(self.file_path, output)
                messagebox.showinfo("Success", f"Converted to:\n{output}")

            elif ext == ".docx":
                output = self.file_path.replace(".docx", ".pdf")
                self.convert_docx_to_pdf(self.file_path, output)
                messagebox.showinfo("Success", f"Converted to:\n{output}")

            else:
                messagebox.showerror("Invalid File", "Only PDF or DOCX files are supported.")
        except Exception as e:
            messagebox.showerror("Error", f"Conversion failed:\n{e}")

    def convert_pdf_to_docx(self, inp, out):
        cv = Converter(inp)
        cv.convert(out)
        cv.close()

    def convert_docx_to_pdf(self, inp, out):
        convert(inp, out)

    def clear(self):
        self.file_path = None
        self.path_label.config(text="No file selected")

if __name__ == "__main__":
    PDFDOCXConverter().mainloop()
