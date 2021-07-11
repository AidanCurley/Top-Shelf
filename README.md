# Overview
The TopShelf application allows a user to record, track, and update their whisky collection, allowing users to record four attributes for each bottle in their collection, distillery name, bottling name, age, and price. Standard functionality for data storage and manipulation is included: insertion, deletion, manipulation (editing and sorting), and searching. The application has been designed using object oriented principles and uses the Tkinter library for GUI implementation. A bottles.csv file has been provided with sample data so the application can be used as intended.

# Classes
The Bottle class is used for storing each bottle in the collection as an object. The attributes are initiated as certain data types - integers, strings, etc. which makes it possible to ensure the data is valid and functions/methods can be written which treat each bottle as generic examples of the same ‘thing’.

The TopShelfApp class is the main class for the application. This opens a window containing a Tkinter frame which is used as a container for all the other pages (which are actually frames layered on top of each other). This class contains most of the methods used throughout the program so that they can be accessed from anywhere within the code.

There are six classes which act as separate pages for the application: Homepage, AddBottlePage, EditBottlePage, FindBottlePage, RemoveBottlePage, ShowCollectionPage. Each of these is a Tkinter Frame object which has been initialised inside the TopShelfApp frame and can be ‘displayed’ by bringing it to the front of the pile calling the show_frame method.

There are two classes to enable error handling: the Error class which provides a base class for exceptions, and the InputError class, a subclass of the Error class which displays a message to the user each time an InputError is raised.

# Implementation
*Insertion* is achieved using the in-built append method which adds an item to the end of a list.

*Deletion* is achieved by allowing users to choose a bottle from the collection, the index of which is stored in the current_bottle attribute of the Main Application. This index is then used by the in-built pop(index) method to remove the bottle from the list.

*Editing* follows a similar pattern, combining the functionality above to delete the bottle with the current_bottle index and append a new bottle with the updated details to the end of the list.

*Sorting* is controlled by the sort_bottles_by method which takes an attribute and uses Python’s sorted() method to update the bottle list to a version of the list sorted by the specified attribute.

*Searching* is implemented in the search_bottle_for_entry method which takes a search term and uses Python list iteration and the in-built startswith string method to return a sublist of bottles where the distillery or name attributes start with the search term.
