import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet

# --- SMART HARDWARE SWITCH ---
try:
    import RPi.GPIO as GPIO
    IS_PI = True
    DOOR_PIN = 18 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DOOR_PIN, GPIO.OUT)
except (ImportError, RuntimeError):
    # This part runs if you are on Windows/Mac
    IS_PI = False
    print("Running in SIMULATION MODE (No Raspberry Pi detected)")

# --- SECURITY SETUP ---
key = Fernet.generate_key()
cipher_suite = Fernet(key)
CORRECT_PIN = "1234" 

class PiDoorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Entry (Simulated)")
        self.root.geometry("400x350")

        tk.Label(root, text="ENTER SECURITY PIN", font=("Arial", 14)).pack(pady=10)
        self.entry = tk.Entry(root, show="*", font=("Arial", 18), justify='center')
        self.entry.pack(pady=10)

        self.status = tk.Label(root, text="STATUS: LOCKED", fg="red", font=("Arial", 16, "bold"))
        self.status.pack(pady=20)

        self.unlock_btn = tk.Button(root, text="UNLOCK DOOR", bg="green", fg="white", 
                                   height=2, width=20, command=self.handle_auth)
        self.unlock_btn.pack(pady=10)

    def handle_auth(self):
        if self.entry.get() == CORRECT_PIN:
            self.entry.delete(0, tk.END)
            self.set_door_state("OPEN")
            self.root.after(5000, lambda: self.set_door_state("CLOSE"))
        else:
            messagebox.showerror("Error", "Wrong PIN")
            self.entry.delete(0, tk.END)

    def set_door_state(self, state):
        msg = cipher_suite.encrypt(state.encode())
        command = cipher_suite.decrypt(msg).decode()
        
        if command == "OPEN":
            if IS_PI: GPIO.output(DOOR_PIN, GPIO.HIGH)
            self.status.config(text="STATUS: UNLOCKED", fg="green")
            self.unlock_btn.config(state="disabled")
            print("[EVENT] Door Opened")
        else:
            if IS_PI: GPIO.output(DOOR_PIN, GPIO.LOW)
            self.status.config(text="STATUS: LOCKED", fg="red")
            self.unlock_btn.config(state="normal")
            print("[EVENT] Door Locked")

# Start App
root = tk.Tk()
app = PiDoorApp(root)
root.mainloop()

# Clean up only if on Pi
if IS_PI: GPIO.cleanup()
