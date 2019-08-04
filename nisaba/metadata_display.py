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

	def userDeleter(self,current_user):
		# Delete a User

		del self.database['users'][current_user]
		self.save_database()
		self.metadata_frame.destroy()
		self.load_users()
		
	def save_metadata_entries(self,current_user):
		# Save a User's Metadata
		
		if current_user in self.database['users']:
			for entry in self.entries:
					self.database['users'][current_user][entry[0]] = entry[1].get()
		
		else:
			self.database['users'][current_user] = {}
			for entry in self.entries:
					self.database['users'][current_user][entry[0]] = entry[1].get()
					
		self.save_database()
		self.metadata_frame.destroy()
		self.load_users()
		
	def load_metadata_entries(self,event):	
		# Load Metadata on Selected User
		
		# Delete Any Existing Information
		try:
			self.metadata_frame.destroy()
		except (NameError, AttributeError):
			pass
			
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
		row = Frame(self.metadata_frame)
		uid_label = Label(row, text="User ID: ", anchor='w', width=30)
		self.uid_entry = Entry(row, width=50)
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		uid_label.pack(side=LEFT)
		self.uid_entry.pack(side=RIGHT, expand=YES, fill=X)
		
		if self.current_user.get() == 'New User':
			self.uid_entry.insert(0,'nid')
		else:
			self.uid_entry.insert(0,self.current_user.get())
		
		# Create Entry Form Elements
		for field,question in questions.items():

			# Create a row
			row = Frame(self.metadata_frame)

			# Create a label and text box
			label = Label(row, text=question, anchor='w', width=30)
			entry = Entry(row, width=50)

			# Package Row
			row.pack(side=TOP, fill=X, padx=5, pady=5,)
			label.pack(side=LEFT)
			entry.pack(side=RIGHT, expand=YES, fill=X)
			
			if self.current_user.get() == 'New User':
				entry.insert(0,'')
			
			else:
				# Fill entry with database values (if available)
				entry_text = self.database['users'][self.current_user.get()].get(field,'')
				entry.insert(0,entry_text)

			# Add field and value to save list
			self.entries.append((field, entry))
			
		self.buttonFrame = ttk.Frame(self.metadata_frame)
		self.save_button = Button(self.buttonFrame, text='Save Values', command=(lambda: self.save_metadata_entries(self.uid_entry.get())))
		self.delete_button = Button(self.buttonFrame, text='Delete User', command=(lambda: self.userDeleter(self.uid_entry.get())))
		self.buttonFrame.pack(anchor=NW)
		self.save_button.pack(side=LEFT, padx=5, pady=5)
		self.delete_button.pack(side=LEFT, padx=5, pady=5)
		
		
	def load_users(self):

		# Delete Any Existing Information
		try:
			self.selection_frame.destroy()
		except (NameError, AttributeError):
			pass
		
		######################
		# Metadata Drop Down #
		######################		
		
		self.selection_frame = ttk.Frame(self.metadata_window)
		
		# Retrieve Existing User List
		users = ['Choose a User','New User']
		
		for key,value in self.database['users'].items():	
			users.append(key)
			
		# Create Dropdown Menu
		self.current_user = StringVar(self.selection_frame)
		self.current_user.set(users[0]) # default value
		users_menu = OptionMenu(self.selection_frame, self.current_user, *users, command=self.load_metadata_entries)

		# Display Selection Frame
		self.selection_frame.pack(anchor=NW)
		users_menu.pack(side=LEFT, padx=5, pady=5)
		
	def database_metadata_viewer(self):
	
		# Delete Any Existing Information
		try:
			self.selection_frame.destroy()
			self.metadata_frame.destroy()
		except (NameError, AttributeError):
			pass
			
		###################
		# Metadata Window #
		###################

		# Setup Metadata Window
		self.metadata_window = Toplevel()
		self.metadata_window.title('Database Metadata')
		self.metadata_window.geometry("450x325+0+0")
		
		# Place Icon
		# "Writing" by IQON from the Noun Project
		self.metadata_window.iconbitmap('icon.ico')
		
		# Display Dropdown Menu
		self.load_users()

		
		
		
