import tkinter as tk
from tkinter import ttk as ttk

class Callback_App:
    def __init__(self, master):
        # make a variable to hold a string
        self.spam = tk.StringVar()
        self.spam.set("It's spam!")
        # change the variable depending on the checkbox value using the command
        self.checkbutton1 = ttk.Checkbutton(master, variable = self.spam, onvalue = "It's spam!", offvalue = "Not spam", text = "Spam?", command = self.update_label)
        self.label = ttk.Label(master)
        self.checkbutton1.pack()
        self.label.pack()

    def update_label(self):
        self.label.config(text = self.spam.get())

def main():
    root = tk.Tk()
    app = Callback_App(root)
    root.mainloop()

if __name__ == "__main__":main()