import tkinter as tk
from tkinter import messagebox
import json
import os

class MultiUserDoorPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-User Secure Panel")
        self.root.geometry("400x600")
        self.bg_color = "#0095ff"
        self.root.configure(bg=self.bg_color)

        # --- DATA FILENAME ---
        self.db_file = "database.json"
        self.users = self.load_database()
        
        self.input_buffer = ""
        self.current_user = None
        self.is_open = False

        # --- UI ELEMENTS ---
        self.indicator = tk.Label(root, text="System Locked", font=("Arial", 16, "bold"),
                                 bg="#00264C", fg="#ff4d4d", height=3, width=35)
        self.indicator.pack(pady=20)

        self.display = tk.Label(root, text="----", font=("Courier", 30),
                               bg="#00509d", fg="#00ff00", width=12)
        self.display.pack(pady=10)

        self.grid_frame = tk.Frame(root, bg=self.bg_color)
        self.grid_frame.pack(pady=10)
        self.create_keypad(self.grid_frame)

        tk.Button(root, text="MANAGE USERS/PINS", bg="#34495e", fg="white",
                  font=("Arial", 10, "bold"), width=25, height=2,
                  command=self.open_admin_screen).pack(pady=15)

    def load_database(self):
        """Loads users and pins from the second file"""
        if os.path.exists(self.db_file):
            with open(self.db_file, "r") as f:
                return json.load(f)
        return {"admin": "1234"} # Fallback

    def save_database(self):
        """Saves current users/pins back to the second file"""
        with open(self.db_file, "w") as f:
            json.dump(self.users, f, indent=4)

    def create_keypad(self, parent):
        buttons = ['1','2','3','4','5','6','7','8','9','CLR','0','OK']
        r, c = 0, 0
        for btn in buttons:
            color = "#004080"
            if btn == 'CLR': color = "#c0392b"
            if btn == 'OK': color = "#27ae60"
            tk.Button(parent, text=btn, width=9, height=3, bg=color, fg="white",
                      font=("Arial", 10, "bold"), command=lambda x=btn: self.handle_press(x)).grid(row=r, column=c, padx=3, pady=3)
            c += 1
            if c > 2: c = 0; r += 1

    def handle_press(self, key):
        if key == 'CLR': self.input_buffer = ""
        elif key == 'OK': self.check_auth()
        elif len(self.input_buffer) < 4: self.input_buffer += key
        self.display.config(text="*" * len(self.input_buffer) if self.input_buffer else "----")

    def check_auth(self):
        # Check if the entered PIN exists for ANY user
        found_user = next((u for u, p in self.users.items() if p == self.input_buffer), None)
        
        if found_user:
            self.current_user = found_user
            self.is_open = True
            self.indicator.config(text=f"WELCOME {found_user.upper()}", bg="#00ff00", fg="#004d00")
            print(f"[LOG] {found_user} opened the door")
            self.root.after(4000, self.lock_system)
        else:
            self.indicator.config(text="INVALID PIN", bg="red", fg="white")
            self.root.after(1500, self.lock_system)
        self.input_buffer = ""

    def lock_system(self):
        self.is_open = False
        self.current_user = None
        self.indicator.config(text="System Locked", bg="#00264C", fg="#ff4d4d")

    def open_admin_screen(self):
        if not self.is_open:
            messagebox.showwarning("Security", "Unlock door first to manage settings!")
            return

        admin_win = tk.Toplevel(self.root)
        admin_win.title("User Management")
        admin_win.geometry("350x300")
        admin_win.configure(bg="#00509d")

        tk.Label(admin_win, text="Username to Update:", bg="#00509d", fg="white").pack(pady=5)
        user_entry = tk.Entry(admin_win, justify='center')
        user_entry.insert(0, self.current_user) # Auto-fill current user
        user_entry.pack(pady=5)

        tk.Label(admin_win, text="New 4-Digit PIN:", bg="#00509d", fg="white").pack(pady=5)
        pin_entry = tk.Entry(admin_win, justify='center')
        pin_entry.pack(pady=5)

        def update():
            u, p = user_entry.get().lower(), pin_entry.get()
            if u and len(p) == 4 and p.isdigit():
                self.users[u] = p
                self.save_database()
                messagebox.showinfo("Success", f"User {u} updated!")
                admin_win.destroy()
            else:
                messagebox.showerror("Error", "Invalid Name or 4-digit PIN")

        tk.Button(admin_win, text="ADD / UPDATE USER", bg="#27ae60", fg="white", command=update).pack(pady=20)

root = tk.Tk()
app = MultiUserDoorPanel(root)
root.mainloop()
