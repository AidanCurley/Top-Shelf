import tkinter as tk
from tkinter import Frame, messagebox
import tkinter.ttk as ttk
import csv

class TopShelfApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        global bottles
        bottles = []
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry('370x250')
        tk.Tk.iconbitmap(self,default='')
        tk.Tk.wm_title(self, "Top Shelf")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        style = ttk.Style()
        style.configure('W.TButton', font =('calibri', 12))

        bottles = self.read_csv_file()

        print(f'Bottle from CSV are {bottles}')
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # set up a dictionary to store the various frames
        self.frames = {}
        # add our pages to the frames dictionary
        for F in (HomePage, AddBottlePage, EditBottlePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.show_frame(HomePage)

    def read_csv_file(self):
        collection = []
        with open("bottles.csv", "r") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                bottle = Bottle(row[0], row[1], row[2], row[3])
                collection.append(bottle)
        print(collection)
        return collection

    def show_frame(self, frame):
        """Make the frame visible"""

        current_frame = self.frames[frame]
        current_frame.tkraise()

    def render_bottle_details_layout(self, frame):
        """Add the labels, entry boxes and buttons for bottle details to the frame"""

        frame.distillery_lbl = tk.Label(frame, text="Distillery: ")
        frame.distillery_lbl.grid(row=1, column=1, columnspan=2, padx=20, pady=(20, 0), sticky=tk.W)
        frame.distillery_txt = tk.Entry(frame)
        frame.distillery_txt.grid(row=1, column=3, columnspan=3, pady=(20, 0), sticky=tk.W)

        frame.name_lbl = tk.Label(frame, text="Name: ")
        frame.name_lbl.grid(row=2, column=1, columnspan=2, padx=20, pady=(10, 0), sticky=tk.W)
        frame.name_txt = tk.Entry(frame)
        frame.name_txt.grid(row=2, column=3, columnspan=3, pady=(10, 0), sticky=tk.W)

        frame.age_lbl = tk.Label(frame, text="Age: ")
        frame.age_lbl.grid(row=3, column=1, columnspan=2, padx=20, pady=(10, 0), sticky=tk.W)
        frame.age_txt = tk.Entry(frame)
        frame.age_txt.grid(row=3, column=3, columnspan=3, pady=(10, 0), sticky=tk.W)

        frame.price_lbl = tk.Label(frame, text="Price: ")
        frame.price_lbl.grid(row=4, column=1, columnspan=2, padx=20, pady=(10, 0), sticky=tk.W)
        frame.price_txt = tk.Entry(frame)
        frame.price_txt.grid(row=4, column=3, columnspan=3, pady=(10, 0), sticky=tk.W)

        frame.save_btn = ttk.Button(frame, text="Save Details", command=lambda: self.save_entry(frame))
        frame.save_btn.grid(row=6, column=1,columnspan=3, padx=(20, 0), pady=(20,0), ipady=5, sticky=tk.NSEW)

        frame.cancel_btn = ttk.Button(frame, text="Cancel", command=lambda: self.cancel_entry(frame))
        frame.cancel_btn.grid(row=6, column=4,columnspan=3, pady=(20,0), ipady=5, sticky=tk.NSEW)

    def save_entry(self, frame):
        """ Add details from the entry boxes to the list of bottles."""

        global bottles
        distillery = frame.distillery_txt.get()
        name = frame.name_txt.get()
        age = frame.age_txt.get() if frame.age_txt.get() != "" else "N/A"
        price = frame.price_txt.get()

        new_bottle = Bottle(distillery, name, age, price)
        bottles.append(new_bottle)
        frame.display_bottles()
        self.clear_entry_boxes(frame)
        return

    def clear_entry_boxes(self, frame):
        """ Clear contents of the entry boxes on the details screen."""

        frame.distillery_txt.delete(0, tk.END)
        frame.name_txt.delete(0, tk.END)
        frame.age_txt.delete(0, tk.END)
        frame.price_txt.delete(0, tk.END)
        return

    def cancel_entry(self, frame):
        response = messagebox.askquestion("Confirm", "Are you sure you want to leave without saving?")
        if response == messagebox.YES:
            self.clear_entry_boxes(frame)
            self.show_frame(HomePage)
        return

    def on_closing(self):
        """ Ask user for confirmation when exiting the application"""

        global bottles
        if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
            try:
                with open('bottles.csv', 'w+', newline ='') as file:
                    writer = csv.writer(file)
                    for bottle in bottles:
                        writer.writerow([bottle.distillery, bottle.name, bottle.age, bottle.price])
            except BaseException:
                messagebox.showwarning(title = 'Warning', message = "There's been a problem saving your session to memory.")
            else:
                messagebox.showinfo(title = 'Confirmation', message = 'Your session has been saved successfully! Goodbye.')
                self.destroy()


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
        messagebox.showerror(title=expression, message=message)

class Bottle(object):
    """ Object to hold bottle details
        Attributes:
        distillery -- the name of the distillery
        name -- the name of the bottle
        price -- the price of the bottle in pounds
        age -- the age of the bottle in whole years
    """

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
        global bottles
        self.display = tk.Label(self, text=f'Welcome! You have {len(bottles)} bottles in your collection.')
        self.display.grid(column=1,columnspan=6, padx=20, pady=40)
        self.show_col_btn = ttk.Button(self, text="Show Collection", style='W.TButton')
        self.show_col_btn.grid(row=4, column=1,columnspan=3, padx=(20, 0), pady=(20,0), ipady=5, sticky=tk.NSEW)
        self.find_btn = ttk.Button(self, text="Find a Bottle", style='W.TButton')
        self.find_btn.grid(row=4, column=4,columnspan=3, pady=(20,0), ipady=5, sticky=tk.NSEW)
        self.add_btn = ttk.Button(self, text="Add a Bottle", style='W.TButton', command = lambda: controller.show_frame(AddBottlePage))
        self.add_btn.grid(row=5, column=1,columnspan=2, padx=(20, 0), pady=(20,0), ipady=5)
        self.edit_btn = ttk.Button(self, text="Edit a Bottle", style='W.TButton', command = lambda: controller.show_frame(EditBottlePage))
        self.edit_btn.grid(row=5, column=3,columnspan=2, pady=(20,0), ipady=5)
        self.remove_btn = ttk.Button(self, text="Remove a Bottle", style='W.TButton')
        self.remove_btn.grid(row=5, column=5,columnspan=2, pady=(20,0), ipady=5)

class AddBottlePage(tk.Frame):
    def __init__(self, parent, controller):
        global bottles
        tk.Frame.__init__(self,parent)
        controller.render_bottle_details_layout(self)

    def display_bottles(self):
        global bottles
        for bottle in bottles:
            print(vars(bottle))
        return

class EditBottlePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        global bottles
        controller.render_bottle_details_layout(self)



app = TopShelfApp()
app.mainloop()