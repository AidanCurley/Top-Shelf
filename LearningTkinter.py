import tkinter as tk

root=tk.Tk()

def declare_buttons(image_number):
    global button_add, button_remove, button_quit
    button_quit = tk.Button(root, text="Exit Program", command=root.quit)
    button_remove = tk.Button(root, text="Remove bottle", command="")
    button_add = tk.Button(root, text="Add bottle", command="")
    return

def render_buttons():
    global button_add, button_remove, button_quit
    button_remove.grid(row=2, column=2, padx=5)
    button_add.grid(row=1, column=2, pady=5)
    button_quit.grid(row=1, column=0)
    return

def render_image_holder():
    global image_holder
    image_holder = tk.Label()
    image_holder.grid(row=0, column=0, columnspan=3)
    return

def main():
    root.title("Top Shelf")
    declare_buttons(0)
    render_buttons()
    render_image_holder()

    root.mainloop()


if __name__ == "__main__":
    main()
