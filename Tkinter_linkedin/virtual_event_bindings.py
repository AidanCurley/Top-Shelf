import tkinter as tk
from tkinter import ttk as ttk

class Callback_App:
    def __init__(self, master):
        self.entry = tk.Entry(master, width = 30)
        self.entry.pack()
        #  using pre-configured events
        self.entry.bind('<<Copy>>', lambda e: print('Copy'))
        self.entry.bind('<<Paste>>', lambda e: print('Paste'))
        # my defined events
        self.entry.event_add('<<OddNumber>>', '1', '3', '5', '7', '9')
        self.entry.bind('<<OddNumber>>', lambda e: print('It\'s odd'))
        # remove an event I defined
        self.entry.event_delete('<<OddNumber>>')


def main():
    root = tk.Tk()
    app = Callback_App(root)
    root.mainloop()

if __name__ == "__main__":main()