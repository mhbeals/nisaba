# Import External Libaries
import json
import datetime
from pathlib import Path
from rdflib import Graph, URIRef, Namespace, RDF, RDFS, Literal
import urllib.parse
import os
import csv

# Import tkinter Libraries
from tkinter import END
from tkinter.filedialog import askopenfilename

class database_maintenance:

	# Set Relative Paths
	assets_path = os.path.join(os.path.dirname(__file__), "assets/")
	config_path = os.path.join(os.path.dirname(__file__), "config_files/")
	user_config_path = os.path.join(os.path.dirname(__file__), "config_files/user_defined")
	raw_data_images_path = os.path.join(os.path.dirname(__file__), "raw_data/images/")
	database_path = os.path.join(os.path.dirname(__file__), "databases/")
	database_backup_path = database_path + "backups/" 

	def __init__(self):
		# Initialise programme with stored databases
		
		self.defaults = []

		# Populate dictionary with imported file
		try: 
			with open (Path(self.user_config_path) / 'user_defined_defaults.txt', 'r') as file:
				reader = csv.reader(file,delimiter='\n')
				for line in reader:
					self.defaults.append(line[0])
		except(FileNotFoundError):
		
			with open (Path(self.config_path) / 'sample_defaults.txt', 'r') as file:
				reader = csv.reader(file,delimiter='\n')
				for line in reader:
					self.defaults.append(line[0])
					
		self.current_database = self.defaults[0]	
		self.current_taxonomy = self.defaults[1]
		self.taxonomy_level_defaults = [self.defaults[1],self.defaults[2],self.defaults[3]]

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
		
		################
		# RDF Database #
		################
		
		# Create a Blank Graph
		self.database_rdf = Graph()
		
		#######################
		# Annotation Taxonomy #
		#######################
		
		# Load Taxonomy
		
		try:
			with open (Path(self.current_taxonomy), 'r') as file:
				loaddata = file.read()
		except(FileNotFoundError):
			self.current_taxonomy = Path(self.database_path) / 'sample_taxonomy.json'
			self.taxonomy_level_defaults = [self.current_taxonomy,self.current_taxonomy,self.current_taxonomy]
			with open (Path(self.current_taxonomy), 'r') as file:
				loaddata = file.read()
				
			self.taxonomy = json.loads(loaddata)
			

	def iid_iterator(self,database,iid,function_call):
		# Search through Database for a Specific Branch or Child
		# Works on Any # - IID,Children - # Database
	
		# Go Through Database Items
		for key,value in database.items():
		
			# Check for Passed-Through IID
			if value['iid'] == iid:
			
				# Call Passed-Through Function
				function_call(database,key)
				break
			
			# If Not Found
			else:
			
				# Run Recursively
				self.iid_iterator(value['children'],iid,function_call)

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

		# Map the saved JSON into RDF
		self.rdf_mapper()

	def rdf_mapper(self):
		# Map the JSON database to RDF
	
		# Load previous triples, if any
		self.database_rdf.parse(self.database_path + "sample_database.ttl", format='turtle')

		# Set URIs
		nisaba_vocab_uri = URIRef('http://purl.org/nisaba/vocab#')
		nisaba_resource_uri = URIRef('http://purl.org/nisaba/')
		nisaba_collection_uri = URIRef('http://purl.org/nisaba/collection/')
		nisaba_v = Namespace(nisaba_vocab_uri)
		nisaba_r = Namespace(nisaba_resource_uri)
		nisaba_c = Namespace(nisaba_collection_uri)

		# Go Through Cached Database and Update RDF Graph
		for c,v in self.database.items():
			collection_uri = nisaba_c[c]
			self.database_rdf.add(( collection_uri, RDF.type, nisaba_v['CollectionEntry']))
			if 'collection_title' in v:
				self.database_rdf.add(( collection_uri, nisaba_v['collection_title'], Literal(v['collection_title']) ))
			if 'collection_date' in v:
				self.database_rdf.add(( collection_uri, nisaba_v['collection_date'], Literal(v['collection_date']) ))
			if 'collection_holder' in v:
				self.database_rdf.add(( collection_uri, nisaba_v['collection_holder'], Literal(v['collection_holder']) ))
			if 'collection_holder_reference' in v:
				self.database_rdf.add(( collection_uri, nisaba_v['collection_holder_reference'], Literal(v['collection_holder_reference']) ))
			if 'collection_holder_original' in v:
				self.database_rdf.add(( collection_uri, nisaba_v['collection_holder_original'], Literal(v['collection_holder_original']) ))
			if 'collection_holder_reference_original' in v:
				self.database_rdf.add(( collection_uri, nisaba_v['collection_holder_reference_original'], Literal(v['collection_holder_reference_original']) ))
			if 'collection_place_of_publication' in v:
				self.database_rdf.add(( collection_uri, nisaba_v['collection_place_of_publication'], Literal(v['collection_place_of_publication']) ))
			if 'collection_author' in v:
				self.database_rdf.add(( collection_uri, nisaba_v['collection_author'], Literal(v['collection_author']) ))

			if 'items' in self.database[c]:
				for i,v in self.database[c]['items'].items():
					item_uri = URIRef(nisaba_c[c] + '/item/' + i)
					self.database_rdf.add(( collection_uri, nisaba_v['hasItem'], item_uri ))
					self.database_rdf.add(( item_uri, RDF.type, nisaba_v['ItemEntry']))
					if 'item_type' in v:
						self.database_rdf.add(( item_uri, nisaba_v['item_type'], Literal(v['item_type']) ))
					if 'item_title' in v:
						self.database_rdf.add(( item_uri, nisaba_v['item_title'], Literal(v['item_title']) ))
					if 'image_file' in v:
						self.database_rdf.add(( item_uri, nisaba_v['image_file'], Literal(v['image_file']) ))
					if 'item_author' in v:
						self.database_rdf.add(( item_uri, nisaba_v['item_author'], Literal(v['item_author']) ))
					if 'item_date' in v:
						self.database_rdf.add(( item_uri, nisaba_v['item_date'], Literal(v['item_date']) ))
					if 'item_page_number' in v:
						self.database_rdf.add(( item_uri, nisaba_v['item_page_number'], Literal(v['item_page_number']) ))
					if 'item_document_number' in v:
						self.database_rdf.add(( item_uri, nisaba_v['item_document_number'], Literal(v['item_document_number']) ))
					if 'transcription' in v:
						self.database_rdf.add(( item_uri, nisaba_v['transcription'], Literal(v['transcription']) ))
					if 'annotations' in v:
						for a in v['annotations']:
							self.database_rdf.add(( item_uri, nisaba_v['hasAnnotation'], Literal(a) ))
					if 'segments' in v:
						for s,v in self.database[c]['items'][i]['segments'].items():
							segment_uri = URIRef(item_uri + '/segment/' + s)
							self.database_rdf.add(( item_uri, nisaba_v['hasSegment'], segment_uri ))
							self.database_rdf.add(( segment_uri, RDF.type, nisaba_v['SegmentEntry']))
							if 'start' in v:
								self.database_rdf.add(( segment_uri, nisaba_v['start'], Literal(v['start']) ))
							if 'end' in v:
								self.database_rdf.add(( segment_uri, nisaba_v['end'], Literal(v['end']) ))
							if 'top' in v:
								self.database_rdf.add(( segment_uri, nisaba_v['top'], Literal(v['top']) ))
							if 'bottom' in v:
								self.database_rdf.add(( segment_uri, nisaba_v['bottom'], Literal(v['bottom']) ))
							if 'left' in v:
								self.database_rdf.add(( segment_uri, nisaba_v['left'], Literal(v['left']) ))
							if 'right' in v:
								self.database_rdf.add(( segment_uri, nisaba_v['right'], Literal(v['right']) ))
							if 'dc:description' in v:
								self.database_rdf.add(( segment_uri, nisaba_v['dc:description'], Literal(v['dc:description']) ))
							if 'annotations' in v:
								for a in v['annotations']:
									self.database_rdf.add(( segment_uri, nisaba_v['hasAnnotation'], Literal(a) ))

		self.database_rdf.bind('nisaba', nisaba_v)

		############
		# Save RDF #
		############
		
		# Save RDF
		with open(Path(self.database_path) / 'sample_database.ttl', 'wb') as file:
			file.write(self.database_rdf.serialize(format='turtle'))

		# Save Date-Stamped Backup of RDF in Backups
		backup_filename = 'database_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.ttl'
		with open(Path(self.database_backup_path) / backup_filename, 'wb') as file:
			file.write(self.database_rdf.serialize(format='turtle'))
	
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
				
		return new_annotations
		
	def database_entry_saver(self, level):
		# Saves Entries to Cached Database
		
		#############
		# All Items #
		#############
		
		# For Every Item
		for entry in self.collection_entries:
		
			# Update the Record Editor Metadata
			if self.provenance_collection_editor != self.database[self.collection_index]['schema:editor'][0]:
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

			# Update the Record Editor Metadata
			if self.provenance_item_editor != self.database[self.collection_index]['items'][self.item_index]['schema:editor'][0]:
				self.database[self.collection_index]['items'][self.item_index]['schema:editor'][0] = self.provenance_item_editor.get()
				self.database[self.collection_index]['items'][self.item_index]['schema:editor'][1] = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
				
			# Save the Annotation Tree to the Mid-Level
			cache_annotations = self.annotation_list_updater(self.annotation_provenance_setter(self.annotation_parent_setter(self.item_tree),level),self.database[self.collection_index]['items'][self.item_index]['annotations'])
			self.database[self.collection_index]['items'][self.item_index]['annotations'] = cache_annotations
			self.database[self.collection_index]['items'][self.item_index]['schema:editor'][2] = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

			# If it is a Text, Save the Transcription
			if self.database[self.collection_index]['items'][self.item_index]['item_type'] == 't':
				self.database[self.collection_index]['items'][self.item_index]['transcription'][0] = self.transcription_text.get("1.0",END)
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
		
			# Update the Record Editor Metadata
			if self.provenance_segment_editor != self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['schema:editor'][0]:
				self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['schema:editor'][0] = self.provenance_segment_editor.get()
				self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['schema:editor'][1] = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

			# Save the Annotation Tree to the Lower Level
			cache_annotations = self.annotation_list_updater(self.annotation_provenance_setter(self.annotation_parent_setter(self.segment_tree),level),self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['annotations'])
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

	def database_loader(self,type,function_call):
		# Loads a New (non-default) JSON Database
		
		# Load Database
		file = askopenfilename(initialdir = self.database_path,title = "Select Database",filetypes = (("json files","*.json"),("all files","*.*")))
		
		if type == 'd': 
		
			self.current_database = Path(file)
			
			with open (file, 'r') as file:
				loaddata = file.read()
			self.database = json.loads(loaddata)
			
		elif type == 'Collection': self.taxonomy_level_defaults[0]=Path(file)
		elif type == 'Item': self.taxonomy_level_defaults[1]=Path(file)
		elif type == 'Segment': self.taxonomy_level_defaults[2]=Path(file)
		
		function_call()

	def taxonomy_saver(self):
		# Saves Taxononmy Definitions

		def entry_retriever(database,key):
			# Retrieves entries from Taxonomy Form
			
			database[key]['iid'] = self.taxonomy_iid_entry.get()
			database[key]['name'] = self.taxonomy_annotation_entry.get()
			database[key]['type'] = self.taxonomy_type_entry.get()
			database[key]['definition'] = self.taxonomy_detail_entry.get()

		# Save All Entries to Cached Taxonomy Database
		self.iid_iterator(self.taxonomy,self.clicked_item,entry_retriever)
		
		# Reload Taxonomy Window
		self.taxonomy_viewer(self.taxonomy_window)

		# Convert Database to JSON
		savedata = json.dumps(self.taxonomy, indent=4)

		# Save JSON to Disk
		with open (Path(self.database_path) / "taxonomy.json", 'w') as file:
			file.write(savedata)
