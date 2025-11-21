import tkinter as tk
from tkinter import messagebox
import time
import threading
import sys

# Try import winsound (Windows). If not available, we'll use window.bell()
try:
    import winsound
    HAVE_WINSOUND = True
except Exception:
    HAVE_WINSOUND = False


class AlarmClockApp:
    def __init__(self, master):
        self.master = master
        master.title("Simple Alarm Clock")
        master.geometry("380x230")
        master.resizable(False, False)
        master.configure(bg="#f7f7fb")

        self.alarm_time = None
        self.alarm_running = False
        self.alarm_thread = None

        # Current time display
        self.current_time_var = tk.StringVar(value="")
        lbl_now = tk.Label(master, textvariable=self.current_time_var,
                           font=("Helvetica", 16, "bold"), bg="#f7f7fb")
        lbl_now.pack(pady=(12, 6))

        # Instruction
        tk.Label(master, text="Set alarm time (HH : MM : SS)",
                 font=("Helvetica", 11, "bold"),
                 bg="#f7f7fb").pack()

        # Time input (spinboxes)
        input_frame = tk.Frame(master, bg="#f7f7fb")
        input_frame.pack(pady=8)

        self.hh = tk.Spinbox(input_frame, from_=0, to=23, width=4,
                             format="%02.0f", font=("Helvetica", 12),
                             justify="center")
        self.hh.grid(row=0, column=0, padx=(0, 4))

        tk.Label(input_frame, text=":", bg="#f7f7fb",
                 font=("Helvetica", 12)).grid(row=0, column=1)

        self.mm = tk.Spinbox(input_frame, from_=0, to=59, width=4,
                             format="%02.0f", font=("Helvetica", 12),
                             justify="center")
        self.mm.grid(row=0, column=2, padx=(4, 4))

        tk.Label(input_frame, text=":", bg="#f7f7fb",
                 font=("Helvetica", 12)).grid(row=0, column=3)

        self.ss = tk.Spinbox(input_frame, from_=0, to=59, width=4,
                             format="%02.0f", font=("Helvetica", 12),
                             justify="center")
        self.ss.grid(row=0, column=4, padx=(4, 0))

        # Buttons Frame
        btn_frame = tk.Frame(master, bg="#f7f7fb")
        btn_frame.pack(pady=(8, 6))

        btn_font = ("Helvetica", 10, "bold")

        # Set Alarm button (blue)
        self.set_btn = tk.Button(
            btn_frame, text="Set Alarm", width=12, font=btn_font,
            bg="#1054a1", fg="white",
            activebackground="#0d447f",
            disabledforeground="white",
            command=self.set_alarm
        )
        self.set_btn.grid(row=0, column=0, padx=6)

        # Cancel Alarm button (red)
        self.cancel_btn = tk.Button(
            btn_frame, text="Cancel Alarm", width=12, font=btn_font,
            bg="#b51f1f", fg="white",
            activebackground="#8c1818",
            disabledforeground="white",
            command=self.cancel_alarm, state="disabled"
        )
        self.cancel_btn.grid(row=0, column=1, padx=6)

        # Stop Sound button (green)
        self.stop_btn = tk.Button(
            btn_frame, text="Stop Sound", width=12, font=btn_font,
            bg="#2f8f57", fg="white",
            activebackground="#256f44",
            disabledforeground="white",
            command=self.stop_sound, state="disabled"
        )
        self.stop_btn.grid(row=0, column=2, padx=6)

        # Status label
        self.status_var = tk.StringVar(value="No alarm set.")
        status = tk.Label(master, textvariable=self.status_var,
                          bg="#f7f7fb", fg="#333",
                          font=("Helvetica", 11))
        status.pack(pady=(6, 4))

        # Start updating clock
        self._update_clock()

    def _update_clock(self):
        now = time.strftime("%H:%M:%S")
        self.current_time_var.set(now)

        # check alarm
        if self.alarm_time and not self.alarm_running:
            if now == self.alarm_time:
                self._trigger_alarm()

        self.master.after(1000, self._update_clock)

    def set_alarm(self):
        h = self._safe_int(self.hh.get())
        m = self._safe_int(self.mm.get())
        s = self._safe_int(self.ss.get())

        if h is None or m is None or s is None:
            messagebox.showwarning("Invalid", "Please enter valid numbers for HH, MM and SS.")
            return

        self.alarm_time = f"{h:02d}:{m:02d}:{s:02d}"
        self.status_var.set(f"Alarm set for {self.alarm_time}")

        self.cancel_btn.config(state="normal")
        self.set_btn.config(state="disabled")

    def cancel_alarm(self):
        if self.alarm_time:
            if messagebox.askyesno("Cancel Alarm", f"Cancel alarm set for {self.alarm_time}?"):
                self.alarm_time = None
                self.status_var.set("Alarm cancelled.")
                self.cancel_btn.config(state="disabled")
                self.set_btn.config(state="normal")

    def _trigger_alarm(self):
        self.alarm_running = True
        self.status_var.set("Time is up!")
        self.stop_btn.config(state="normal")
        self.cancel_btn.config(state="disabled")

        self.alarm_thread = threading.Thread(
            target=self._play_alarm_sound_loop, daemon=True
        )
        self.alarm_thread.start()

    def _play_alarm_sound_loop(self):
        count = 0
        while self.alarm_running and count < 20:
            self._play_sound_once()
            count += 1
            time.sleep(1)

        self.alarm_running = False
        self.master.after(0, lambda: self.stop_btn.config(state="disabled"))
        self.master.after(0, lambda: self.set_btn.config(state="normal"))
        self.master.after(0, lambda: self.status_var.set("Alarm finished."))

    def _play_sound_once(self):
        if HAVE_WINSOUND and sys.platform.startswith("win"):
            try:
                winsound.Beep(2000, 800)
            except Exception:
                self.master.bell()
        else:
            self.master.bell()

    def stop_sound(self):
        if self.alarm_running:
            self.alarm_running = False
            self.status_var.set("Alarm stopped by user.")
            self.stop_btn.config(state="disabled")
            self.set_btn.config(state="normal")

        self.alarm_time = None
        self.cancel_btn.config(state="disabled")

    def _safe_int(self, s):
        try:
            return int(s)
        except:
            return None


if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmClockApp(root)
    root.mainloop()
