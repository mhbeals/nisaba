# Import Classes
try:
	# Used when executing with Python
	from database_display import *
	from taxonomy_display import *
	from metadata_display import *
except ModuleNotFoundError:
	# Used when calling as library
	from nisaba.database_display import *
	from nisaba.taxonomy_display import *
	from nisaba.metadata_display import *

# Import TKinter Libraries
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import scrolledtext

def main():

	# Set assests path
	assets_path = os.path.join(os.path.dirname(__file__), "assets/")

	# Instantiate Database Viewer
	database_window = database_display()
	taxonomy_window = taxonomy_display()
	metadata_window = metadata_display()

	# Create Window
	root = Tk()
	root.title("Nisaba")
	root.minsize(400, 150)
	root.maxsize(400, 150)

	# Place Icon
	# "Writing" by IQON from the Noun Project
	if (sys.platform.startswith('win') or sys.platform.startswith('darwin')):
		root.iconbitmap(Path(assets_path) / 'icon.ico')
	else:
		logo = PhotoImage(file=Path(assets_path) / 'icon.gif')
		self.root.call('wm', 'iconphoto', self.root._w, logo)

	# Setup Menu Tab
	root_window_title = Label(root, text="\nNisaba: Multi-Modal Annotations\n")
	root_window_title.config(font=("Times", 16))
	root_window_title.place(relx=0.5, rely=0.2, anchor=CENTER)

	# Add Icons to Options
	# Icons made by Freepik(https://www.flaticon.com/authors/freepik) from https://www.flaticon.com/" CC-BY (http://creativecommons.org/licenses/by/3.0/)
	user_logo=PhotoImage(file=Path(assets_path) / 'users.png')
	database_logo=PhotoImage(file=Path(assets_path) / 'database.png')
	taxonomy_logo=PhotoImage(file=Path(assets_path) / 'taxonomy.png')
	
	# Setup Menu Options
	edit_metadata = Button(root,text='Users', image=user_logo, compound="top", command=metadata_window.database_metadata_viewer)
	edit_database = Button(root,text='Database', image=database_logo, compound="top", command=database_window.database_window_displayer)
	edit_vocabulary = Button(root,text='Taxonomy', image=taxonomy_logo, compound="top", command=taxonomy_window.taxonomy_viewer)
	
	# Display Menu Options
	edit_metadata.place(relx=0.3, rely=0.6, anchor=CENTER)
	edit_database.place(relx=0.5, rely=0.6, anchor=CENTER)
	edit_vocabulary.place(relx=0.7, rely=0.6, anchor=CENTER)

	# Begin Main Loop
	root.mainloop()

if __name__ == "__main__":
	main()
