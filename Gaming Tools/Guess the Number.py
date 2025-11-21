import tkinter as tk
import random

class GuessNumberApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Guess The Number")
        self.geometry("360x300")
        self.configure(bg="#f7f7fb")
        self.resizable(False, False)

        # Game state
        self.random_number = random.randint(1, 10)
        self.tries = 0

        # UI variables
        self.result_var = tk.StringVar(value="Try to guess the number (1 - 10)")
        self.tries_var = tk.StringVar(value="Tries: 0")
        self.last_guess_var = tk.StringVar(value="")

        self._create_widgets()

    def _create_widgets(self):
        pad_y = 10

        # Title
        title = tk.Label(self, text="Guess The Number", font=("Helvetica", 18, "bold"),
                         bg="#f7f7fb", fg="#2b2b3a")
        title.pack(pady=(18, 6))

        # Instruction
        instr = tk.Label(self, text="I have chosen a number between 1 and 10.",
                         font=("Helvetica", 10), bg="#f7f7fb", fg="#4b4b57")
        instr.pack()

        # Entry frame
        entry_frame = tk.Frame(self, bg="#f7f7fb")
        entry_frame.pack(pady=pad_y)

        vcmd = (self.register(self._validate_digit), "%P")
        self.entry = tk.Entry(entry_frame, font=("Helvetica", 14), width=8, justify="center",
                              validate="key", validatecommand=vcmd)
        self.entry.grid(row=0, column=0, padx=(0, 8))
        self.entry.focus()

        check_btn = tk.Button(entry_frame, text="Check", font=("Helvetica", 11, "bold"),
                              bg="#4a90e2", fg="white", activebackground="#357ABD",
                              width=8, command=self.check_guess)
        check_btn.grid(row=0, column=1)

        # Bind Enter key to check
        self.bind("<Return>", lambda event: self.check_guess())

        # Result label
        result_label = tk.Label(self, textvariable=self.result_var, font=("Helvetica", 12),
                                bg="#f7f7fb", fg="#333")
        result_label.pack(pady=(6, 4))

        # Last guess and tries
        info_frame = tk.Frame(self, bg="#f7f7fb")
        info_frame.pack(pady=(4, 10))

        last_guess_label = tk.Label(info_frame, textvariable=self.last_guess_var,
                                    font=("Helvetica", 10), bg="#f7f7fb", fg="#666")
        last_guess_label.grid(row=0, column=0, padx=8)
        tries_label = tk.Label(info_frame, textvariable=self.tries_var,
                               font=("Helvetica", 10, "bold"), bg="#f7f7fb", fg="#2e8b57")
        tries_label.grid(row=0, column=1, padx=8)

        # Control buttons
        ctrl_frame = tk.Frame(self, bg="#f7f7fb")
        ctrl_frame.pack(pady=8)

        new_btn = tk.Button(ctrl_frame, text="New Game", command=self.new_game,
                            bg="#6c6cff", fg="white", width=10)
        new_btn.grid(row=0, column=0, padx=6)

        reset_btn = tk.Button(ctrl_frame, text="Reset Score", command=self.reset_score,
                              bg="#d9534f", fg="white", width=10)
        reset_btn.grid(row=0, column=1, padx=6)

        quit_btn = tk.Button(self, text="Quit", command=self.quit, bg="#777", fg="white", width=36)
        quit_btn.pack(pady=(10, 8))

    def _validate_digit(self, new_text):
        # Allow empty string so user can delete; otherwise only digits 0-9
        if new_text == "":
            return True
        return new_text.isdigit()

    def check_guess(self):
        txt = self.entry.get().strip()
        if not txt:
            self.result_var.set("❗ Enter a number between 1 and 10.")
            return

        try:
            guess = int(txt)
        except ValueError:
            self.result_var.set("❌ Invalid input. Use numbers only.")
            self.entry.delete(0, tk.END)
            return

        if not (1 <= guess <= 10):
            self.result_var.set("⚠️ Number must be between 1 and 10.")
            self.entry.delete(0, tk.END)
            return

        self.tries += 1
        self.tries_var.set(f"Tries: {self.tries}")
        self.last_guess_var.set(f"Last guess: {guess}")
        self.entry.delete(0, tk.END)

        if guess == self.random_number:
            self.result_var.set(f"🎉 Correct! It was {self.random_number}.")
            # show a subtle success color change
            self._flash_bg("#dff0d8")
        elif guess < self.random_number:
            self.result_var.set("🔼 Too low — try a higher number.")
        else:
            self.result_var.set("🔽 Too high — try a lower number.")

    def new_game(self):
        self.random_number = random.randint(1, 10)
        self.tries = 0
        self.tries_var.set("Tries: 0")
        self.last_guess_var.set("")
        self.result_var.set("New number chosen. Good luck!")
        self.entry.delete(0, tk.END)
        self.entry.focus()

    def reset_score(self):
        # In this simple game 'reset' means reset tries and messages (not necessary to change secret)
        self.tries = 0
        self.tries_var.set("Tries: 0")
        self.result_var.set("Score reset. Keep guessing!")
        self.last_guess_var.set("")
        self.entry.delete(0, tk.END)
        self.entry.focus()

    def _flash_bg(self, color):
        # Temporary background flash on success (subtle)
        orig = self["bg"]
        self.configure(bg=color)
        self.after(220, lambda: self.configure(bg=orig))
        # Also flash inner frames/widgets by updating their bg if needed (kept simple)

if __name__ == "__main__":
    app = GuessNumberApp()
    app.mainloop()
