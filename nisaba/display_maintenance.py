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

class main_display(database_maintenance):

	def window_creator(self):
	
		# Set assests path
		assets_path = os.path.join(os.path.dirname(__file__), "assets/")

		# Instantiate Database Viewer
		database_window = database_display()
		taxonomy_window = taxonomy_display()
		metadata_window = metadata_display()
	
		# Displays the Main Window
	
		################
		# Setup Window #
		################

		# Setup Taxonomy Window
		self.main_window = Tk()
		self.main_window.title('Nisaba: Multi-Modal Annotation')
		
		# Place Icon
		# "Writing" by IQON from the Noun Project
		if (sys.platform.startswith('win') or sys.platform.startswith('darwin')):
			self.main_window.iconbitmap(Path(self.assets_path) / 'icon.ico')
		else:
			logo = PhotoImage(file=Path(self.assets_path) / 'icon.gif')
			self.main_window.call('wm', 'iconphoto', self.main_window._w, logo)
			
		# Set to Full Screen
		try:
			self.main_window.state('zoomed')
		except (TclError):
			pass
			m = self.main_window.maxsize()
			self.main_window.geometry('{}x{}+0+0'.format(*m))

		# Determine Window Size / Screen Resolution 
		window_width = self.main_window.winfo_screenwidth()
		window_height = self.main_window.winfo_screenheight()

		# Setup Taxonomy Window Panels 
		self.main_pane_menu = Frame(self.main_window, relief=SUNKEN)
		self.main_pane_one = Frame(self.main_window, relief=SUNKEN)
		self.main_pane_two = Frame(self.main_window, relief=SUNKEN)
		self.main_pane_three = Frame(self.main_window, relief=SUNKEN)
		self.main_pane_alpha = Frame(self.main_window, relief=SUNKEN)
		self.main_pane_beta = Frame(self.main_window, relief=SUNKEN)
		
		# Setup Menu Icon Panel
		self.main_pane_menu.place(relwidth=.1, relheight=1)
		
		# Setup Two-Pane Steup
		#self.main_pane_alpha.place(relx=.1, relwidth=.44, relheight=1)
		#self.main_pane_beta.place(relx=.54, relwidth=.46, relheight=1)
				
		# Setup Three-Pane Setup
		#self.main_pane_one.place(relx=.1, relwidth=.30, relheight=1)
		#self.main_pane_two.place(relx=.40, relwidth=.30, relheight=1)
		#self.main_pane_three.place(relx=.70, relwidth=.30, relheight=1)
		
		# Add Icons to Options
		# Icons made by Freepik(https://www.flaticon.com/authors/freepik) from https://www.flaticon.com/" CC-BY (http://creativecommons.org/licenses/by/3.0/)
		user_logo=PhotoImage(file=Path(assets_path) / 'users.png')
		database_logo=PhotoImage(file=Path(assets_path) / 'database.png')
		taxonomy_logo=PhotoImage(file=Path(assets_path) / 'taxonomy.png')
		
		# Setup Menu Options
		edit_metadata = Button(self.main_pane_menu,text='Users',  command=metadata_window.database_metadata_viewer)
		edit_database = Button(self.main_pane_menu,text='Database',  command=database_window.database_window_displayer)
		edit_vocabulary = Button(self.main_pane_menu,text='Taxonomy',  command=taxonomy_window.taxonomy_viewer)
		
		# Display Menu Options
		edit_metadata.place(relx=0.5, rely=0.3, anchor=CENTER)
		edit_database.place(relx=0.5, rely=0.5, anchor=CENTER)
		edit_vocabulary.place(relx=0.5, rely=0.7, anchor=CENTER)
		
		main_window.mainloop()