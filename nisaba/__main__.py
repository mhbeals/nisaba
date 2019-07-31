# Import Classes
try:
    # Used when executing with Python
    from database_display import *
    from taxonomy_display import *
    # from metadata_display import *
except ModuleNotFoundError:
    # Used when calling as library
    from nisaba.database_display import *
    from nisaba.taxonomy_display import *
    # from nisaba.metadata_display import *

# Import TKinter Libraries
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import scrolledtext

def main():
    # Instantiate Database Viewer
    database_window = database_display()
    taxonomy_window = taxonomy_display()
    # metadata_window = metadata_display()

    # Create Window
    root = Tk()
    root.title("Nisaba")
    root.minsize(400, 150)
    root.maxsize(400, 150)

    # Place Icon
    # "Writing" by IQON from the Noun Project
    root.iconbitmap('icon.ico')

    # Setup Menu Tab
    root_window_title = Label(root, text="\nNisaba: Multi-Modal Annotations\n")
    root_window_title.config(font=("Times", 16))
    root_window_title.place(relx=0.5, rely=0.2, anchor=CENTER)

    # Setup Menu Options
    #edit_metadata = Button(root,text='View/Edit Database Metadata', command=metadata_window.database_metadata_viewer)
    edit_database = Button(root,text='View/Edit Database', command=database_window.collection_selector)
    edit_vocabulary = Button(root,text='Edit Annotation Vocabulary', command=taxonomy_window.taxonomy_viewer)


    # Display Menu Options
    #edit_metadata.place(relx=0.5, rely=0.45, anchor=CENTER)
    edit_database.place(relx=0.5, rely=0.5, anchor=CENTER)
    edit_vocabulary.place(relx=0.5, rely=0.7, anchor=CENTER)

    # Begin Main Loop
    root.mainloop()

if __name__ == "__main__":
    main()
