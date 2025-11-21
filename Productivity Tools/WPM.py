import tkinter as tk
import time
from tkinter import messagebox

# Original text (you can change this string)
text = "The quick brown fox jumps over the lazy dog"

class WPMApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WPM Typing Test")
        # increased height so reset button isn't cut
        self.geometry("640x470")
        self.configure(bg="#f5f8fb")
        self.resizable(False, False)

        self.start_time = None
        self.running = False

        self._build_ui()

    def _build_ui(self):
        # Title
        tk.Label(self, text="WPM Typing Test", font=("Segoe UI", 18, "bold"),
                 bg="#f5f8fb", fg="#001843").pack(pady=(12, 6))

        # Instruction frame
        instr = tk.Frame(self, bg="#f5f8fb")
        instr.pack(pady=(0, 6))
        tk.Label(instr, text="Type the sentence shown below as quickly and accurately as you can.",
                 font=("Segoe UI", 10), bg="#f5f8fb", fg="#000000").pack()

        # Sentence display
        sentence_frame = tk.Frame(self, bg="#ffffff", bd=1, relief="solid")
        sentence_frame.pack(padx=20, pady=(6, 12), fill="x")
        self.sentence_label = tk.Label(sentence_frame, text=text, font=("Segoe UI", 14),
                                       bg="#ffffff", fg="#000000", wraplength=580, justify="left")
        self.sentence_label.pack(padx=10, pady=12)

        # Entry and controls
        control_frame = tk.Frame(self, bg="#f5f8fb")
        control_frame.pack(pady=(0,8))

        # make typing box white and visible
        self.entry = tk.Entry(control_frame, font=("Segoe UI", 13), width=58, bd=1, relief="solid",
                              bg="white", fg="black")
        self.entry.grid(row=0, column=0, padx=(6,10), ipady=6)
        self.entry.config(state="disabled")

        btn_frame = tk.Frame(control_frame, bg="#f5f8fb")
        btn_frame.grid(row=0, column=1, padx=(0,6))

        self.start_btn = tk.Button(btn_frame, text="Start", width=10, bg="#144176", fg="white",
                                   font=("Segoe UI", 10, "bold"), command=self.start_test)
        self.start_btn.pack(pady=(0,6))

        self.finish_btn = tk.Button(btn_frame, text="Finish", width=10, bg="#0f6f37", fg="white",
                                    font=("Segoe UI", 10, "bold"), command=self.calculate_wpm, state="disabled")
        self.finish_btn.pack()

        # Info / results
        info_frame = tk.Frame(self, bg="#f5f8fb")
        info_frame.pack(pady=(10,0))

        self.time_var = tk.StringVar(value="Time: 0.00 s")
        tk.Label(info_frame, textvariable=self.time_var, font=("Segoe UI", 10), bg="#f5f8fb").grid(row=0, column=0, padx=12)

        self.words_var = tk.StringVar(value="Words: 0")
        tk.Label(info_frame, textvariable=self.words_var, font=("Segoe UI", 10), bg="#f5f8fb").grid(row=0, column=1, padx=12)

        self.wpm_var = tk.StringVar(value="WPM: 0.00")
        tk.Label(info_frame, textvariable=self.wpm_var, font=("Segoe UI", 10, "bold"), bg="#f5f8fb").grid(row=0, column=2, padx=12)

        # Result label (bigger)
        self.result_label = tk.Label(self, text="", font=("Segoe UI", 12), bg="#f5f8fb", fg="#2b3a55")
        self.result_label.pack(pady=(12,6))

        # Reset button — ensure no trailing () after pack so it doesn't crash
        reset_frame = tk.Frame(self, bg="#f5f8fb")
        reset_frame.pack(pady=(5,20))
        tk.Button(reset_frame, text="Reset", width=14, bg="#ba2323", fg="white",
                  font=("Segoe UI", 11, "bold"), command=self.reset).pack()

    def start_test(self):
        # prepare
        self.entry.config(state="normal")
        self.entry.delete(0, tk.END)
        self.entry.focus()
        self.start_time = time.time()
        self.running = True
        self.finish_btn.config(state="normal")
        self.start_btn.config(state="disabled")
        self.result_label.config(text="")
        self._update_timer()

    def _update_timer(self):
        if not self.running:
            return
        elapsed = time.time() - self.start_time
        self.time_var.set(f"Time: {elapsed:.2f} s")
        # estimate words while typing
        typed = self.entry.get()
        self.words_var.set(f"Words: {len(typed.split())}")
        self.after(100, self._update_timer)

    def calculate_wpm(self):
        if not self.start_time:
            return
        self.running = False
        end_time = time.time()
        typed = self.entry.get().strip()
        time_taken = end_time - self.start_time

        if time_taken <= 0:
            time_taken = 0.01

        words = len(typed.split())
        wpm = (words / time_taken) * 60

        # accuracy: compare characters
        original = text.strip()
        typed_chars = typed
        correct_chars = sum(1 for i, c in enumerate(typed_chars) if i < len(original) and c == original[i])
        total_chars = max(len(typed_chars), 1)
        accuracy = (correct_chars / total_chars) * 100

        self.time_var.set(f"Time: {time_taken:.2f} s")
        self.words_var.set(f"Words: {words}")
        self.wpm_var.set(f"WPM: {wpm:.2f}")

        self.result_label.config(text=f"Accuracy: {accuracy:.1f}%")

        self.finish_btn.config(state="disabled")
        self.start_btn.config(state="normal")
        self.entry.config(state="disabled")

    def reset(self):
        self.running = False
        self.start_time = None
        self.entry.config(state="disabled")
        self.entry.delete(0, tk.END)
        self.time_var.set("Time: 0.00 s")
        self.words_var.set("Words: 0")
        self.wpm_var.set("WPM: 0.00")
        self.result_label.config(text="")
        self.start_btn.config(state="normal")
        self.finish_btn.config(state="disabled")

if __name__ == "__main__":
    app = WPMApp()
    app.mainloop()
