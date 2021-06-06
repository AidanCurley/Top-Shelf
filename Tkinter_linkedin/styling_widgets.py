import tkinter as tk
from tkinter import ttk as ttk

class Callback_App:
    def __init__(self, master):
        self.style = ttk.Style()
        self.style.configure('TButton', foreground = 'blue')
        # Making a new custom style which you can configure any of your buttons to
        self.style.configure('Alarm.TButton', foreground = 'orange')
        # Making the button styling react to different states
        self.style.map('Alarm.TButton', font = [['hover', ('Arial', 14, 'bold')]])
        # change the variable depending on the checkbox value using the command
        self.entry_box = ttk.Entry(master, width = 30)
        self.entry_box.insert(0, "Enter text here")
        self.enter_btn = ttk.Button(master, text = "Enter", command = self.empty_text)
        self.delete_btn = ttk.Button(master, text = "Delete", command = self.empty_text)
        self.delete_btn.config(style = 'Alarm.TButton')
        self.entry_box.pack()
        self.enter_btn.pack()
        self.delete_btn.pack()

    def empty_text(self):
        self.entry_box.delete(0, tk.END)


def main():
    root = tk.Tk()
    app = Callback_App(root)
    root.mainloop()

if __name__ == "__main__":main()