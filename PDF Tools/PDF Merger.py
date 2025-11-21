# pdf_merger_gui.py
import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger

class PDFMergerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PDF Merger")
        self.geometry("480x420")
        self.resizable(False, False)
        self.configure(bg="#f4f7ff")

        self.pdf_list = []

        self._setup_ui()

    def _setup_ui(self):
        header = tk.Frame(self, bg="#2575fc", height=70)
        header.pack(fill="x")
        tk.Label(header, text="PDF Merger", bg="#2575fc", fg="white",
                 font=("Segoe UI", 18, "bold")).pack(pady=18)

        body = tk.Frame(self, bg="white")
        body.place(x=20, y=90, width=440, height=260)

        tk.Label(body, text="Selected PDF files:", font=("Segoe UI", 11),
                 bg="white").place(x=10, y=10)

        # listbox showing selected PDFs
        self.listbox = tk.Listbox(body, width=55, height=10, bd=0, bg="#eef2ff")
        self.listbox.place(x=10, y=40)

        # add & remove buttons
        add_btn = tk.Button(body, text="Add PDF", bg="#28c76f", fg="white",
                            font=("Segoe UI", 10, "bold"), bd=0,
                            command=self.add_pdf)
        add_btn.place(x=10, y=210, width=120, height=35)

        remove_btn = tk.Button(body, text="Remove Selected", bg="#ff6b6b", fg="white",
                               font=("Segoe UI", 10, "bold"), bd=0,
                               command=self.remove_selected)
        remove_btn.place(x=150, y=210, width=140, height=35)

        clear_btn = tk.Button(body, text="Clear All", bg="#f2f4f8", fg="#333",
                              font=("Segoe UI", 10, "bold"), bd=0,
                              command=self.clear_all)
        clear_btn.place(x=310, y=210, width=120, height=35)

        # merge button outside card
        merge_btn = tk.Button(self, text="Merge PDFs", bg="#2575fc", fg="white",
                              font=("Segoe UI", 12, "bold"), bd=0,
                              command=self.merge_pdfs)
        merge_btn.place(x=160, y=360, width=160, height=40)

    # ------------ BUTTON LOGIC ---------------

    def add_pdf(self):
        file_paths = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF Files", "*.pdf")]
        )
        for f in file_paths:
            self.pdf_list.append(f)
            self.listbox.insert(tk.END, f)

    def remove_selected(self):
        selected = self.listbox.curselection()
        if not selected:
            return
        for index in reversed(selected):
            del self.pdf_list[index]
            self.listbox.delete(index)

    def clear_all(self):
        self.pdf_list = []
        self.listbox.delete(0, tk.END)

    def merge_pdfs(self):
        if not self.pdf_list:
            messagebox.showerror("No PDFs", "Please add at least one PDF file.")
            return

        # ask output file name
        output = filedialog.asksaveasfilename(
            title="Save Merged PDF",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )
        if not output:
            return

        try:
            merger = PdfMerger()
            for pdf in self.pdf_list:
                merger.append(pdf)

            merger.write(output)
            merger.close()
            messagebox.showinfo("Success", f"Merged PDF saved as:\n{output}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to merge PDFs:\n{e}")

# Run the GUI
if __name__ == "__main__":
    PDFMergerGUI().mainloop()
