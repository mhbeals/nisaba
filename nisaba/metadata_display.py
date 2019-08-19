try:
	# Used when executing with Python
	from database_maintenance import *
	from cache_maintenance import *
	from tooltip_creation import *
except ModuleNotFoundError:
	# Used when calling as library
	from nisaba.database_maintenance import *
	from nisaba.cache_maintenance import *
	from nisaba.tooltip_creation import *

# Import External Libraries
from pathlib import Path
import yaml

# Import TKinter Libraries
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import scrolledtext
from tkinter import messagebox

class metadata_display(cache_maintenance):

	#########################
	#   Field Populators    #
	#########################
		
	def user_metadata_fields_displayer(self,event):	
	# Displays Metadata on Selected User
		
		##################
		# Window Cleanup #
		##################

		# Delete Any Existing Information
		try:
			self.metadata_frame.destroy()
		except (NameError, AttributeError):
			pass
			
		##############################
		# Create User Metadata Frame #
		##############################
			
		# Create Metadata ttk.Frame	
		self.metadata_frame = ttk.Frame(self.metadata_window)
		self.metadata_frame.place(y = 10, relx=.01, rely=.05)
	
		#################
		# Load Metadata #
		#################
		
		# Load Metadata Questions
		questions = {}

		# Populate Dictionary with Imported File
		filename = 'users/UserMetadata.yaml'
		
		with open (Path(self.config_path) / filename, 'r') as file:
			self.questions = yaml.safe_load(file)
		
		# Create Entry Type List for Save Functions
		self.entries = []
		
		######################
		# Fill Metadata Form #
		######################
		
		# Create User ID Entry Box and Default User Check - This Ensures a User ID if Omitted from Config File
		row = ttk.Frame(self.metadata_frame)
		uid_label = Label(row, text="User ID: ", anchor='w', width=30)
		uid_entry = Entry(row, width=50)		

		# Display User ID Entry Box
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		uid_label.pack(side=LEFT)
		uid_entry.pack(side=LEFT, expand=YES, fill=X)
	
		# Fill User ID Entry Box
		if self.current_user.get() == 'New User':
			uid_entry.insert(0,'nid')
		else:
			uid_entry.insert(0,self.current_user.get())
		
		# Create the Rest of the Entry Form Elements
		for field,question in self.questions.items():

			# Create a Row
			row = ttk.Frame(self.metadata_frame)

			# Create a Label and Text Box
			label = Label(row, text=question, anchor='w', width=30)
			entry = Entry(row, width=50)

			# Display Row
			row.pack(side=TOP, fill=X, padx=5, pady=5,)
			label.pack(side=LEFT)
			entry.pack(side=RIGHT, expand=YES, fill=X)

			if self.current_user.get() == 'New User':
				entry.insert(0,'')

			else:
				entry_text = self.database['users'][self.current_user.get()].get(field,'')
				entry.insert(0,entry_text)

			# Add Field and Current Pointers to Save List
			self.entries.append((field, entry))
			
		# Create Save and Delete Buttons	
		self.buttonFrame = ttk.Frame(self.metadata_frame)
		self.save_button = Button(self.buttonFrame, image=self.save_icon, command=(lambda: self.metadata_entry_saver(uid_entry.get())))
		save_button_tt = ToolTip(self.save_button, "Save User",delay=0.01)
		self.delete_button = Button(self.buttonFrame, image=self.delete_icon, command=(lambda: self.user_deleter(uid_entry.get())))
		delete_button_tt = ToolTip(self.delete_button, "Delete User",delay=0.01)
		
		# Display Save and Delete Buttons
		self.buttonFrame.pack(anchor=NW)
		self.save_button.pack(side=LEFT, padx=5, pady=5)
		self.delete_button.pack(side=LEFT, padx=5, pady=5)
				
	def user_dropdown_displayer(self):
	# Creates Dropdown Menu of Possible Users
				
		##################
		# Window Cleanup #
		##################
		
		# Delete Previous Panels and Menus or Create New Window
		try:
			self.pane_one.destroy()
			self.pane_two.destroy()
			self.pane_three.destroy()
		except (NameError, AttributeError):
			pass

		##############################
		# Create User DropDown Frame #
		##############################		
		
		# Create User Dropdown Frame
		self.pane_one = ttk.Frame(self.metadata_window)

		# Divider		
		dividing_label = ttk.Label(self.pane_one, text="User Configuration")
		dividing_label.configure(font=(14))
		dividing_label.pack(pady = 20)
		
		# Retrieve Existing User List
		users = ['Choose a User','New User']

		for key,value in self.database['users'].items():
			users.append(key)

		# Create Dropdown Menu
		self.current_user = StringVar(self.pane_one)
		self.current_user.set(users[0]) # default value
		users_menu = OptionMenu(self.pane_one, self.current_user, *users, command=self.user_metadata_fields_displayer)

		# Display Selection ttk.Frame
		self.pane_one.place(relx=.01, rely=.01)
		users_menu.pack(side=LEFT, padx=5, pady=5)
	
	########################
	#         Main         #
	########################
	
	def database_metadata_viewer(self,window):
	# Displays User Information Panel
				
		# Set Icon Assets
		# Menu Bar Icons made by Pixel Buddha (https://www.flaticon.com/authors/pixel-buddha) from http://www.flaticon.com  CC-BY (http://creativecommons.org/licenses/by/3.0/)
		self.delete_icon=PhotoImage(file=Path(self.assets_path) / 'delete.png')
		self.save_icon=PhotoImage(file=Path(self.assets_path) / 'save.png')
	
		self.metadata_window = window
		self.metadata_window.pack_forget 
		self.user_dropdown_displayer()
