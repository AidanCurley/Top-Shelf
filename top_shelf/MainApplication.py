import tkinter as tk
import tkinter.ttk as ttk
from pprint import pprint

class TopShelfApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry('370x250')
        tk.Tk.iconbitmap(self,default='')
        tk.Tk.wm_title(self, "Top Shelf")

        style = ttk.Style()
        style.configure('W.TButton', font =('calibri', 12))

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # set up a dictionary to store the various frames
        self.frames = {}

        self.frames[HomePage] = HomePage(container, self)
        self.frames[AddBottlePage] = AddBottlePage(container, self)
        self.frames[EditBottlePage] = EditBottlePage(container, self)

        current_frame = self.frames[AddBottlePage]
        current_frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.show_frame(AddBottlePage)

    def show_frame(self, frame):
        current_frame = self.frames[frame]
        current_frame.tkraise()

class Error(Exception):
    """Base class for exceptions in this app"""
    pass


class InputError(Error):
    """ Exception raised when there is an error in the input
        Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class Bottle(object):
    def __init__(self, distillery, name, age, price):
        for character in distillery:
            if character.isdigit():
                raise InputError("distillery", "The distillery name can only include alphabetic characters.")
        self.distillery = distillery.title()
        self.name = str(name).title()
        try:
            self.price = "{:.2f}".format(float(price))
        except ValueError:
            raise InputError("price", "The price must be a number in the following format: ##.##")

        if age.isnumeric() or age == "N/A":
            self.age = age
        else:
            raise InputError("age", "The age must be a whole number.")

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        self.display = tk.Label(self, text="Welcome! You have X bottles in your collection.")
        self.display.grid(column=1,columnspan=6, padx=20, pady=40)
        self.show_col_btn = ttk.Button(self, text="Show Collection", style='W.TButton')
        self.show_col_btn.grid(row=4, column=1,columnspan=3, padx=(20, 0), pady=(20,0), ipady=5, sticky=tk.NSEW)
        self.find_btn = ttk.Button(self, text="Find a Bottle", style='W.TButton')
        self.find_btn.grid(row=4, column=4,columnspan=3, pady=(20,0), ipady=5, sticky=tk.NSEW)
        self.add_btn = ttk.Button(self, text="Add a Bottle", style='W.TButton')
        self.add_btn.grid(row=5, column=1,columnspan=2, padx=(20, 0), pady=(20,0), ipady=5)
        self.edit_btn = ttk.Button(self, text="Edit a Bottle", style='W.TButton')
        self.edit_btn.grid(row=5, column=3,columnspan=2, pady=(20,0), ipady=5)
        self.remove_btn = ttk.Button(self, text="Remove a Bottle", style='W.TButton')
        self.remove_btn.grid(row=5, column=5,columnspan=2, pady=(20,0), ipady=5)

class AddBottlePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        self.distillery_lbl = tk.Label(self, text="Distillery: ")
        self.distillery_lbl.grid(row=1, column=1, columnspan=2, padx=20, pady=(20, 0), sticky=tk.W)
        self.distillery_txt = tk.Entry(self)
        self.distillery_txt.grid(row=1, column=3, columnspan=3, pady=(20, 0), sticky=tk.W)

        self.name_lbl = tk.Label(self, text="Name: ")
        self.name_lbl.grid(row=2, column=1, columnspan=2, padx=20, pady=(10, 0), sticky=tk.W)
        self.name_txt = tk.Entry(self)
        self.name_txt.grid(row=2, column=3, columnspan=3, pady=(10, 0), sticky=tk.W)

        self.age_lbl = tk.Label(self, text="Age: ")
        self.age_lbl.grid(row=3, column=1, columnspan=2, padx=20, pady=(10, 0), sticky=tk.W)
        self.age_txt = tk.Entry(self)
        self.age_txt.grid(row=3, column=3, columnspan=3, pady=(10, 0), sticky=tk.W)

        self.price_lbl = tk.Label(self, text="Price: ")
        self.price_lbl.grid(row=4, column=1, columnspan=2, padx=20, pady=(10, 0), sticky=tk.W)
        self.price_txt = tk.Entry(self)
        self.price_txt.grid(row=4, column=3, columnspan=3, pady=(10, 0), sticky=tk.W)

        self.save_btn = ttk.Button(self, text="Save Details", command=self.save_entry)
        self.save_btn.grid(row=6, column=1,columnspan=3, padx=(20, 0), pady=(20,0), ipady=5, sticky=tk.NSEW)

        self.cancel_btn = ttk.Button(self, text="Cancel", command=self.cancel_entry)
        self.cancel_btn.grid(row=6, column=4,columnspan=3, pady=(20,0), ipady=5, sticky=tk.NSEW)

    def save_entry(self):
        distillery = self.distillery_txt.get()
        name = self.name_txt.get()
        age = self.age_txt.get() if self.age_txt.get() != "" else "N/A"
        price = self.price_txt.get()

        new_bottle = Bottle(distillery, name, age, price)
        print(vars(new_bottle))
        return

    def cancel_entry(self):
        return

class EditBottlePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Edit Bottle")
        label.pack(pady=10,padx=10)

app = TopShelfApp()
app.mainloop()