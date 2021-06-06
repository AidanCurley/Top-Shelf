import tkinter as tk
from tkinter import ttk as ttk

# Mouse Events
# <Button> <ButtonPress>            ======> any button was pressed
# <Button-1> <ButtonPress-1> <1>    ======> Button 1 was pressed
# <ButtonRelease-1>                 ======> Button 1 was released
# <Double-Button-1>                 ======> Button 1 was double-clicked
# <Enter> <Leave>                   ======> The mouse enters/leaves the widget area
# <Motion>                          ======> When the mouse is moved

class Callback_App:
    def __init__(self, master):
        self.canvas = tk.Canvas(master, width = 640, height = 480,  background = 'white')
        self.canvas.pack()
        self.canvas.bind('<ButtonPress>', self.mouse_press)
        self.canvas.bind('<B1-Motion>', self.draw)

    def mouse_press(self, event):
        global previous
        previous = event
        print(f'type: {event.type}')
        print(f'widget: {event.widget}')
        print(f'num: {event.num}')
        print(f'x: {event.x}')
        print(f'y: {event.y}')
        print(f'x-screen: {event.x_root}')
        print(f'y-screen: {event.y_root}')

    def draw(self, event):
        global previous
        self.canvas.create_line(previous.x, previous.y, event.x, event.y, width = 2)
        previous = event


def main():
    root = tk.Tk()
    app = Callback_App(root)
    root.mainloop()

if __name__ == "__main__":main()