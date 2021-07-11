import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import csv


class Bottle(object):
    """ Class to hold bottle details
        Attributes:
        distillery -- the name of the distillery (string)
        name -- the name of the bottle (string)
        age -- the age of the bottle in whole years (integer)
        price -- the price of the bottle in pounds (float)
    """

    def __init__(self, distillery, name, age, price):
        # ensure that the distillery name contains only letters and the
        # first letter is uppercase as there are no whisky distilleries
        # in Scotland with numbers in the name
        for character in distillery:
            if character.isdigit():
                raise InputError("distillery", "Invalid entry: The distillery name can only include alphabetic characters.")
        if len(distillery) == 0:
            raise InputError("distillery", "Invalid entry: The distillery name cannot be blank.")
        self.distillery = distillery.title()

        # ensure the first letter of the bottle name is uppercase
        self.name = str(name).title()

        # ensure that the price is in the format ##.##
        try:
            self.price = "{:.2f}".format(float(price))
            self.price = round(float(price), 2)
        except ValueError:
            raise InputError("price", "Invalid entry: The price must be a number in the following format: ##.##")

        # ensure the age is a whole number or if it is 'N/A', convert to 0
        # for storage and sorting purposes
        try:
            if age == "N/A" or age == "":
                self.age = 0
            else:
                self.age = int(age)
        except:
            raise InputError("age", "Invalid entry: The age must be a whole number.")
        return


class Error(Exception):
    """ Base class for exceptions in this app.
        Will be extended by other classes
    """
    pass


class InputError(Error):
    """ Exception raised when there is an error in the input
        Attributes:
        expression -- input expression in which the error occurred (string)
        message -- explanation of the error (string)
    """

    def __init__(self, expression, message):
        messagebox.showerror(title=expression, message=message)
        return


class TopShelfApp(tk.Tk):
    """ Base class for the application.

        Contains the Frames that act as windows for different use cases
        Contains functions that can be accessed from one or more windows

        Attributes
        ---------------------------
        bottles: list
        list of bottle objects in the collection

        current_bottle: integer
        index of bottle currently used for display/editting purposes

        modes: dictionary
        dictionary of modes: edit, remove, show and their descriptions

        NA: integer
        stores 0 to be used when converting ages entered as "N/A" to 0

        frames: dictionary
        contains the frames which are used as different pages
            --   HomePage, AddBottlePage, EditBottlePage,
            --   RemoveBottlePage, ShowCollectionPage
    """

    def __init__(self, *args, **kwargs):
        # populate the bottles list from ,csv,set current bottle index = 0
        self.bottles = self.read_csv_file()
        self.current_bottle = 0
        # initialise the modes dictionary and set current mode to edit
        self.modes = {"edit" : "Double click a bottle to edit it", "remove" : "Double click a bottle to remove it from your collection", "show" : "Double click a bottle for more details"}
        self.current_mode= self.modes['edit']
        # initialise the constant NA
        self.NA = 0

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self,default='')
        tk.Tk.wm_title(self, "Top Shelf")

        # get application to run self.on_closing method when window is closed
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # initialise container as Frame to hold all other frames(windows)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # set up a dictionary to store the various frames
        # and add our pages to the frames dictionary
        self.frames = {}
        for F in (HomePage, AddBottlePage, EditBottlePage, FindBottlePage, RemoveBottlePage, ShowCollectionPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky=tk.NSEW)

        # display the homepage
        self.show_frame(HomePage)
        return

    def add_bottles_to_table(self, bottles, table):
        """ Adds bottles to a table

            Args:
            table ([type]): [description]
        """
        # adding data to the treeview
        for bottle in bottles:
            table.insert('', tk.END, values=(bottle.distillery, bottle.name, bottle.age if bottle.age != self.NA else 'N/A', bottle.price))
        return

    def add_details_to_entry_boxes(self, frame, bottle):
        """Renders bottle details to entry boxes on the details screen

            Args:
            frame (Frame): the frame where the details will be added
            bottle (Bottle): the Bottle object to be displayed
        """
        # insert the bottle's attributes into the entry widgets on the frame
        frame.distillery_txt.insert(0, bottle.distillery)
        frame.name_txt.insert(0, bottle.name)
        frame.age_txt.insert(0, bottle.age if bottle.age != self.NA else 'N/A')
        frame.price_txt.insert(0, bottle.price)
        return

    def cancel_entry(self, frame):
        """ Leaves the edit/enter/delete bottle page without saving changes

            Args:
            frame (Frame): the frame which will be cleared
        """
        #  display message asking for user confirmation
        response = messagebox.askquestion("Confirm", "Are you sure you want to leave without saving?")
        if response == messagebox.YES:
            self.show_frame(HomePage)
        return

    def clear_entry_boxes(self, frame):
        """ Clears contents of the entry boxes on the details screen

            Args:
            frame (Frame): the frame which will be cleared
        """
        # delete contents of entry widgets
        frame.distillery_txt.delete(0, tk.END)
        frame.name_txt.delete(0, tk.END)
        frame.age_txt.delete(0, tk.END)
        frame.price_txt.delete(0, tk.END)
        return

    def edit_bottle(self):
        """ Sets current_mode to edit and shows the entire collection
        """
        self.current_mode= self.modes['edit']
        self.show_frame(ShowCollectionPage)
        return

    def search_bottles_for_entry(self, search_term):
        """ Searches the list of bottles for a bottle whose distillery/name
            matches the search term

            Args:
            search_term (string): the string being searched for

            Returns:
            a list of bottles
        """
        return [x for x in self.bottles if x.distillery.startswith(search_term.title()) or x.name.startswith(search_term.title())]


    def get_details_from_entry_boxes(self, frame):
        """ Extracts details from entry widgets

            Args:
            frame (Frame): the frame containing the entry widgets

            Returns:
            a tuple of the entry details
        """
        distillery = frame.distillery_txt.get()
        name = frame.name_txt.get()
        # default value for age is "N/A" if no entry detexted
        age = frame.age_txt.get() if frame.age_txt.get() != "" else "N/A"
        price = frame.price_txt.get()
        return (distillery, name, age, price)


    def on_closing(self):
        """ Asks user for confirmation when exiting the application"""
        # if user says ok, try to save the contents of the list of bottles
        # to the csv. Display whether this has been successful or not
        # before completely shutting the application
        if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
            try:
                with open('bottles.csv', 'w+', newline ='') as file:
                    writer = csv.writer(file)
                    for bottle in self.bottles:
                        writer.writerow([bottle.distillery, bottle.name, bottle.age, bottle.price])
            except BaseException:
                messagebox.showwarning(title = 'Warning', message = "There's been a problem saving your session to memory.")
            else:
                messagebox.showinfo(title = 'Confirmation', message = 'Your session has been saved successfully! Goodbye.')
                self.destroy()
        return


    def read_csv_file(self):
        """ Reads the contents of bottles.csv into a list

            Returns:
            a list of Bottle objects
        """
        collection = []
        with open("bottles.csv", "r") as file:
            csv_reader = csv.reader(file)
            # read csv row by row
            for row in csv_reader:
                bottle = Bottle(row[0], row[1], row[2], row[3])
                collection.append(bottle)
        return collection

    def remove_bottle(self):
        """ Sets current_mode to remove and shows the entire collection
        """
        self.current_mode= self.modes['remove']
        self.show_frame(ShowCollectionPage)
        return

    def remove_entry_from_bottles(self):
        """ Deletes current bottle and displays the homepage
        """
        self.bottles.pop(self.current_bottle)
        messagebox.showinfo(title = "Confirmation", message = f'The bottle has been removed from your collection.')
        self.show_frame(HomePage)
        return

    def render_bottle_details_layout(self, frame):
        """ Renders the labels and entry boxes on the frame

            Args:
            frame (Frame): the frame which will be used
        """
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
        return

    def render_search_details_layout(self, frame):
        """ Renders the labels and entry boxes on the frame

            Args:
            frame (Frame): the frame which will be used
        """
        frame.search_txt = tk.Entry(frame)
        frame.search_txt.grid(row=3, column=0, columnspan=2, pady=(20, 0), sticky=tk.NSEW)

        # Every time a key is pressed in the search box, run the callback
        # function which searches for bottles whose distillery/name begin
        # with the term in the search box and filters the table accordingly
        frame.search_txt.bind('<KeyRelease>', (lambda _: frame.callback(frame.search_txt.get(), self)))
        return

    def render_search_buttons(self, frame):
        """ Renders search and cancel buttons

            Args:
            frame (Frame): the frame which will be used
        """
        frame.cancel_btn = ttk.Button(frame, text="Cancel", command=lambda: self.cancel_entry(frame))
        frame.cancel_btn.grid(row=3, column=1,columnspan=1, pady=(20,0), ipady=5, sticky=tk.NSEW)
        return

    def render_homepage_display(self, frame):
        """ Renders the labels, entry boxes and buttons on the homepage frame

            Args:
            frame (Frame): the frame which will be used
        """
        # renders the welcome message with the number of bottles in collection
        frame.display_string.set(f'Welcome! You have {len(self.bottles)} bottles in your collection.')
        frame.display = tk.Label(frame, textvariable = frame.display_string)
        frame.display.grid(column=1,columnspan=6, padx=20, pady=40)
        # add and render buttons
        frame.show_col_btn = ttk.Button(frame, text="Show Collection", style='W.TButton', command = lambda: self.show_collection())
        frame.show_col_btn.grid(row=4, column=1,columnspan=3, padx=(20, 0), pady=(20,0), ipady=5, sticky=tk.NSEW)
        frame.find_btn = ttk.Button(frame, text="Find a Bottle", style='W.TButton', command = lambda: self.show_frame(FindBottlePage))
        frame.find_btn.grid(row=4, column=4,columnspan=3, pady=(20,0), ipady=5, sticky=tk.NSEW)
        frame.add_btn = ttk.Button(frame, text="Add a Bottle", style='W.TButton', command = lambda: self.show_frame(AddBottlePage))
        frame.add_btn.grid(row=5, column=1,columnspan=2, padx=(20, 0), pady=(20,0), ipady=5)
        frame.edit_btn = ttk.Button(frame, text="Edit a Bottle", style='W.TButton', command = lambda: self.edit_bottle())
        frame.edit_btn.grid(row=5, column=3,columnspan=2, pady=(20,0), ipady=5)
        frame.remove_btn = ttk.Button(frame, text="Remove a Bottle", style='W.TButton', command = lambda: self.remove_bottle())
        frame.remove_btn.grid(row=5, column=5,columnspan=2, pady=(20,0), ipady=5)
        return

    def render_save_buttons(self, frame):
        """ Renders save and cancel buttons

            Args:
            frame (Frame): the frame which will be used
        """
        frame.save_btn = ttk.Button(frame, text="Save Details", command=lambda: self.save_entry(frame))
        frame.save_btn.grid(row=6, column=1,columnspan=3, padx=(20, 0), pady=(20,0), ipady=5, sticky=tk.NSEW)

        frame.cancel_btn = ttk.Button(frame, text="Cancel", command=lambda: self.cancel_entry(frame))
        frame.cancel_btn.grid(row=6, column=4,columnspan=3, pady=(20,0), ipady=5, sticky=tk.NSEW)
        return

    def render_table(self, frame):
        """ Renders a table to display bottle collection

            Args:
            frame (Frame): the frame where the table will be rendered
        """
        # Four columns, one for each atttribute
        columns = ('#1', '#2', '#3', '#4')
        frame.tree = ttk.Treeview(frame, columns=columns, show='headings')
        frame.tree.heading('#1', text='Distillery', command = lambda: self.sort_bottles_by("distillery", frame))
        frame.tree.heading('#2', text='Name', command = lambda: self.sort_bottles_by("name", frame))
        frame.tree.heading('#3', text='Age', command = lambda: self.sort_bottles_by("age", frame))
        frame.tree.heading('#4', text='Price', command = lambda: self.sort_bottles_by("price", frame))
        frame.tree.grid(row=0, column=0, columnspan=10, sticky='nsew')

        # make columns run function frame.on_double_click when double-clicked
        frame.tree.bind("<Double-1>", lambda e: frame.on_double_click(e, self))

        # display the appropriate message depending on whether in edit,
        # remove, or show modes
        frame.instructions_lbl = tk.Label(frame, textvariable = frame.instructions)
        frame.instructions_lbl.grid(row=2,column=0, sticky=tk.W)
        return

    def render_update_buttons(self, frame):
        """ Renders update and cancel buttons

            Args:
            frame (Frame): the frame where the buttons will be rendered
        """
        frame.update_btn = ttk.Button(frame, text="Update", command=lambda: self.update_entry(frame))
        frame.update_btn.grid(row=6, column=1,columnspan=3, padx=(20, 0), pady=(20,0), ipady=5, sticky=tk.NSEW)

        frame.cancel_btn = ttk.Button(frame, text="Cancel", command=lambda: self.cancel_entry(frame))
        frame.cancel_btn.grid(row=6, column=4,columnspan=3, pady=(20,0), ipady=5, sticky=tk.NSEW)
        return

    def render_remove_buttons(self, frame):
        """ Renders remove and cancel buttons

            Args:
            frame (Frame): the frame where the buttons will be rendered
        """
        frame.remove_btn = ttk.Button(frame, text="Remove", command=lambda: self.remove_entry_from_bottles())
        frame.remove_btn.grid(row=6, column=1,columnspan=3, padx=(20, 0), pady=(20,0), ipady=5, sticky=tk.NSEW)

        frame.cancel_btn = ttk.Button(frame, text="Cancel", command=lambda: self.cancel_entry(frame))
        frame.cancel_btn.grid(row=6, column=4,columnspan=3, pady=(20,0), ipady=5, sticky=tk.NSEW)
        return

    def save_entry(self, frame):
        """ Saves details from the entry boxes to the list of bottles

            Args:
            frame (Frame): the frame from where the details are fetched
        """
        distillery, name, age, price = self.get_details_from_entry_boxes(frame)
        # make a new bottle from the details and add it to the list
        new_bottle = Bottle(distillery, name, age, price)
        self.bottles.append(new_bottle)

        # show message of success
        messagebox.showinfo(title = "Confirmation", message = f'{new_bottle.distillery} {new_bottle.name} has been added to your collection.')
        self.clear_entry_boxes(frame)

        # return to the homepage
        self.show_frame(HomePage)
        return

    def show_collection(self):
        """ Sets current_mode to edit and shows the entire collection
        """
        self.current_mode= self.modes['show']
        self.show_frame(ShowCollectionPage)
        return

    def show_frame(self, frame):
        """ Brings a frame to the front and makes it visible

            Args:
            frame (Frame): the frame to be shown
        """
        current_frame = self.frames[frame]
        current_frame.update_display(self)
        current_frame.tkraise()
        return

    def sort_bottles_by(self, attribute, frame):
        """ Sorts the list of bottles by the specified attribute

            Args:
            attribute (string): the attribute being used to sort the list
        """
        self.bottles = sorted(self.bottles, key=lambda bottle: getattr(bottle, attribute))
        # render the showCollection page again so the display is updated
        frame.update_display(self)
        return

    def update_entry(self, frame):
        """ Updates details from entry boxes to current_bottle in list of bottles

            Args:
            frame (Frame): the frame to be shown
        """
        #  get the details, create a new bottle and add to the list
        distillery, name, age, price = self.get_details_from_entry_boxes(frame)
        new_bottle = Bottle(distillery, name, age, price)
        self.bottles.append(new_bottle)
        messagebox.showinfo(title = "Confirmation", message = f'{new_bottle.distillery} {new_bottle.name} has been added to your collection.')

        # delete old bottle from the list, clear the page, display homepage
        self.clear_entry_boxes(frame)
        self.bottles.pop(self.current_bottle)
        self.show_frame(HomePage)
        return


class HomePage(tk.Frame):
    """ Class for the homepage window

        Attributes
        ---------------------------
        display_string: string
        the welcome message displayed in the centre of the homepage

        Methods
        ___________________________
        update_display: renders the homepage, updates title and display message
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.display_string = tk.StringVar()
        self.update_display(controller)

    def update_display(self, controller):
        """ Renders the homepage, updates title and display message

            Args:
            controller (Frame): the main application so methods can be accessed
        """
        controller.render_homepage_display(self)
        tk.Tk.wm_title(controller, "Top Shelf")
        controller.geometry('380x250')


class AddBottlePage(tk.Frame):
    """ Class for the homepage window

        Methods
        ___________________________
        update_display: renders addbottlepage, updates title and size of window
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.update_display(controller)

    def update_display(self, controller):
        """ Renders the addbottlepage, updates title and size of window

            Args:
            controller (Frame): the main application so methods can be accessed
        """
        controller.render_bottle_details_layout(self)
        controller.render_save_buttons(self)
        tk.Tk.wm_title(controller, "Add a Bottle")
        controller.geometry('300x250')


class EditBottlePage(tk.Frame):
    """ Class for the editbottlepage window

        Methods
        ___________________________
        update_display: renders editbottlepage with currrent bottle details
                        updates title and size of window
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.update_display(controller)
        return

    def update_display(self, controller):
        """ Renders editbottlepage with currrent bottle details
            updates title and size of window

            Args:
            controller (Frame): the main application so methods can be accessed
        """
        controller.render_bottle_details_layout(self)
        controller.render_update_buttons(self)
        controller.add_details_to_entry_boxes(self, controller.bottles[controller.current_bottle])
        tk.Tk.wm_title(controller, "Edit a Bottle")
        controller.geometry('300x250')
        return


class FindBottlePage(tk.Frame):
    """ Class for the findbottlepage window

        Methods
        ___________________________
        update_display: renders findbottlepage updates title and size of window
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.instructions = tk.StringVar()
        self.update_display(controller)
        return

    def callback(self, search_term, controller):
        """ Searches the bottles list for distilleries/names beginning with
            the search_term and updates the table with the results

            Args:
            search_term (string): the term used to filter the list of bottles
            controller (Frame): the main application so methods can be accessed
        """
        # search the bottles list for distillery/name beginning with search_term
        results = controller.search_bottles_for_entry(search_term)
        # delete all results from the table
        self.tree.delete(*self.tree.get_children())
        # update table with search results
        controller.add_bottles_to_table(results, self.tree)


    def update_display(self, controller):
        """ Renders findbottlepage, updates title and size of window

            Args:
            controller (Frame): the main application so methods can be accessed
        """
        self.instructions.set("Start typing a distillery or name to filter your collection")
        controller.render_search_details_layout(self)
        controller.render_search_buttons(self)

        # render table, make sure it's empty and fill it with list of bottles
        controller.render_table(self)
        self.tree.delete(*self.tree.get_children())
        controller.add_bottles_to_table(controller.bottles, self.tree)

        # change title and size of window
        tk.Tk.wm_title(controller, "Find a Bottle")
        controller.geometry('770x350')
        return

    def on_double_click(self, event, controller):
        """ Handles double-click on an item in the table

            Args:
            controller (Frame): the main application so methods can be accessed
            """
        # identify which bottle was clicked
        item = self.tree.identify('item',event.x, event.y)
        vals = self.tree.item(self.tree.focus())

        # set the current_bottle = the bottle that was clicked
        for index, bottle in enumerate(controller.bottles):
            if bottle.distillery == vals['values'][0] and bottle.name == vals['values'][1]:
                controller.current_bottle = index

        # decide which page to be displayed depending on the mode
        if controller.current_mode== controller.modes['remove']:
            controller.show_frame(RemoveBottlePage)
        else:
            controller.show_frame(EditBottlePage)
        return


class RemoveBottlePage(tk.Frame):
    """ Class for the removebottlepage window

        Methods
        ___________________________
        update_display: renders removebottlepage with currrent bottle details
                        updates title and size of window

    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.update_display(controller)
        return

    def update_display(self, controller):
        """ Renders removebottlepage with currrent bottle details
            updates title and size of window

            Args:
            controller (Frame): the main application so methods can be accessed
        """
        controller.render_bottle_details_layout(self)
        controller.render_remove_buttons(self)
        controller.add_details_to_entry_boxes(self, controller.bottles[controller.current_bottle])
        tk.Tk.wm_title(controller, "Remove a Bottle")
        controller.geometry('300x250')
        return


class ShowCollectionPage(tk.Frame):
    """ Class for the showcollectionpage window

        Methods
        ___________________________
        update_display: renders page with table containing collection
                        updates title and size of window
        on_double_click: event-handler for double click on an item in the table
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.instructions = tk.StringVar()
        self.update_display(controller)
        return


    def update_display(self, controller):
        """ Renders removebottlepage with table containing collection
            updates title and size of window

            Args:
            controller (Frame): the main application so methods can be accessed
        """
        # display the instructions for the current mode e.g. 'double click
        # to remove a bottle' when mode is 'remove'
        self.instructions.set(controller.current_mode)

        # render the table, make sure it's empty and fille it with bottles
        controller.render_table(self)
        self.tree.delete(*self.tree.get_children())
        controller.add_bottles_to_table(controller.bottles, self.tree)

        # change title of page and set size
        tk.Tk.wm_title(controller, "My Collection")
        controller.geometry('770x250')
        return

    def on_double_click(self, event, controller):
        """ Handles double-click on an item in the table

            Args:
            controller (Frame): the main application so methods can be accessed
            """
        # identify which bottle was clicked
        item = self.tree.identify('item',event.x, event.y)
        vals = self.tree.item(self.tree.focus())

        # set the current_bottle = the bottle that was clicked
        for index, bottle in enumerate(controller.bottles):
            if bottle.distillery == vals['values'][0] and bottle.name == vals['values'][1]:
                controller.current_bottle = index

        # decide which page to be displayed depending on the mode
        if controller.current_mode== controller.modes['remove']:
            controller.show_frame(RemoveBottlePage)
        else:
            controller.show_frame(EditBottlePage)
        return


app = TopShelfApp()
app.mainloop()