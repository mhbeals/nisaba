# Import External Libaries
import json
import datetime
from pathlib import Path
import re
import os
import configparser

# Import tkinter Libraries
from tkinter import END
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askdirectory

class database_maintenance:

	##############################
	#	   Initialisation	   #
	##############################

	# Set Relative Paths
	assets_path = os.path.join(os.path.dirname(__file__), "assets/")
	config_path = os.path.join(os.path.dirname(__file__), "config_files/")
	database_path = os.path.join(os.path.dirname(__file__), "databases/")
	raw_data_path = os.path.join(os.path.dirname(__file__), "raw_data/")
	sample_image_path = os.path.join(os.path.dirname(__file__), "raw_data/images/")
	database_backup_path = database_path + "backups/"

	def __init__(self):
		# Initialise programme with stored databases

		# Create Configuration Defaults
		self.configuration_file_creator()

		# Set Current Database and Taxonomies
		self.current_database = self.config['Database']

		try:
			self.git_path = self.config['GitPath']
		except(KeyError):
			self.git_path = Path(os.path.join(os.path.dirname(__file__)))

		try:
			self.raw_data_images_path = self.config['ImagePath']
		except(KeyError):
			self.raw_data_images_path = Path(os.path.join(os.path.dirname(__file__), "raw_data/images/"))
		
		try:
			self.current_taxonomy = self.config['Taxonomy']
		except(KeyError):
			self.current_taxonomy = self.config['CollectionTaxonomy']
			
		try:
			self.Github_DataBase_ID = self.config['Github_DataBase_ID']
			self.Github_Taxonomy_ID = self.config['Github_Taxonomy_ID']
			self.Github_Username = self.config['Github_Username']
		except(KeyError):
			self.Github_DataBase_ID = '123456789'
			self.Github_Taxonomy_ID = '123456789'
			self.Github_Username = 'username'

		#################
		# JSON Database #
		#################

		# Load JSON database
		try:
			with open (Path(self.current_database), 'r') as file:
				loaddata = file.read()
		except(FileNotFoundError):
			self.current_database = Path(self.database_path) / 'sample_database.json'
			with open (Path(self.current_database), 'r') as file:
				loaddata = file.read()

		# Import JSON into a Dictionary
		self.database = json.loads(loaddata)
		        
		#######################
		# Annotation Taxonomy #
		#######################

		# Load Taxonomy
		try:
			with open (Path(self.current_taxonomy), 'r') as file:
				loaddata = file.read()
		except(FileNotFoundError):
			self.current_taxonomy = Path(self.database_path) / 'sample_taxonomy.json'
			with open (Path(self.current_taxonomy), 'r') as file:
				loaddata = file.read()

		self.taxonomy = json.loads(loaddata)

	##############################
	#   Reformatting Functions   #
	##############################

	def annotation_provenance_setter (self,annotation_list,level):
		# Adds provenance data to each cache annotation as a list [annotation,user,datetime]

		# Create Provenanced Annotation List
		listed_annotation_list = []
		for annotation in annotation_list:
			if level == 'i':
				listed_annotation_list.append([annotation,self.item_annotation_editor.get(),datetime.datetime.now().strftime('%Y%m%d_%H%M%S')])
			elif level == 's':
				listed_annotation_list.append([annotation,self.segment_annotation_editor.get(),datetime.datetime.now().strftime('%Y%m%d_%H%M%S')])

		# Return Provenanced Annotation List
		return listed_annotation_list

	def annotation_parent_setter(self,tree_name):
		# Ticks the Parents of Selected Annotations with the TreeView Widget
		# This is a Bug Fix to Prevent the Default 'Third State') of Parents Boxes

		# Create a List of All Checked Items
		annotation_list = tree_name.get_checked()

		# For Every Item in the List
		for annotation in annotation_list:

			# If that Item has a Parent and that Parent is not Already in the List
			if tree_name.parent(annotation) != "" and tree_name.parent(annotation) not in annotation_list:

				# Add Parent Item to the List
				annotation_list.append(tree_name.parent(annotation))

		# Return the Updated List of Annotations
		return annotation_list

	def annotation_list_updater(self,cache_annotations,saved_annotations):
		# Checks the cache annotations against the saved ones and merges the list (deleting any annotations no longer in cache but keeping old dates/users for exisiting ones)

		new_annotations = []

		# For every annotation in the current annotation list
		for cache_annotation in cache_annotations:

			found = False

			# Go through every annotation in the saved/disk annotation list
			for saved_annotation in saved_annotations:

				# If the annotation is the same
				if cache_annotation[0] == saved_annotation[0]:

						# keep it as it is and mark as found
						new_annotations.append(saved_annotation)
						found = True

			# If you never found the annotation, add it from the cached version
			if found == False:
				new_annotations.append(cache_annotation)

		## This will delete any annotations that have been removed. If you want a different annotation list for a different user, then make a new segment ##

		return new_annotations

	##############################
	#	  Saving Functions	  #
	##############################

	def configuration_file_saver(self,file):

		filepath = self.path_dictionary[file]

		with open (filepath, 'w') as file:
			file.write(self.configuration_textbox.get("1.0",END))

		self.pane_two.destroy()

	def configuration_defaults_saver(self):

		self.config['Database'] = str(self.current_database)
		self.config['Taxonomy'] = str(self.current_taxonomy)
		self.config['ImagePath'] = str(self.raw_data_images_path)
		self.config['GitPath'] = str(self.git_path)

		try:
			self.config['Github_DataBase_ID'] = str(self.github_database_ID_entry.get())
			self.config['Github_Taxonomy_ID'] = str(self.github_taxonomy_ID_entry.get())
			self.config['Github_Username'] = str(self.github_username_entry.get())
			
		except(AttributeError):
			self.config['Github_DataBase_ID'] = str(self.Github_DataBase_ID)
			self.config['Github_Taxonomy_ID'] = str(self.Github_Taxonomy_ID)
			self.config['Github_Username'] = str(self.Github_Username)

		try:
			for parameter in self.parameter_entries:
				self.config[parameter[0]] = parameter[1].get()
			
		except(AttributeError):
			pass

		with open(Path(self.config_path) / 'config.ini', 'w') as configfile:
			self.default_config.write(configfile)

	def database_entry_saver(self, level):
		# Saves Entries to Cached Database
		
		#############
		# All Items #
		#############

		# Update the collection bibliography type
		self.database[self.collection_index]['fabio_type'] = self.collections_type_namespace + self.default_collection_type.get()

		# For Every Item
		for entry in self.collection_entries:
		
			# Update the Record Editor Metadata
			if self.provenance_collection_editor.get() != self.database[self.collection_index]['schema:editor'][0]:
				self.database[self.collection_index]['schema:editor'][0] = self.provenance_collection_editor.get()
				self.database[self.collection_index]['schema:editor'][1] = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

			try:
				# Update the Database with the Item's Top-Level Entries
				if entry[2].get() != self.database[self.collection_index][entry[0]][1] or entry[1].get() != self.database[self.collection_index][entry[0]][0]:
					self.database[self.collection_index]['schema:editor'][2] = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

			except(KeyError):
				# Create the Database with the Item's Top-Level Entries
				if entry[1].get() !='':
					self.database[self.collection_index][entry[0]] = ["","",""]
					self.database[self.collection_index][entry[0]][0] = entry[1].get()
					self.database[self.collection_index][entry[0]][1] = entry[2].get()
					self.database[self.collection_index][entry[0]][2] = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
			else:
				self.database[self.collection_index][entry[0]][0] = entry[1].get()
				self.database[self.collection_index][entry[0]][1] = entry[2].get()
				self.database[self.collection_index][entry[0]][2] = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

			self.database[self.collection_index]['schema:editor'][2] = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

		###################
		# Mid-Level Items #
		###################

		# If Saving an Mid-Level Item
		if level == 'i':
		
			# Update the item bibliography type
			self.database[self.collection_index]['items'][self.item_index]['fabio_type'] = self.item_type_namespace + self.default_item_type.get()

			# Update the Record Editor Metadata
			if self.provenance_item_editor.get() != self.database[self.collection_index]['items'][self.item_index]['schema:editor'][0]:
				self.database[self.collection_index]['items'][self.item_index]['schema:editor'][0] = self.provenance_item_editor.get()
				self.database[self.collection_index]['items'][self.item_index]['schema:editor'][1] = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

			# Save the Annotation Tree to the Mid-Level
			try:
				cache_annotations = self.annotation_list_updater(self.annotation_provenance_setter(self.annotation_parent_setter(self.item_tree),level),self.database[self.collection_index]['items'][self.item_index]['annotations'])
			except(KeyError):
				cache_annotations = []

			self.database[self.collection_index]['items'][self.item_index]['annotations'] = cache_annotations
			self.database[self.collection_index]['items'][self.item_index]['schema:editor'][2] = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

			# Save any reference images/
			if self.reference_image_filename.get() != 'filename.jpg':
				self.database[self.collection_index]['items'][self.item_index]['reference_image_file'] = self.reference_image_filename.get()
				self.database[self.collection_index]['items'][self.item_index]['reference_image_file_rotation'] = self.reference_image_rotation

			# If it is a Text, Save the Transcription
			if self.database[self.collection_index]['items'][self.item_index]['item_type'] == 't':		
				self.database[self.collection_index]['items'][self.item_index]['transcription'][0] = re.sub('\s+',' ',self.transcription_text.get("1.0",END).rstrip())
				self.database[self.collection_index]['items'][self.item_index]['transcription'][1] = self.transcription_provenance_user.get()
				self.database[self.collection_index]['items'][self.item_index]['transcription'][2] = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
				self.database[self.collection_index]['items'][self.item_index]['schema:editor'][2] = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
				
			# If it is an Image, Save the Filepath
			elif self.database[self.collection_index]['items'][self.item_index]['item_type'] == 'i':
				self.database[self.collection_index]['items'][self.item_index]['image_file'] = self.image_filename.get()
				self.database[self.collection_index]['items'][self.item_index]['schema:editor'][2] = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')


		###################################
		# Mid-Level and Lower-Level Items #
		###################################

		# If Saving a Mid or Lower-Level Item
		if level == 'i' or level == 's':
			# Update the Database with the Item's Mid-Level Entries
			for entry in self.item_entries:
				try:
					# Update the Database with the Item's Top-Level Entries
					if entry[2].get() != self.database[self.collection_index]['items'][self.item_index][entry[0]][1] or entry[1].get() != self.database[self.collection_index]['items'][self.item_index][entry[0]][0]:
						self.database[self.collection_index]['items'][self.item_index]['schema:editor'][2] = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

				except(KeyError):
					# Create the Database with the Item's Top-Level Entries
					if entry[1].get() !='':
						self.database[self.collection_index]['items'][self.item_index][entry[0]] = ["","",""]
						self.database[self.collection_index]['items'][self.item_index][entry[0]][0] = entry[1].get()
						self.database[self.collection_index]['items'][self.item_index][entry[0]][1] = entry[2].get()
						self.database[self.collection_index]['items'][self.item_index][entry[0]][2] = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
				else:
					self.database[self.collection_index]['items'][self.item_index][entry[0]][0] = entry[1].get()
					self.database[self.collection_index]['items'][self.item_index][entry[0]][1] = entry[2].get()
					self.database[self.collection_index]['items'][self.item_index][entry[0]][2] = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

				self.database[self.collection_index]['items'][self.item_index]['schema:editor'][2] = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

		#####################
		# Lower-Level Items #
		#####################

		# If Saving a Lower-Level ITem
		if level == 's':

			# Update the segment bibliography type
			self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['fabio_type'] = self.default_segment_type.get()

			# Update the Record Editor Metadata
			if self.provenance_segment_editor.get() != self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['schema:editor'][0]:
				self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['schema:editor'][0] = self.provenance_segment_editor.get()
				self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['schema:editor'][1] = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

			# Save the Annotation Tree to the Lower Level
			try:
				cache_annotations = self.annotation_list_updater(self.annotation_provenance_setter(self.annotation_parent_setter(self.segment_tree),level),self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['annotations'])
			except(KeyError):
				cache_annotations = []
			self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['annotations'] = cache_annotations

			# If it is a Text, Save the Word Segmenters
			if self.database[self.collection_index]['items'][self.item_index]['item_type'] == 't':
				self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['start'] = int(self.start_text.get())
				self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['end'] = int(self.end_text.get())
				self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['schema:editor'][2] = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

			# If it is an Image, Save the Image Percentages
			elif self.database[self.collection_index]['items'][self.item_index]['item_type'] == 'i':
				self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['top'] = int(self.top_text.get())
				self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['bottom'] = int(self.bottom_text.get())
				self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['right'] = int(self.right_text.get())
				self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['left'] = int(self.left_text.get())
				self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['schema:editor'][2] = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

			# Save free-form notes
			self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['nisaba:notes'] = [self.note_text.get("1.0",END).rstrip(),self.segment_note_editor.get(),datetime.datetime.now().strftime('%Y%m%d_%H%M%S')]
			
				
			# Update the Database with the Item's Lower-Level Entries
			for entry in self.segment_entries:

				try:
					# Update the Database with the Item's Top-Level Entries
					if entry[2].get() != self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index][entry[0]][1] or entry[1].get() != self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index][entry[0]][0]:
						self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['schema:editor'][2] = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

				except(KeyError):
					# Create the Database with the Item's Top-Level Entries
					if entry[1].get() !='':
						self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index][entry[0]] = ["","",""]
						self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index][entry[0]][0] = entry[1].get()
						self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index][entry[0]][1] = entry[2].get()
						self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index][entry[0]][2] = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
				else:
					self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index][entry[0]][0] = entry[1].get()
					self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index][entry[0]][1] = entry[2].get()
					self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index][entry[0]][2] = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

				self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['schema:editor'][2] = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

		#################
		# Save Database #
		#################

		# Save Cached Database to Disk
		self.database_saver()

	def taxonomy_saver(self):
		# Saves Taxononmy Definitions

		def entry_retriever(database,key):
			# Retrieves entries from Taxonomy Form
			
			database[key]['iid'] = self.taxonomy_iid_entry.get()
			database[key]['name'] = self.taxonomy_annotation_entry.get()
			database[key]['type'] = self.taxonomy_type_entry.get()
			database[key]['definition'] = self.taxonomy_detail_entry.get()
			database[key]['reference'] = self.taxonomy_reference_entry.get("1.0",END)

		# Save All Entries to Cached Taxonomy Database
		self.iid_iterator(self.taxonomy,self.clicked_item,entry_retriever)

		# Convert Database to JSON
		savedata = json.dumps(self.taxonomy, indent=4)

		# Save JSON to Disk
		with open (self.current_taxonomy, 'w') as file:
			file.write(savedata)
			
		# Reload Taxonomy Window
		self.taxonomy_viewer(self.taxonomy_window,self.switcher_active)

	def database_saver(self):
		# Save Cached Database to Disk

		# Convert Database to JSON
		savedata = json.dumps(self.database, indent=4)

		# Save JSON to disk
		with open (Path(self.current_database), 'w') as file:
			file.write(savedata)

		# Save Date-Stamped Backup of Database to Backups
		backup_filename = 'database_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.json'
		with open (Path(self.database_backup_path) / backup_filename, 'w') as file:
			file.write(savedata)

	##############################
	#	 Loading Functions	  #
	##############################

	def configuration_file_loader(self,event):

		file = self.path_dictionary[event]

		#file = Path(self.config_path) / directory / event[0]
		with open (file, 'r') as file:
			loaddata = file.read()

		return loaddata

	def database_loader(self,type,function_call):
		# Loads a New (non-default) JSON Database

		if type == 'g':
			folder = askdirectory()
			self.git_path=Path(folder)

		elif type == 'ip':
			folder = askdirectory()
			self.raw_data_images_path=Path(folder)

		else:

			# Load Database
			file = askopenfilename(initialdir = self.database_path,title = "Select Database",filetypes = (("json files","*.json"),("all files","*.*")))

			if type == 'd':

				self.current_database = Path(file)

				with open (file, 'r') as file:
					loaddata = file.read()
				self.database = json.loads(loaddata)

			elif type == 't': self.current_taxonomy=Path(file)
			elif type == 'Item': self.current_taxonomy=Path(file)
			elif type == 'Segment': self.current_taxonomy=Path(file)

		function_call()

	##############################
	#	Creating Functions	  #
	##############################

	def configuration_file_creator(self):

		self.default_config = configparser.ConfigParser()

		try:
			self.default_config.read(Path(self.config_path) / 'config.ini')
			self.config = self.default_config['custom']
		except(FileNotFoundError,KeyError):
			self.default_config = configparser.ConfigParser()
			self.default_config['DEFAULT']['Database'] = 'Path(self.database_path) / "database.json"'
			self.default_config['DEFAULT']['Taxonomy'] = 'Path(self.database_path) / "taxonomy.json"'
			self.default_config['DEFAULT']['ImagePath'] = 'Path(self.database_path) / images/'
			self.default_config['DEFAULT']['GitPath'] = 'Path(self.database_path)'
			self.default_config['DEFAULT']['Github_DataBase_ID'] = '1234567890'
			self.default_config['DEFAULT']['Github_Taxonomy_ID'] = '1234567890'
			self.default_config['DEFAULT']['Github_Username'] = 'username'
			self.default_config['DEFAULT']['v_Collection_Namespace'] = 'fabio:'
			self.default_config['DEFAULT']['v_Item_Namespace'] = 'fabio:'
			self.default_config['DEFAULT']['v_Segment_Namespace'] = 'fabio:'
			self.default_config['DEFAULT']['v_Collection_Title_Field'] = 'dc:title'
			self.default_config['DEFAULT']['v_Item_Title_Field'] = 'dc:title'
			self.default_config['DEFAULT']['v_Segment_Title_Field'] = 'dc:title'
			self.default_config['custom'] = {}
			self.config = self.default_config['custom']

	def configuration_yaml_creator(self):
		# Create new config file

		file = asksaveasfile(initialdir = self.config_path, mode='w', defaultextension=".yaml")
		if file is None:
			return

		data = '"namespace:element" : "Text"'

		file.write(data)
		file.close()

		self.default_database_panels_displayer()

	def database_creator(self):
		# Create new database

		file = asksaveasfile(mode='w', defaultextension=".json")
		if file is None:
			return

		data = '{"users":{"nid":{"schema:givenName":"New","schema:familyName":"User","schema:sameAS":"","schema:worksFor":"","schema:memberOf":"","schema:email":"","foaf:homepage":"","default":1}},"0":{"schema:editor":["","",""],"dc:title":["New Collection","",""],"items":{},"dc:creator":["","",""]}}'

		file.write(data)
		file.close()
