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
	def save_metadata_entries(self,key):
		
		for entry in self.entries:
				self.database['users'][key][entry[0]] = entry[1].get()
		
		self.save_database()
				
	def database_metadata_viewer(self):
	
		###################
		# Metadata Window #
		###################

		# Setup Metadata Window
		self.metadata_window = Toplevel()
		self.metadata_window.title('Database Metadata')
		self.metadata_window.minsize(600,0)
		
		# Place Icon
		# "Writing" by IQON from the Noun Project
		self.metadata_window.iconbitmap('icon.ico')

		# Load Metadata Questions
		questions = {}

		# Populate dictionary with imported file
		self.config_files_path = os.path.join(os.path.dirname(__file__), "config_files/")
		
		with open (Path(self.config_files_path) / 'user_metadata.tsv', 'r') as file:
			reader = csv.reader(file, delimiter='\t')
			for line in reader:
				questions[line[0]] = line[1]
				
		self.entries = []

		for key,value in self.database['users'].items():
		
			# Designate user id
			row = Frame(self.metadata_window)
			label = Label(row, text="User ID: ", anchor='w')
			entry = Entry(row)
			row.pack(side=TOP, fill=X, padx=5, pady=5)
			label.pack(side=LEFT)
			entry.pack(side=RIGHT, expand=YES, fill=X)
			entry.insert(0,key)
			#entries.append(("userid", key))
			
			# Create Entry Form Elements
			for field,question in questions.items():

				# Create a row
				row = Frame(self.metadata_window)

				# Create a label and text box
				label = Label(row, text=question, anchor='w')
				entry = Entry(row)

				# Package Row
				row.pack(side=TOP, fill=X, padx=5, pady=5)
				label.pack(side=LEFT)
				entry.pack(side=RIGHT, expand=YES, fill=X)

				# Fill entry with database values (if available)

				entry_text = self.database['users'][key].get(field,'')

				entry.insert(0,entry_text)

				# Add field and value to save list
				self.entries.append((field, entry))
		
		self.buttonFrame = ttk.Frame(self.metadata_window)
		b1 = Button(self.buttonFrame, text='Save Values', command=(lambda: self.save_metadata_entries(key)))
		self.buttonFrame.pack(anchor=NW)
		b1.pack(side=LEFT, padx=5, pady=5)
