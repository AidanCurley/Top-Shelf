import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import csv

class TopShelfApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        global bottles; global current_bottle
        bottles = self.read_csv_file()
        current_bottle = 0
        self.modes = {"edit" : 1, "remove" : 2, "show" : 3}
        self.mode = self.modes['edit']
        self.NA = 0

        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry('370x250')
        tk.Tk.iconbitmap(self,default='')
        tk.Tk.wm_title(self, "Top Shelf")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        print(f'Bottle from CSV are {bottles}')
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # set up a dictionary to store the various frames
        self.frames = {}
        # add our pages to the frames dictionary
        for F in (HomePage, AddBottlePage, EditBottlePage, RemoveBottleDetailPage, ShowCollectionPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky=tk.NSEW)
        self.show_frame(HomePage)

    def add_bottles_to_table(self, table):
        global bottles; global current_bottle
        # adding data to the treeview
        for bottle in bottles:
            table.insert('', tk.END, values=(bottle.distillery, bottle.name, bottle.age if bottle.age != self.NA else 'N/A', bottle.price))

    def add_details_to_entry_boxes(self, frame, bottle):
        """Add bottle details to entry boxes on the details screen."""

        frame.distillery_txt.insert(0, bottle.distillery)
        frame.name_txt.insert(0, bottle.name)
        frame.age_txt.insert(0, bottle.age if bottle.age != self.NA else 'N/A')
        frame.price_txt.insert(0, bottle.price)
        return

    def cancel_entry(self, frame):
        response = messagebox.askquestion("Confirm", "Are you sure you want to leave without saving?")
        if response == messagebox.YES:
            self.clear_entry_boxes(frame)
            self.show_frame(HomePage)
        return

    def clear_entry_boxes(self, frame):
        """ Clear contents of the entry boxes on the details screen."""
        frame.distillery_txt.delete(0, tk.END)
        frame.name_txt.delete(0, tk.END)
        frame.age_txt.delete(0, tk.END)
        frame.price_txt.delete(0, tk.END)
        return

    def edit_bottle(self):
        self.mode = self.modes['edit']
        self.show_frame(ShowCollectionPage)

    def get_details_from_entry_boxes(self, frame):
        global bottles; global current_bottle
        distillery = frame.distillery_txt.get()
        name = frame.name_txt.get()
        age = frame.age_txt.get() if frame.age_txt.get() != "" else "N/A"
        price = frame.price_txt.get()
        return (distillery, name, age, price)


    def on_closing(self):
        """ Ask user for confirmation when exiting the application"""

        global bottles; global current_bottle
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


    def read_csv_file(self):
        collection = []
        with open("bottles.csv", "r") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                bottle = Bottle(row[0], row[1], row[2], row[3])
                collection.append(bottle)
        print(collection)
        return collection

    def remove_bottle(self):
        self.mode = self.modes['remove']
        self.show_frame(ShowCollectionPage)

    def remove_entry_from_bottles(self):
        """Remove current bottle from the list of bottles."""
        global bottles; global current_bottle
        bottles.pop(current_bottle)
        messagebox.showinfo(title = "Confirmation", message = f'The bottle has been removed from your collection.')
        self.show_frame(HomePage)
        return

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

    def render_homepage_display(self, frame):
        global bottles; global current_bottle
        frame.display_string.set(f'Welcome! You have {len(bottles)} bottles in your collection.')
        frame.display = tk.Label(frame, textvariable = frame.display_string)
        frame.display.grid(column=1,columnspan=6, padx=20, pady=40)
        frame.show_col_btn = ttk.Button(frame, text="Show Collection", style='W.TButton', command = lambda: self.show_frame(ShowCollectionPage))
        frame.show_col_btn.grid(row=4, column=1,columnspan=3, padx=(20, 0), pady=(20,0), ipady=5, sticky=tk.NSEW)
        frame.find_btn = ttk.Button(frame, text="Find a Bottle", style='W.TButton')
        frame.find_btn.grid(row=4, column=4,columnspan=3, pady=(20,0), ipady=5, sticky=tk.NSEW)
        frame.add_btn = ttk.Button(frame, text="Add a Bottle", style='W.TButton', command = lambda: self.show_frame(AddBottlePage))
        frame.add_btn.grid(row=5, column=1,columnspan=2, padx=(20, 0), pady=(20,0), ipady=5)
        frame.edit_btn = ttk.Button(frame, text="Edit a Bottle", style='W.TButton', command = lambda: self.edit_bottle())
        frame.edit_btn.grid(row=5, column=3,columnspan=2, pady=(20,0), ipady=5)
        frame.remove_btn = ttk.Button(frame, text="Remove a Bottle", style='W.TButton', command = lambda: self.remove_bottle())
        frame.remove_btn.grid(row=5, column=5,columnspan=2, pady=(20,0), ipady=5)

    def render_save_buttons(self, frame):
        frame.save_btn = ttk.Button(frame, text="Save Details", command=lambda: self.save_entry(frame))
        frame.save_btn.grid(row=6, column=1,columnspan=3, padx=(20, 0), pady=(20,0), ipady=5, sticky=tk.NSEW)

        frame.cancel_btn = ttk.Button(frame, text="Cancel", command=lambda: self.cancel_entry(frame))
        frame.cancel_btn.grid(row=6, column=4,columnspan=3, pady=(20,0), ipady=5, sticky=tk.NSEW)

    def render_table(self, frame):
        columns = ('#1', '#2', '#3', '#4')
        frame.tree = ttk.Treeview(frame, columns=columns, show='headings')
        frame.tree.heading('#1', text='Distillery', command = lambda: self.sort_bottles_by("distillery"))
        frame.tree.heading('#2', text='Name', command = lambda: self.sort_bottles_by("name"))
        frame.tree.heading('#3', text='Age', command = lambda: self.sort_bottles_by("age"))
        frame.tree.heading('#4', text='Price', command = lambda: self.sort_bottles_by("price"))
        frame.tree.grid(row=0, column=0, sticky='nsew')
        frame.tree.bind("<Double-1>", lambda e: frame.on_double_click(e, self))
        frame.instructions_lbl = tk.Label(frame, textvariable = frame.instructions)

    def render_update_buttons(self, frame):
        frame.update_btn = ttk.Button(frame, text="Update", command=lambda: self.update_entry(frame))
        frame.update_btn.grid(row=6, column=1,columnspan=3, padx=(20, 0), pady=(20,0), ipady=5, sticky=tk.NSEW)

        frame.cancel_btn = ttk.Button(frame, text="Cancel", command=lambda: self.cancel_entry(frame))
        frame.cancel_btn.grid(row=6, column=4,columnspan=3, pady=(20,0), ipady=5, sticky=tk.NSEW)

    def render_remove_buttons(self, frame):
        frame.remove_btn = ttk.Button(frame, text="Remove", command=lambda: self.remove_entry_from_bottles())
        frame.remove_btn.grid(row=6, column=1,columnspan=3, padx=(20, 0), pady=(20,0), ipady=5, sticky=tk.NSEW)

        frame.cancel_btn = ttk.Button(frame, text="Cancel", command=lambda: self.cancel_entry(frame))
        frame.cancel_btn.grid(row=6, column=4,columnspan=3, pady=(20,0), ipady=5, sticky=tk.NSEW)

    def save_entry(self, frame):
        """ Add details from the entry boxes to the list of bottles."""
        global bottles; global current_bottle
        distillery, name, age, price = self.get_details_from_entry_boxes(frame)
        new_bottle = Bottle(distillery, name, age, price)
        bottles.append(new_bottle)
        messagebox.showinfo(title = "Confirmation", message = f'{new_bottle.distillery} {new_bottle.name} has been added to your collection.')
        self.clear_entry_boxes(frame)
        self.show_frame(HomePage)
        return

    def show_frame(self, frame):
        """Make the frame visible"""
        current_frame = self.frames[frame]
        current_frame.update_display(self)
        current_frame.tkraise()

    def sort_bottles_by(self, attribute):
        """sorts the list of bottles by the specified attribute"""
        global bottles; global current_bottle
        bottles = sorted(bottles, key=lambda bottle: getattr(bottle, attribute))
        self.show_frame(ShowCollectionPage)

    def update_entry(self, frame):
        """ Add details from the entry boxes to the list of bottles."""
        global bottles; global current_bottle
        distillery, name, age, price = self.get_details_from_entry_boxes(frame)
        new_bottle = Bottle(distillery, name, age, price)
        bottles.append(new_bottle)
        messagebox.showinfo(title = "Confirmation", message = f'{new_bottle.distillery} {new_bottle.name} has been added to your collection.')
        self.clear_entry_boxes(frame)
        bottles.pop(current_bottle)
        self.show_frame(HomePage)
        return



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
                raise InputError("distillery", "Invalid entry: The distillery name can only include alphabetic characters.")
        self.distillery = distillery.title()
        self.name = str(name).title()
        try:
            self.price = "{:.2f}".format(float(price))
            self.price = float(price)
        except ValueError:
            raise InputError("price", "Invalid entry: The price must be a number in the following format: ##.##")
        try:
            if age == "N/A":
                self.age = 0
            else:
                self.age = int(age)
        except:
            raise InputError("age", "Invalid entry: The age must be a whole number.")

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.display_string = tk.StringVar()
        self.update_display(controller)

    def update_display(self, controller):
        controller.render_homepage_display(self)
        tk.Tk.wm_title(controller, "Top Shelf")


class AddBottlePage(tk.Frame):
    def __init__(self, parent, controller):
        global bottles; global current_bottle
        tk.Frame.__init__(self,parent)
        self.update_display(controller)

    def update_display(self, controller):
        controller.render_bottle_details_layout(self)
        controller.render_save_buttons(self)
        tk.Tk.wm_title(controller, "Add a Bottle")

class EditBottlePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        global bottles; global current_bottle
        self.update_display(controller)

    def update_display(self, controller):
        global current_bottle
        controller.render_bottle_details_layout(self)
        controller.render_update_buttons(self)
        controller.add_details_to_entry_boxes(self, bottles[current_bottle])
        tk.Tk.wm_title(controller, "Edit a Bottle")

class RemoveBottleDetailPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        global bottles; global current_bottle
        self.update_display(controller)

    def update_display(self, controller):
        global bottles; global current_bottle
        controller.render_bottle_details_layout(self)
        controller.render_remove_buttons(self)
        controller.add_details_to_entry_boxes(self, bottles[current_bottle])
        tk.Tk.wm_title(controller, "Remove a Bottle")

class ShowCollectionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global bottles; global current_bottle
        self.instructions = tk.StringVar()
        self.update_display(controller)


    def update_display(self, controller):
        controller.render_table(self)
        controller.add_bottles_to_table(self.tree)
        tk.Tk.wm_title(controller, "My Collection")

    def on_double_click(self, event, controller):
        global bottles; global current_bottle
        item = self.tree.identify('item',event.x, event.y)
        vals = self.tree.item(self.tree.focus())
        for index, bottle in enumerate(bottles):
            if bottle.distillery == vals['values'][0] and bottle.name == vals['values'][1]:
                current_bottle = index
        if controller.mode == controller.modes['remove']:
            controller.show_frame(RemoveBottleDetailPage)
        else:
            controller.show_frame(EditBottlePage)

app = TopShelfApp()
app.mainloop()