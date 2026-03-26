import tkinter as tk

class AutoLockBluePanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto-Lock Secure Panel")
        self.root.geometry("350x550") 
        
        # Brighter Blue Background
        self.bg_color = "#0095ff"  
        self.root.configure(bg=self.bg_color)

        self.pin = ""
        self.correct_pin = "1234"
        self.is_open = False

        # 1. TOP STATUS INDICATOR
        self.indicator = tk.Label(root, text="Door Locked", font=("Arial", 16, "bold"),
                                 bg="#00264C", fg="#ff4d4d", height=3, width=30)
        self.indicator.pack(pady=20)

        # 2. PIN DISPLAY SCREEN (Centered dots)
        self.display = tk.Label(root, text="----", font=("Courier", 30),
                               bg="#00509d", fg="#00ff00", width=10, anchor="center")
        self.display.pack(pady=10)

        # 3. KEYPAD GRID
        self.grid_frame = tk.Frame(root, bg=self.bg_color)
        self.grid_frame.pack(pady=20)

        buttons = ['1','2','3','4','5','6','7','8','9','CLR','0','OK']
        r, c = 0, 0
        for btn in buttons:
            btn_color = "#004080" 
            if btn == 'CLR': btn_color = "#c0392b"
            if btn == 'OK': btn_color = "#27ae60"
            
            tk.Button(self.grid_frame, text=btn, width=8, height=3, 
                      bg=btn_color, fg="white", font=("Arial", 10, "bold"),
                      command=lambda x=btn: self.handle_press(x)).grid(row=r, column=c, padx=4, pady=4)
            c += 1
            if c > 2:
                c = 0
                r += 1

    def handle_press(self, key):
        if self.is_open: return 

        if key == 'CLR':
            self.pin = ""
        elif key == 'OK':
            if self.pin == self.correct_pin:
                self.unlock_sequence()
            else:
                self.indicator.config(text="ACCESS DENIED", bg="#ff0000", fg="white")
                self.root.after(1000, self.lock_system)
            self.pin = ""
        elif len(self.pin) < 4:
            self.pin += key
        
        self.display.config(text="*" * len(self.pin) if self.pin else "----")

    def unlock_sequence(self):
        self.is_open = True
        self.indicator.config(text="DOOR OPEN", bg="#00ff00", fg="#004d00")
        print("[GPIO] Relay open")
        self.root.after(4000, self.lock_system)

    def lock_system(self):
        self.is_open = False
        # Returning to the Deep Dark Blue theme for Locked state
        self.indicator.config(text="Door Locked", bg="#00264C", fg="#ff4d4d")
        print("[GPIO] Relay closed")

# Start the application
root = tk.Tk()
app = AutoLockBluePanel(root)
root.mainloop()
