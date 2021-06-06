import tkinter as tk
from tkinter import ttk as ttk

class Callback_App:
    def __init__(self, master):
        self.button1 = ttk.Button(master, text = "Click me", command = self.callback)
        self.label = ttk.Label(master)
        self.button1.pack()
        self.label.pack()

    def callback(self):
        self.label.config(text = "Clicked")

def main():
    root = tk.Tk()
    app = Callback_App(root)
    root.mainloop()

if __name__ == "__main__":main()