# Import Classes
from database_display import *
from taxonomy_display import *

# Import TKinter Libraries
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import scrolledtext

# Instantiate Database Viewer
view_window = database_display()
taxonomy_window = taxonomy_display()

# Create Window
root = Tk()
root.title("Nisaba")
root.geometry('600x200')

# Setup Menu Tab
root_window_title = Label(root, text="\nNisaba: Multi-Modal Annotations\n")
root_window_title.config(font=("Times", 16))  
root_window_title.grid(column=0,row=0,sticky=W,padx=5, pady=5)

# Setup Menu Options
view_radio = Button(root,text='View/Edit an Existing Record', command=view_window.collection_selector)
vocabulary_radio = Button(root,text='Create Controlled Vocabulary', command=taxonomy_window.taxonomy_viewer)

# Display Menu Options
view_radio.grid(column=0,row=1,sticky=W,padx=5, pady=5)
vocabulary_radio.grid(column=0,row=3,sticky=W, padx=5, pady=5)

# Begin Main Loop  
root.mainloop()