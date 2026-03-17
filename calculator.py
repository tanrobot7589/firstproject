import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Avyan's Calculator")

        self.result_var = tk.StringVar()

        # Show welcome pop-up
        messagebox.showinfo("Welcome", "Welcome to Avyan's Calculator")

        self.create_widgets()

    def create_widgets(self):
        # Entry to display the result
        entry = tk.Entry(self.master, textvariable=self.result_var, font=('Arial', 16), bd=10, insertwidth=2, width=14, borderwidth=4)
        entry.grid(row=0, column=0, columnspan=4)

        # Buttons for digits and operations
        buttons = [
            '7', '8', '9', '/', 
            '4', '5', '6', '*', 
            '1', '2', '3', '-', 
            '0', '.', '=', '+'
        ]

        row_val = 1
        col_val = 0

        for button in buttons:
            tk.Button(self.master, text=button, padx=20, pady=20, font=('Arial', 16), command=lambda b=button: self.on_button_click(b)).grid(row=row_val, column=col_val)
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

    def on_button_click(self, button):
        if button == '=':
            try:
                expression = self.result_var.get()
                result = eval(expression)
                self.result_var.set(result)
                # Show result pop-up
                messagebox.showinfo("Result", "Avyan is Bongi")
            except Exception as e:
                self.result_var.set('Error')
        else:
            current_text = self.result_var.get()
            new_text = current_text + button
            self.result_var.set(new_text)

if __name__ == '__main__':
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()