try:
	# Used when executing with Python
	from database_maintenance import *
	from cache_maintenance import *
	from tooltip_creation import *
	from metadata_display import *
except ModuleNotFoundError:
	# Used when calling as library
	from nisaba.database_maintenance import *
	from nisaba.cache_maintenance import *
	from nisaba.tooltip_creation import *
	from nisaba.metadata_display import *

# Import External Libraries
from pathlib import Path
import csv
import yaml
import configparser
import re 

# Import TKinter Libraries
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import scrolledtext
from tkinter import messagebox

class configuration_display(cache_maintenance):

	##############################
	#      Panel Displays        #
	##############################

	def edit_user_frame_displayer(self):
	# Displays user metadata in pane two
	
		# Delete Previous Panels and Menus or Create New Window
		try:
			self.pane_two.destroy()
		except (NameError, AttributeError):
			pass

		# Create User Metadata instance
		metadata_window = metadata_display()

		# Create Configuration Frame
		self.pane_two = ttk.Frame(self.configuration_window)
		self.pane_two.place(relx=.55, relwidth=.4, rely =.05, relheight=1)

		# Create User Frame
		metadata_window.database_metadata_viewer(self.pane_two)

	def configuration_textbox_frame_displayer(self,filename):
	# Displays configuration file in pane two
	
		# Delete Previous Panels and Menus or Create New Window
		try:
			self.pane_two.destroy()
		except (NameError, AttributeError):
			pass

		# Create Configuration Frame
		self.pane_two = ttk.Frame(self.configuration_window)
		self.pane_two.place(relx=.55, relwidth=.4, rely =.05, relheight=1)

		# Create Loader Frame
		self.configuration_textbox_frame = ttk.Frame(self.pane_two)
		self.configuration_textbox_frame.pack(side=TOP, fill=X)

		self.configuration_textbox = Text(self.configuration_textbox_frame, wrap=WORD)
		self.configuration_textbox.pack(expand=YES, fill=BOTH)

		self.configuration_textbox.insert("0.0",self.configuration_file_loader(filename))

		row = ttk.Frame(self.pane_two)
		self.save_button = ttk.Button(row, image=self.save_icon, command=(lambda:self.configuration_file_saver(filename)))
		save_button_tt = ToolTip(self.save_button, "Save Configuration File",delay=0.01)
		self.save_button.pack(side=LEFT)
		row.pack()

	def configurations_frame_displayer(self):
	# Loads non-database parameters from Configuration File
		
		# Create Configuration Frame
		self.configurations_frame = ttk.Frame(self.pane_one)
		
		# Create List to Hold Widget Pointers (for save)
		self.parameter_entries = []

		# Display all variable (v_) items in the config file
		for key,value in self.config.items():

			if key.startswith('v_'):
			
				# Format Label from Key
				label_text = re.sub('_',' ',key[1:]).title() + ':'
			
				# Create Row
				row = ttk.Frame(self.pane_one)
				label = Label(row, text=label_text, anchor='w', width=30)
				entry = Entry(row)
				entry.insert(0,value)
				row.pack(side=TOP, fill=X, padx=5, pady=5)
				label.pack(side=LEFT)
				entry.pack(side=RIGHT, expand=YES, fill=X)
				
				# Save Label and Pointer
				self.parameter_entries.append([key,entry])

		# Divider
		
		dividing_label = ttk.Label(self.pane_one, text="Additional Configuration Files")
		dividing_label.configure(font=(14))
		dividing_label.pack(pady = 10)
				
		# Load up Additional Config Files
		directories = []
		self.path_dictionary = {}
		
		# Looks up all available configuration directories
		for root, dirs, files in os.walk(Path(self.config_path)):
			for dir in dirs:
				directories.append(dir)
				
		for directory in directories:
			
			# Looks up all available type YAML files
			types = []
			
			for root, dirs, files in os.walk(Path(self.config_path) / directory):
				for file in files:
					if file.endswith(".yaml") or file.endswith(".txt"):
						filename = re.sub('(?!^)([A-Z]+)', r' \1',os.path.splitext(file)[0])
						types.append(filename)
						self.path_dictionary[filename] = Path(self.config_path) / directory / file
			
			if len(types) != 0:
				
				types.insert(0,'Choose a Configuration File')
				default_type = StringVar(self.pane_one)
							
				# Create Question Row
				row = ttk.Frame(self.pane_one)
				label = Label(row, text=directory.title(), anchor='w', width=30)
				label.pack(side=LEFT)
				dropdown = ttk.OptionMenu(row, default_type, *types, command=self.configuration_textbox_frame_displayer)
				dropdown.pack(side=LEFT)
				new_button = ttk.Button(row, text="New", command=self.configuration_yaml_creator)
				new_button.pack(side=RIGHT)
				row.pack(side=TOP, fill=X, padx=5, pady=5)
				
		dividing_label = ttk.Label(self.pane_one, text=" ")
		dividing_label.configure(font=(14))
		dividing_label.pack(pady = 10)
		
		self.button_frame = ttk.Frame(self.pane_one)
		self.save_button = ttk.Button(self.button_frame, image=self.save_icon, command=self.configuration_defaults_saver)
		save_button_tt = ToolTip(self.save_button, "Save Configuration File",delay=0.01)
		self.save_button.pack()
		self.configurations_frame.pack()
		self.button_frame.pack(anchor=NW)

	def default_taxonomy_frame_displayer(self):
	# Creates Fields for Default Taxonomies
	
		# Create Taxonomy Loader Frame
		self.taxonomy_loader_frame = ttk.Frame(self.pane_one)
		self.taxonomy_loader_frame.pack(side=TOP, fill=X)

		# Create Taxonomy Levels
		self.taxonomy_levels = ['Collection','Item','Segment']

		for level in self.taxonomy_levels:

			
			# Create Taxonmy Loader Row
			row = ttk.Frame(self.taxonomy_loader_frame)
			row.pack(side=TOP, fill=X, padx=5, pady=5)
			label = Label(row, text="Default " + level + " Taxonomy: ", anchor='w', width=30)
			label.pack(side=LEFT)
			
			# Load Default Taxonomy Paths
			if level == 'Collection':
				self.collection_entry = Entry(row)
				self.collection_entry.insert(0,self.taxonomy_level_defaults[0])
				self.collection_entry.pack(side=LEFT, expand=YES, fill=X)
				button = ttk.Button(row, text="Load" , command=(lambda: self.database_loader("Collection",self.default_database_panels_displayer)))
			if level == 'Item':
				self.item_entry = Entry(row)
				self.item_entry.insert(0,self.taxonomy_level_defaults[1])
				self.item_entry.pack(side=LEFT, expand=YES, fill=X)
				button = ttk.Button(row, text="Load" , command=(lambda: self.database_loader("Item",self.default_database_panels_displayer)))
			if level == 'Segment':
				self.segment_entry = Entry(row)
				self.segment_entry.insert(0,self.taxonomy_level_defaults[2])
				self.segment_entry.pack(side=LEFT, expand=YES, fill=X)
				button = ttk.Button(row, text="Load" , command=(lambda: self.database_loader("Segment",self.default_database_panels_displayer)))
			
			button.pack(side=RIGHT)
			
		# Load other parameters
		self.configurations_frame_displayer()

	def user_dropdown_displayer(self):
	# Creates Dropdown Menu of Possible Users

		# Retrieve Existing User List
		users = []
		self.current_user = StringVar(self.configuration_window)

		try:
			for key,value in self.database['users'].items():
				users.append(key)
				if  value['default'] == 1:
					self.current_user.set(key)
		except(KeyError):
			label = ttk.Label(self.pane_one,text="Invalid Database File")
			label.pack()

		else:
			# Create Default User Row
			row = ttk.Frame(self.pane_one)
			row.pack(side=TOP, fill=X, padx=5, pady=5)
			label = Label(row, text="Default User: ", anchor='w', width=30)
			label.pack(side=LEFT)
			edit_button = ttk.Button(row, text="Edit Users", command=self.edit_user_frame_displayer)
			refresh_button = ttk.Button(row, text="Refresh Users", command=self.default_database_panels_displayer)
			edit_button.pack(side=RIGHT)
			refresh_button.pack(side=RIGHT)

			# Create Dropdown Menu
			users_menu = OptionMenu(row, self.current_user, *users)

			# Display Selection ttk.Frame
			users_menu.pack(anchor=W)

			self.default_taxonomy_frame_displayer()

	def default_database_panels_displayer(self):

		# Delete Previous Panels and Menus or Create New Window
		try:
			self.pane_one.destroy()
			self.pane_two.destroy()
		except (NameError, AttributeError):
			pass

		# Create Configuration Frame
		self.pane_one = ttk.Frame(self.configuration_window)
		self.pane_one.place(relwidth=.4, relheight=1, rely =.05)
		self.pane_two = ttk.Frame(self.configuration_window)
		self.pane_two.place(relx=.4, relwidth=.5, rely =.05, relheight=1)

		# Create Database Loader Row
		row = ttk.Frame(self.pane_one)
		label = Label(row, text="Database: ", anchor='w', width=30)
		entry = Entry(row)
		entry.insert(0,self.current_database)
		button = ttk.Button(row, text="Load" , command=(lambda: self.database_loader('d',self.default_database_panels_displayer)))
		new_button = ttk.Button(row, text="New", command=self.database_creator)
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		label.pack(side=LEFT)
		button.pack(side=RIGHT)
		new_button.pack(side=RIGHT)
		entry.pack(side=RIGHT, expand=YES, fill=X)

		self.user_dropdown_displayer()

	##############################
	#           Main             #
	##############################		
		
	def configuration_viewer(self,window):
	# Display Configuration Panels 
	
		self.save_icon=PhotoImage(file=Path(self.assets_path) / 'save.png')
		
		self.configuration_window = window
		self.configuration_window.pack_forget
		self.default_database_panels_displayer()