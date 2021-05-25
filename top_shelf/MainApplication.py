import tkinter as tk

class TopShelfApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry('600x600')
        tk.Tk.iconbitmap(self,default='')
        tk.Tk.wm_title(self, "Top Shelf")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # set up a dictionary to store the various frames
        self.frames = {}

        self.frames[HomePage] = HomePage(container, self)
        self.frames[AddBottlePage] = AddBottlePage(container, self)
        self.frames[EditBottlePage] = EditBottlePage(container, self)

        current_frame = self.frames[HomePage]
        current_frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(HomePage)

    def show_frame(self, frame):
        current_frame = self.frames[frame]
        current_frame.tkraise()


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="My collection")
        label.pack(pady=10,padx=10)


class AddBottlePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Add Bottle")
        label.pack(pady=10,padx=10)


class EditBottlePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Edit Bottle")
        label.pack(pady=10,padx=10)

app = TopShelfApp()
app.mainloop()