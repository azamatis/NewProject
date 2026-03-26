import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet

# --- SECURE LOGIC SETUP ---
key = Fernet.generate_key()
cipher_suite = Fernet(key)
CORRECT_PASSWORD = "Admin123"

class DoorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Door Control")
        self.root.geometry("300x250")

        # 1. Password Field
        tk.Label(root, text="Enter Security PIN:").pack(pady=10)
        self.pass_entry = tk.Entry(root, show="*") # Hides typing
        self.pass_entry.pack()

        # 2. Status Indicator
        self.status_label = tk.Label(root, text="Door is: CLOSED", fg="red", font=("Arial", 12, "bold"))
        self.status_label.pack(pady=20)

        # 3. Control Buttons
        tk.Button(root, text="OPEN DOOR", command=lambda: self.send_command("OPEN"), bg="green", fg="white").pack(side="left", padx=20)
        tk.Button(root, text="CLOSE DOOR", command=lambda: self.send_command("CLOSE"), bg="gray", fg="white").pack(side="right", padx=20)

    def send_command(self, action):
        user_input = self.pass_entry.get()

        # Step 1: Authentication
        if user_input != CORRECT_PASSWORD:
            messagebox.showerror("Access Denied", "Incorrect Security PIN!")
            return

        # Step 2: Encrypt & "Send" to Hardware Simulation
        encrypted_msg = cipher_suite.encrypt(action.encode())
        self.simulate_hardware(encrypted_msg)

    def simulate_hardware(self, encrypted_msg):
        # Step 3: Decrypt and Update GUI (Simulating GPIO Pin change)
        decrypted_action = cipher_suite.decrypt(encrypted_msg).decode()
        
        if decrypted_action == "OPEN":
            self.status_label.config(text="Door is: OPEN", fg="green")
            print("[SIMULATION] GPIO PIN 18 -> HIGH")
        else:
            self.status_label.config(text="Door is: CLOSED", fg="red")
            print("[SIMULATION] GPIO PIN 18 -> LOW")

# Start the App
root = tk.Tk()
app = DoorApp(root)
root.mainloop()
