try:
	# Used when executing with Python
	from database_maintenance import *
	from tooltip import *
	from metadata_display import *
except ModuleNotFoundError:
	# Used when calling as library
	from nisaba.database_maintenance import *
	from nisaba.tooltip import *
	from nisaba.metadata_display import *

# Import External Libraries
from pathlib import Path
import csv
import yaml
# Import TKinter Libraries
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import scrolledtext
from tkinter import messagebox

class configuration_display(database_maintenance):

	def default_user_setter(self):

	# Set everyone to 0
		for key,value in self.database['users'].items():
			value['default'] = 0

		# Set this user to default (1)
		self.database['users'][self.current_user.get()]['default'] = 1

		self.database_saver()

	def edit_user_frame_displayer(self):
		##################
		# Window Cleanup #
		##################

		# Delete Previous Panels and Menus or Create New Window
		try:
			self.pane_two.destroy()
		except (NameError, AttributeError):
			pass

		##############################
		# Create Configuration Frame #
		##############################

		# Create User Metadata instance
		metadata_window = metadata_display()

		# Create Configuration Frame
		self.pane_two = ttk.Frame(self.configuration_window)
		self.pane_two.place(relx=.55, relwidth=.4, rely =.05, relheight=1)

		# Create User Frame
		metadata_window.database_metadata_viewer(self.pane_two)

	def configuration_textbox_frame_loader(self,filename):

		##################
		# Window Cleanup #
		##################

		# Delete Previous Panels and Menus or Create New Window
		try:
			self.pane_two.destroy()
		except (NameError, AttributeError):
			pass

		##############################
		# Create Configuration Frame #
		##############################

		# Create Configuration Frame
		self.pane_two = ttk.Frame(self.configuration_window)
		self.pane_two.place(relx=.55, relwidth=.4, rely =.05, relheight=1)

		# Create Taxonomy Loader Frame
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

	def configurations_loader(self):

		self.configurations_frame = ttk.Frame(self.pane_one)
		default_parameters = ["Collection Type Namespace","Collection 'Title' Field","Item Type Namespace","Item 'Title' Field"]
		default_values = self.defaults[4:]
		button_parameters = ["Default LOD Prefixes","Collection-Level Questions","Item-Level Questions","Segment-Level Questions"]
		self.parameter_entries = []
		i = 0

		for parameter in default_parameters:

			# Create Question Row
			row = ttk.Frame(self.pane_one)
			label = Label(row, text=parameter, anchor='w', width=30)
			entry = Entry(row)
			entry.insert(0,default_values[i])
			row.pack(side=TOP, fill=X, padx=5, pady=5)
			label.pack(side=LEFT)
			entry.pack(side=RIGHT, expand=YES, fill=X)
			self.parameter_entries.append([parameter,entry])
			i = i+1

		for parameter in button_parameters:
			# Create Question Row
			row = ttk.Frame(self.pane_one)
			label = Label(row, text=parameter, anchor='w', width=30)
			if parameter == "Default LOD Prefixes": button = ttk.Button(row, text="Set",command=(lambda: self.configuration_textbox_frame_loader('prefixes.txt')))
			if parameter == "Collection-Level Questions": button = ttk.Button(row, text="Set",command=(lambda: self.configuration_textbox_frame_loader(str(Path(self.metadata_path) / 'collections' / 'Standard.yaml'))))
			if parameter == "Item-Level Questions": button = ttk.Button(row, text="Set",command=(lambda: self.configuration_textbox_frame_loader(str(Path(self.metadata_path) / 'items' / 'Standard.yaml'))))
			if parameter == "Segment-Level Questions": button = ttk.Button(row, text="Set",command=(lambda: self.configuration_textbox_frame_loader(str(Path(self.metadata_path) / 'segments' / 'Standard.yaml'))))
			row.pack(side=TOP, fill=X, padx=5, pady=5)
			label.pack(side=LEFT)
			button.pack(side=LEFT)

		self.button_frame = ttk.Frame(self.pane_one)
		self.save_button = ttk.Button(self.button_frame, image=self.save_icon, command=self.configuration_defaults_saver)
		save_button_tt = ToolTip(self.save_button, "Save Configuration File",delay=0.01)
		self.save_button.pack()
		self.configurations_frame.pack()
		self.button_frame.pack(anchor=NW)

	def default_taxonomy_frame_creator(self):
	# Creates Fields for Default Taxonomies
	
		# Create Taxonomy Loader Frame
		self.taxonomy_loader_frame = ttk.Frame(self.pane_one)
		self.taxonomy_loader_frame.pack(side=TOP, fill=X)

		self.taxonomy_levels = ['Collection','Item','Segment']

		for level in self.taxonomy_levels:

			# Create Taxonmy Loader Row
			row = ttk.Frame(self.taxonomy_loader_frame)
			label = Label(row, text="Default " + level + " Taxonomy: ", anchor='w', width=30)
			entry = Entry(row)

			# Load Default Taxonomy Paths
			if level == 'Collection':
				entry.insert(0,self.taxonomy_level_defaults[0])
				button = ttk.Button(row, text="Load" , command=(lambda: self.database_loader("Collection",self.default_database_loader)))
			if level == 'Item':
				entry.insert(0,self.taxonomy_level_defaults[1])
				button = ttk.Button(row, text="Load" , command=(lambda: self.database_loader("Item",self.default_database_loader)))
			if level == 'Segment':
				entry.insert(0,self.taxonomy_level_defaults[2])
				button = ttk.Button(row, text="Load" , command=(lambda: self.database_loader("Segment",self.default_database_loader)))

			row.pack(side=TOP, fill=X, padx=5, pady=5)
			label.pack(side=LEFT)
			button.pack(side=RIGHT)
			entry.pack(side=RIGHT, expand=YES, fill=X)

		self.configurations_loader()

	def user_dropdown_creator(self):
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
			refresh_button = ttk.Button(row, text="Refresh Users", command=self.default_database_loader)
			edit_button.pack(side=RIGHT)
			refresh_button.pack(side=RIGHT)

			# Create Dropdown Menu
			users_menu = OptionMenu(row, self.current_user, *users)

			# Display Selection ttk.Frame
			users_menu.pack(anchor=W)

			self.default_taxonomy_frame_creator()

	def default_database_loader(self):

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
		# Create Configuration Frame #
		##############################

		# Create Configuration Frame
		self.pane_one = ttk.Frame(self.configuration_window)
		self.pane_one.place(relwidth=.5, relheight=1, rely =.05)
		self.pane_two = ttk.Frame(self.configuration_window)
		self.pane_two.place(relx=.55, relwidth=.4, rely =.05, relheight=1)

		# Create Database Loader Row
		row = ttk.Frame(self.pane_one)
		label = Label(row, text="Database: ", anchor='w', width=30)
		entry = Entry(row)
		entry.insert(0,self.current_database)
		button = ttk.Button(row, text="Load" , command=(lambda: self.database_loader('d',self.default_database_loader)))
		new_button = ttk.Button(row, text="New", command=self.database_creator)
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		label.pack(side=LEFT)
		button.pack(side=RIGHT)
		new_button.pack(side=RIGHT)
		entry.pack(side=RIGHT, expand=YES, fill=X)

		self.user_dropdown_creator()

	def configuration_viewer(self,window):

		self.save_icon=PhotoImage(file=Path(self.assets_path) / 'save.png')
		self.configuration_window = window
		self.configuration_window.pack_forget

		self.default_database_loader()
