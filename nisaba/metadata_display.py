try:
	# Used when executing with Python
	from database_maintenance import *
except ModuleNotFoundError:
	# Used when calling as library
	from nisaba.database_maintenance import *

# Import External Libraries
from pathlib import Path
import csv

# Import TKinter Libraries
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import scrolledtext
from tkinter import messagebox

class metadata_display(database_maintenance):

	def default_user_setter(self,current_user):
		# If this user has 'default' checked
		if self.uid_default_user_var.get() == 1:
			
			# Set everyone to 0
			for key,value in self.database['users'].items():
				value['default'] = 0
			
			# Set this user to default (1)
			self.database['users'][current_user]['default'] = 1

	def user_deleter(self,current_user):
		# Delete a User

		# Delete User from Cached Database
		del self.database['users'][current_user]
		
		# Save Cached Database to Disk
		self.database_saver()
		
		# Clear Metadata Window and Reload Data 
		self.metadata_frame.destroy()
		self.user_loader()
		
	def metadata_entry_saver(self,current_user):
		# Save a User's Metadata
		
		# Update Current User
		if current_user in self.database['users']:

			self.default_user_setter(current_user)
			
			# Go through the rest of the entries and save the vaule
			for entry in self.entries:
				self.database['users'][current_user][entry[0]] = entry[1].get()
					
		else:
		
			# Create new entry in database
			self.database['users'][current_user] = {}
			
			# Go through the entries and save the vaule
			for entry in self.entries:
					self.database['users'][current_user][entry[0]] = entry[1].get()
		
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

		# Delete Any Existing Information
		try:
			self.metadata_frame.destroy()
		except (NameError, AttributeError):
			pass
			
		##############################
		# Create User Metadata ttk.Frame #
		##############################
			
		# Create Metadata ttk.Frame	
		self.metadata_frame = ttk.Frame(self.metadata_window)
		self.metadata_frame.place(relx=.01, rely=.05)
	
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
		
		# Create User ID Entry Box and Default User Check - This Ensures a User ID if Omitted from Config File
		row = ttk.Frame(self.metadata_frame)
		uid_label = Label(row, text="User ID: ", anchor='w', width=30)
		uid_entry = Entry(row, width=50)		
		self.uid_default_user_var = BooleanVar()
		self.uid_default_user = Checkbutton(row, text="Default User", variable=self.uid_default_user_var)

		# Display User ID Entry Box
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		uid_label.pack(side=LEFT)
		uid_entry.pack(side=LEFT, expand=YES, fill=X)
		self.uid_default_user.pack(side=RIGHT, padx=5)
		
		# Fill User ID Entry Box
		if self.current_user.get() == 'New User':
			uid_entry.insert(0,'nid')
		else:
			uid_entry.insert(0,self.current_user.get())
			
			# Check Default Box
			if self.database['users'][self.current_user.get()].get('default',0) == 1:
				self.uid_default_user_var.set(1)
		
		# Create the Rest of the Entry Form Elements
		for field,question in questions.items():

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
		self.save_button = Button(self.buttonFrame, text='Save Values', command=(lambda: self.metadata_entry_saver(uid_entry.get())))
		self.delete_button = Button(self.buttonFrame, text='Delete User', command=(lambda: self.user_deleter(uid_entry.get())))
		
		# Display Save and Delete Buttons
		self.buttonFrame.pack(anchor=NW)
		self.save_button.pack(side=LEFT, padx=5, pady=5)
		self.delete_button.pack(side=LEFT, padx=5, pady=5)
				
	def user_loader(self):
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
		# Create User DropDown ttk.Frame #
		##############################		
		
		# Create User Dropdown ttk.Frame
		self.pane_one = ttk.Frame(self.metadata_window)

		# Retrieve Existing User List
		users = ['Choose a User','New User']

		for key,value in self.database['users'].items():
			users.append(key)

		# Create Dropdown Menu
		self.current_user = StringVar(self.pane_one)
		self.current_user.set(users[0]) # default value
		users_menu = OptionMenu(self.pane_one, self.current_user, *users, command=self.database_metadata_entry_loader)

		# Display Selection ttk.Frame
		self.pane_one.place(relx=.01, rely=.01)
		users_menu.pack(side=LEFT, padx=5, pady=5)
	
	def database_metadata_viewer(self,window):
	
		self.metadata_window = window
		self.metadata_window.pack_forget 
		self.user_loader()
