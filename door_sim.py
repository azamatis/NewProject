import tkinter as tk
from tkinter import messagebox
import os

class AdminDoorPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Admin Panel")
        self.root.geometry("350x580")
        self.bg_color = "#0095ff"
        self.root.configure(bg=self.bg_color)

        self.pin_file = "secret_pin.txt"
        self.correct_pin = self.load_pin()
        self.input_buffer = ""
        self.is_open = False

        # --- MAIN UI ---
        self.indicator = tk.Label(root, text="Door Locked", font=("Arial", 16, "bold"),
                                 bg="#00264C", fg="#ff4d4d", height=3, width=30)
        self.indicator.pack(pady=20)

        self.display = tk.Label(root, text="----", font=("Courier", 30),
                               bg="#00509d", fg="#00ff00", width=10)
        self.display.pack(pady=10)

        # Keypad
        self.grid_frame = tk.Frame(root, bg=self.bg_color)
        self.grid_frame.pack(pady=10)
        self.create_keypad(self.grid_frame)

        # Admin Button
        self.admin_btn = tk.Button(root, text="UPDATE PIN SETTINGS", bg="#34495e", fg="white",
                                  font=("Arial", 10, "bold"), width=25, height=2,
                                  command=self.open_admin_screen)
        self.admin_btn.pack(pady=10)

    def load_pin(self):
        if os.path.exists(self.pin_file):
            with open(self.pin_file, "r") as f: return f.read().strip()
        return "1234"

    def create_keypad(self, parent):
        buttons = ['1','2','3','4','5','6','7','8','9','CLR','0','OK']
        r, c = 0, 0
        for btn in buttons:
            color = "#004080"
            if btn == 'CLR': color = "#c0392b"
            if btn == 'OK': color = "#27ae60"
            tk.Button(parent, text=btn, width=8, height=3, bg=color, fg="white",
                      font=("Arial", 10, "bold"), command=lambda x=btn: self.handle_press(x)).grid(row=r, column=c, padx=4, pady=4)
            c += 1
            if c > 2: c = 0; r += 1

    def handle_press(self, key):
        if key == 'CLR': self.input_buffer = ""
        elif key == 'OK': self.check_auth()
        elif len(self.input_buffer) < 4: self.input_buffer += key
        self.display.config(text="*" * len(self.input_buffer) if self.input_buffer else "----")

    def check_auth(self):
        if self.input_buffer == self.correct_pin:
            self.is_open = True
            self.indicator.config(text="ACCESS GRANTED", bg="#00ff00", fg="#004d00")
            self.root.after(5000, self.lock_system)
        else:
            self.indicator.config(text="WRONG PIN", bg="red", fg="white")
            self.root.after(1000, self.lock_system)
        self.input_buffer = ""

    def lock_system(self):
        self.is_open = False
        self.indicator.config(text="Door Locked", bg="#00264C", fg="#ff4d4d")

    # --- NEW SCREEN LOGIC ---
    def open_admin_screen(self):
        if not self.is_open:
            messagebox.showwarning("Security", "You must unlock the door first!")
            return

        # Create New Window
        self.admin_win = tk.Toplevel(self.root)
        self.admin_win.title("PIN Update")
        self.admin_win.geometry("300x250")
        self.admin_win.configure(bg="#00509d")

        tk.Label(self.admin_win, text="Enter New 4-Digit PIN:", bg="#00509d", fg="white").pack(pady=20)
        self.new_pin_entry = tk.Entry(self.admin_win, font=("Arial", 20), justify='center', width=10)
        self.new_pin_entry.pack(pady=10)

        tk.Button(self.admin_win, text="SAVE NEW PIN", bg="#27ae60", fg="white", 
                  command=self.save_new_pin).pack(pady=20)

    def save_new_pin(self):
        new_val = self.new_pin_entry.get()
        if len(new_val) == 4 and new_val.isdigit():
            self.correct_pin = new_val
            with open(self.pin_file, "w") as f: f.write(new_val)
            messagebox.showinfo("Success", f"PIN updated to: {new_val}")
            self.admin_win.destroy() # Close the admin window
            self.lock_system()       # Re-lock the door
        else:
            messagebox.showerror("Error", "PIN must be 4 numbers!")

root = tk.Tk()
app = AdminDoorPanel(root)
root.mainloop()
