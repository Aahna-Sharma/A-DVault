import tkinter as tk
from tkinter import ttk
import random

# ---------- Constants ----------
CHOICES = ["Rock", "Paper", "Scissors"]

# ---------- Game logic ----------
def decide_winner(player, computer):
    if player == computer:
        return "draw"
    # player wins cases
    wins = {
        "Rock": "Scissors",
        "Paper": "Rock",
        "Scissors": "Paper"
    }
    return "player" if wins[player] == computer else "computer"

# ---------- GUI app ----------
class RockPaperScissorsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rock • Paper • Scissors — AD VAULT Mini-Game")
        self.geometry("420x360")
        self.configure(bg="#1f1f2e")
        self.resizable(False, False)

        # Score and state
        self.player_score = 0
        self.computer_score = 0
        self.rounds_played = 0

        # StringVars for dynamic labels
        self.status_var = tk.StringVar(value="Choose Rock, Paper or Scissors to start")
        self.computer_var = tk.StringVar(value="Computer chose: —")
        self.score_var = tk.StringVar(value=self._score_text())

        self._create_widgets()
        self._style_widgets()

    def _create_widgets(self):
        pad = 12

        # Title
        title = tk.Label(self, text="Rock • Paper • Scissors", font=("Helvetica", 18, "bold"),
                         bg="#1f1f2e", fg="white")
        title.pack(pady=(20, 5))

        # Status
        status = tk.Label(self, textvariable=self.status_var, font=("Helvetica", 11),
                          bg="#1f1f2e", fg="lightgrey")
        status.pack(pady=(0, 10))

        # Computer choice
        comp_label = tk.Label(self, textvariable=self.computer_var, font=("Helvetica", 11),
                              bg="#1f1f2e", fg="lightgrey")
        comp_label.pack(pady=(0, 10))

        # Buttons frame
        btn_frame = tk.Frame(self, bg="#1f1f2e")
        btn_frame.pack(pady=5)

        # Create buttons for choices
        self.buttons = {}
        for i, choice in enumerate(CHOICES):
            b = tk.Button(btn_frame, text=choice, width=10, height=2,
                          font=("Helvetica", 11, "bold"), bg="#3a3a4d", fg="white",
                          activebackground="#5a5a78", relief="flat",
                          command=lambda c=choice: self.play(c))
            b.grid(row=0, column=i, padx=8, pady=8)
            b.bind("<Enter>", lambda e, btn=b: btn.configure(bg="#55556f"))
            b.bind("<Leave>", lambda e, btn=b: btn.configure(bg="#3a3a4d"))
            self.buttons[choice] = b

        # Result label
        result_label = tk.Label(self, textvariable=self.status_var, font=("Helvetica", 14, "bold"),
                                bg="#1f1f2e", fg="white")
        # We'll just reuse status_var for message; place it bigger below buttons
        result_label.pack(pady=(14, 6))

        # Score label
        score_label = tk.Label(self, textvariable=self.score_var, font=("Helvetica", 11),
                               bg="#1f1f2e", fg="lightgreen")
        score_label.pack(pady=(6, 8))

        # Bottom control frame
        ctrl_frame = tk.Frame(self, bg="#1f1f2e")
        ctrl_frame.pack(pady=(6, 12))

        # Reset button
        reset_btn = tk.Button(ctrl_frame, text="Reset Scores", command=self.reset_scores,
                              bg="#6b2f2f", fg="white", relief="flat", width=12)
        reset_btn.grid(row=0, column=0, padx=6)

        # Quit button
        quit_btn = tk.Button(ctrl_frame, text="Quit", command=self.quit,
                             bg="#2f4f2f", fg="white", relief="flat", width=8)
        quit_btn.grid(row=0, column=1, padx=6)

    def _style_widgets(self):
        # Some ttk style fallback for combability if used later
        style = ttk.Style()
        # Use a minimal style change if available
        try:
            style.configure("TNotebook", background="#1f1f2e")
        except Exception:
            pass

    def _score_text(self):
        return f"You: {self.player_score}    Computer: {self.computer_score}    Rounds: {self.rounds_played}"

    def play(self, player_choice):
        computer_choice = random.choice(CHOICES)
        self.computer_var.set(f"Computer chose: {computer_choice}")

        winner = decide_winner(player_choice, computer_choice)
        if winner == "draw":
            self.status_var.set("It's a draw!")
        elif winner == "player":
            self.player_score += 1
            self.status_var.set("You won this round! 🎉")
        else:
            self.computer_score += 1
            self.status_var.set("Computer wins this round!")

        self.rounds_played += 1
        self.score_var.set(self._score_text())

    def reset_scores(self):
        self.player_score = 0
        self.computer_score = 0
        self.rounds_played = 0
        self.status_var.set("Scores reset. Play again!")
        self.computer_var.set("Computer chose: —")
        self.score_var.set(self._score_text())

if __name__ == "__main__":
    app = RockPaperScissorsApp()
    app.mainloop()
