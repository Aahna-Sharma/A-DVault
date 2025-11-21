import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import os

class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("To-Do List")
        self.geometry("460x420")
        self.configure(bg="#f5f7fa")
        self.resizable(False, False)

        self.tasks = []
        self.tasks_file = "tasks.txt"

        self._create_widgets()
        self._load_tasks()

    def _create_widgets(self):
        # Header
        header = tk.Frame(self, bg="#f5f7fa")
        header.pack(fill="x", pady=(12, 6), padx=12)

        title = tk.Label(header, text="My To-Do List", font=("Arial", 16, "bold"),
                         bg="#f5f7fa", fg="#222")
        title.pack(side="left")

        # Input area
        input_frame = tk.Frame(self, bg="#f5f7fa")
        input_frame.pack(fill="x", padx=12, pady=(8, 10))

        self.entry = tk.Entry(input_frame, font=("Arial", 12))
        self.entry.pack(side="left", fill="x", expand=True, ipady=5, padx=(0,8))
        self.entry.focus()

        add_btn = tk.Button(input_frame, text="Add", width=10, bg="#2e86de", fg="white",
                            command=self.add_task)
        add_btn.pack(side="right")

        # Listbox + scrollbar
        list_frame = tk.Frame(self, bg="#f5f7fa")
        list_frame.pack(fill="both", expand=True, padx=12, pady=(0,10))

        self.listbox = tk.Listbox(list_frame, font=("Arial", 12), height=12,
                                  selectbackground="#d6eaf8", activestyle="none")
        self.listbox.pack(side="left", fill="both", expand=True, pady=6)

        scrollbar = tk.Scrollbar(list_frame, command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y", pady=6)
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Bindings
        self.listbox.bind("<Double-Button-1>", lambda e: self.edit_task())
        self.bind("<Delete>", lambda e: self.remove_task())
        self.bind("<Return>", lambda e: self.add_task())

        # Controls
        ctrl_frame = tk.Frame(self, bg="#f5f7fa")
        ctrl_frame.pack(fill="x", padx=12, pady=(0,12))

        edit_btn = tk.Button(ctrl_frame, text="Edit", width=10, command=self.edit_task)
        edit_btn.grid(row=0, column=0, padx=6, pady=6)

        remove_btn = tk.Button(ctrl_frame, text="Remove", width=12, bg="#e74c3c", fg="white",
                               command=self.remove_task)
        remove_btn.grid(row=0, column=1, padx=6, pady=6)

        clear_btn = tk.Button(ctrl_frame, text="Clear All", width=12, command=self.clear_all)
        clear_btn.grid(row=0, column=2, padx=6, pady=6)

        save_btn = tk.Button(ctrl_frame, text="Save", width=10, bg="#27ae60", fg="white",
                             command=self.save_tasks)
        save_btn.grid(row=0, column=3, padx=6, pady=6)

        export_btn = tk.Button(ctrl_frame, text="Export...", width=10, command=self.export_tasks)
        export_btn.grid(row=0, column=4, padx=6, pady=6)

        # Exit
        exit_btn = tk.Button(self, text="Exit", width=58, bg="#7f8c8d", fg="white", command=self.exit_app)
        exit_btn.pack(padx=12, pady=(0,12))

    # Task operations (simple & clear)
    def add_task(self):
        text = self.entry.get().strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter a task before adding.")
            return
        self.tasks.append(text)
        self.entry.delete(0, tk.END)
        self._refresh_listbox()

    def edit_task(self):
        try:
            idx = self.listbox.curselection()[0]
        except IndexError:
            messagebox.showinfo("Edit Task", "Select a task to edit (or double-click a task).")
            return

        old = self.tasks[idx]
        new = simpledialog.askstring("Edit Task", "Modify your task:", initialvalue=old, parent=self)
        if new is None:
            return
        new = new.strip()
        if not new:
            messagebox.showwarning("Warning", "Task cannot be empty.")
            return
        self.tasks[idx] = new
        self._refresh_listbox()
        self.listbox.selection_set(idx)
        self.listbox.see(idx)

    def remove_task(self):
        try:
            idx = self.listbox.curselection()[0]
        except IndexError:
            messagebox.showwarning("Warning", "Select a task to remove!")
            return

        task = self.tasks[idx]
        if messagebox.askyesno("Remove Task", f"Remove this task?\n\n{task}"):
            self.tasks.pop(idx)
            self._refresh_listbox()

    def clear_all(self):
        if not self.tasks:
            messagebox.showinfo("Clear All", "There are no tasks to clear.")
            return
        if messagebox.askyesno("Clear All", "Are you sure you want to remove all tasks?"):
            self.tasks.clear()
            self._refresh_listbox()

    def save_tasks(self):
        try:
            with open(self.tasks_file, "w", encoding="utf-8") as f:
                for t in self.tasks:
                    f.write(t.replace("\n", " ") + "\n")
            messagebox.showinfo("Save", f"Saved {len(self.tasks)} tasks to '{self.tasks_file}'.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save tasks:\n{e}")

    def export_tasks(self):
        if not self.tasks:
            messagebox.showinfo("Export", "No tasks to export.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                                            title="Export tasks to...")
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                for t in self.tasks:
                    f.write(t.replace("\n", " ") + "\n")
            messagebox.showinfo("Export", f"Exported {len(self.tasks)} tasks to:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not export tasks:\n{e}")

    def exit_app(self):
        if self.tasks:
            if messagebox.askyesno("Exit", "Save tasks before exiting?"):
                self.save_tasks()
        self.destroy()

    def _refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for i, t in enumerate(self.tasks, start=1):
            # Keep numbering, but keep it simple
            self.listbox.insert(tk.END, f"{i}. {t}")

    def _load_tasks(self):
        if os.path.exists(self.tasks_file):
            try:
                with open(self.tasks_file, "r", encoding="utf-8") as f:
                    lines = [line.strip() for line in f if line.strip()]
                self.tasks = [line for line in lines]
                self._refresh_listbox()
            except Exception:
                pass

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
