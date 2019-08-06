from database_maintenance import *

# Import External Libraries
from pathlib import Path
import csv

# Import TKinter Libraries
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import scrolledtext

class metadata_display(database_maintenance):

	def user_deleter(self,current_user):
		# Delete a User

		# Delete User from Cached Database
		del self.database['users'][current_user]
		
		# Save Cached Database to Disk
		self.database_saver()
		
		# Clear Metadata Window and Reload Data 
		self.metadata_frame.destroy()
<<<<<<< HEAD
		self.user_loader()
		
	def metadata_entry_saver(self,current_user):
		# Save a User's Metadata
		
		# Update Current User
		if current_user in self.database['users']:
			for entry in self.entries:
					self.database['users'][current_user][entry[0]] = entry[1].get()
		
		# Create New User
=======
		self.load_users()

	def save_metadata_entries(self,current_user):
		# Save a User's Metadata

		if current_user in self.database['users']:
			for entry in self.entries:
					self.database['users'][current_user][entry[0]] = entry[1].get()

>>>>>>> a4792820267d2e682b503e63599a6536473153d5
		else:
			self.database['users'][current_user] = {}
			for entry in self.entries:
					self.database['users'][current_user][entry[0]] = entry[1].get()
<<<<<<< HEAD
		
		# Save Cached Database to Disk
		self.database_saver()
		
		# Clear Metadata Window and Reload Data 
		self.metadata_frame.destroy()
		self.user_loader()
		
	def database_metadata_entry_loader(self,event):	
		# Loads Metadata on Selected User
		
		##################
		# Window Cleanup #
		##################
		
=======

		self.save_database()
		self.metadata_frame.destroy()
		self.load_users()

	def load_metadata_entries(self,event):
		# Load Metadata on Selected User

>>>>>>> a4792820267d2e682b503e63599a6536473153d5
		# Delete Any Existing Information
		try:
			self.metadata_frame.destroy()
		except (NameError, AttributeError):
			pass
<<<<<<< HEAD
			
		##############################
		# Create User Metadata Frame #
		##############################
			
		# Create Metadata Frame	
		self.metadata_frame = ttk.Frame(self.metadata_window)
		self.metadata_frame.pack(anchor=NW)
	
		#################
		# Load Metadata #
		#################
		
		# Load Metadata Questions
		questions = {}

		# Populate Dictionary with Imported File
		with open (Path(self.config_path) / 'user_metadata.tsv', 'r') as file:
			reader = csv.reader(file, delimiter='\t')
			for line in reader:
				questions[line[0]] = line[1]
		
		# Create Entry Type List for Save Functions
		self.entries = []
		
		######################
		# Fill Metadata Form #
		######################
		
		# Create User ID Entry Box - This Ensures a User ID if Omitted from Config File
=======

		# Create Metadata Frame
		self.metadata_frame = ttk.Frame(self.metadata_window)
		self.metadata_frame.pack(anchor=NW)

		# Load Metadata Questions
		questions = {}

		# Populate dictionary with imported file
		self.config_files_path = os.path.join(os.path.dirname(__file__), "config_files/")

		with open (Path(self.config_files_path) / 'user_metadata.tsv', 'r') as file:
			reader = csv.reader(file, delimiter='\t')
			for line in reader:
				questions[line[0]] = line[1]

		self.entries = []

		# Designate user id
>>>>>>> a4792820267d2e682b503e63599a6536473153d5
		row = Frame(self.metadata_frame)
		uid_label = Label(row, text="User ID: ", anchor='w', width=30)
		uid_entry = Entry(row, width=50)
		
		# Display User ID Entry Box
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		uid_label.pack(side=LEFT)
<<<<<<< HEAD
		uid_entry.pack(side=RIGHT, expand=YES, fill=X)
		
		# Fill User ID Entry Box
=======
		self.uid_entry.pack(side=RIGHT, expand=YES, fill=X)

>>>>>>> a4792820267d2e682b503e63599a6536473153d5
		if self.current_user.get() == 'New User':
			uid_entry.insert(0,'nid')
		else:
<<<<<<< HEAD
			uid_entry.insert(0,self.current_user.get())
		
		# Create the Rest of the Entry Form Elements
=======
			self.uid_entry.insert(0,self.current_user.get())

		# Create Entry Form Elements
>>>>>>> a4792820267d2e682b503e63599a6536473153d5
		for field,question in questions.items():

			# Create a Row
			row = Frame(self.metadata_frame)

			# Create a Label and Text Box
			label = Label(row, text=question, anchor='w', width=30)
			entry = Entry(row, width=50)

			# Display Row
			row.pack(side=TOP, fill=X, padx=5, pady=5,)
			label.pack(side=LEFT)
			entry.pack(side=RIGHT, expand=YES, fill=X)
<<<<<<< HEAD
			
			# Fill in Entry Boxes
=======

>>>>>>> a4792820267d2e682b503e63599a6536473153d5
			if self.current_user.get() == 'New User':
				entry.insert(0,'')

			else:
				entry_text = self.database['users'][self.current_user.get()].get(field,'')
				entry.insert(0,entry_text)

			# Add Field and Current Pointers to Save List
			self.entries.append((field, entry))
<<<<<<< HEAD
			
		# Create Save and Delete Buttons	
=======

>>>>>>> a4792820267d2e682b503e63599a6536473153d5
		self.buttonFrame = ttk.Frame(self.metadata_frame)
		self.save_button = Button(self.buttonFrame, text='Save Values', command=(lambda: self.metadata_entry_saver(uid_entry.get())))
		self.delete_button = Button(self.buttonFrame, text='Delete User', command=(lambda: self.user_deleter(uid_entry.get())))
		
		# Display Save and Delete Buttons
		self.buttonFrame.pack(anchor=NW)
		self.save_button.pack(side=LEFT, padx=5, pady=5)
		self.delete_button.pack(side=LEFT, padx=5, pady=5)
<<<<<<< HEAD
				
	def user_loader(self):
		# Creates Dropdown Menu of Possible Users
	
		##################
		# Window Cleanup #
		##################
		
=======


	def load_users(self):

>>>>>>> a4792820267d2e682b503e63599a6536473153d5
		# Delete Any Existing Information
		try:
			self.selection_frame.destroy()
		except (NameError, AttributeError):
			pass
<<<<<<< HEAD
		
		##############################
		# Create User DropDown Frame #
		##############################		
		
		# Create User Dropdown Frame
=======

		######################
		# Metadata Drop Down #
		######################

>>>>>>> a4792820267d2e682b503e63599a6536473153d5
		self.selection_frame = ttk.Frame(self.metadata_window)

		# Retrieve Existing User List
		users = ['Choose a User','New User']

		for key,value in self.database['users'].items():
			users.append(key)

		# Create Dropdown Menu
		self.current_user = StringVar(self.selection_frame)
		self.current_user.set(users[0]) # default value
		users_menu = OptionMenu(self.selection_frame, self.current_user, *users, command=self.database_metadata_entry_loader)

		# Display Selection Frame
		self.selection_frame.pack(anchor=NW)
		users_menu.pack(side=LEFT, padx=5, pady=5)

	def database_metadata_viewer(self):
<<<<<<< HEAD
			
=======

		# Delete Any Existing Information
		try:
			self.selection_frame.destroy()
			self.metadata_frame.destroy()
		except (NameError, AttributeError):
			pass

>>>>>>> a4792820267d2e682b503e63599a6536473153d5
		###################
		# Metadata Window #
		###################

		# Setup Metadata Window
		self.metadata_window = Toplevel()
		self.metadata_window.title('Database Metadata')
		self.metadata_window.geometry("450x325+0+0")

		# Place Icon
		# "Writing" by IQON from the Noun Project
		if (sys.platform.startswith('win') or sys.platform.startswith('darwin')):
			self.metadata_window.iconbitmap(Path(self.assets_path) / 'icon.ico')
		else:
			logo = PhotoImage(file=Path(self.assets_path) / 'icon.gif')
			self.metadata_window.call('wm', 'iconphoto', self.metadata_window._w, logo)
<<<<<<< HEAD
		
		#################
		# User DropDown #
		#################
		
		# Display DropDown Menu
		self.user_loader()

		
		
		
=======

		# Display Dropdown Menu
		self.load_users()
>>>>>>> a4792820267d2e682b503e63599a6536473153d5
