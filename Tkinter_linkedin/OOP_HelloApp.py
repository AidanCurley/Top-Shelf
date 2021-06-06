import tkinter as tk
from tkinter import ttk as ttk

class HelloApp:
    def __init__(self, master):
        self.label = ttk.Label(master, text = "Hello, Tkinter")
        self.label.grid(row = 0, column = 0, columnspan = 2)
        ttk.Button(master, text = "Dublin", command = self.say_hello_dublin).grid(row = 1, column = 0)
        ttk.Button(master, text = "Sydney", command = self.say_hello_sydney).grid(row = 1, column = 1)

    def say_hello_dublin(self):
        self.label.config(text = 'Dia dhuit, a chairde.')

    def say_hello_sydney(self):
        self.label.config(text = "G'day, mate!")

def main():
    root = tk.Tk()
    app = HelloApp(root)
    root.mainloop()

if __name__ == "__main__":main()