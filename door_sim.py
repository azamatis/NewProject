import tkinter as tk
from tkinter import messagebox

class SimpleKeypad:
    def __init__(self, root):
        self.root = root
        self.root.title("Keypad Test")
        self.root.geometry("300x450") # Fixed size
        
        self.code = ""
        
        # 1. THE DISPLAY (Shows dots)
        self.label = tk.Label(root, text="ENTER PIN", font=("Arial", 18), pady=20)
        self.label.pack()

        # 2. THE BUTTON HOLDER (The Frame)
        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        # 3. CREATE BUTTONS 1-9
        buttons = [
            '1', '2', '3',
            '4', '5', '6',
            '7', '8', '9',
            'C', '0', 'OK'
        ]

        row = 0
        col = 0
        for b in buttons:
            # This creates the button and places it in the grid
            cmd = lambda x=b: self.press(x)
            tk.Button(self.frame, text=b, width=8, height=3, 
                      command=cmd, bg="#eeeeee").grid(row=row, column=col, padx=2, pady=2)
            
            col += 1
            if col > 2:
                col = 0
                row += 1

    def press(self, key):
        if key == 'C':
            self.code = ""
        elif key == 'OK':
            if self.code == "1234":
                messagebox.showinfo("Success", "Door Unlocked!")
            else:
                messagebox.showerror("Denied", "Wrong PIN")
            self.code = ""
        else:
            if len(self.code) < 4:
                self.code += key
        
        # Update the screen
        self.label.config(text="*" * len(self.code) if self.code else "ENTER PIN")

# START
root = tk.Tk()
app = SimpleKeypad(root)
root.mainloop()
