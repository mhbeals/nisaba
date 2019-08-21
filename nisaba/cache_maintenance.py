try:
	# Used when executing with Python
	from database_maintenance import *
except ModuleNotFoundError:
	# Used when calling as library
	from nisaba.database_maintenance import *

class cache_maintenance(database_maintenance):

	##############################
	#         Navigation         #
	##############################

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

	def database_renumberer(self,database):
	
		if len(database) != 0:
			i = 0
		else:
			i = 1
		
		while i < len(database)+1:
			if str(i) in database:
				i = i + 1
			else:
				if str(i+1) in database:
					database[str(i)] = database[str(i+1)]
					del database[str(i+1)]
				else:
					break
	
	def default_user_setter(self):

	# Set everyone to 0
		for key,value in self.database['users'].items():
			value['default'] = 0

		# Set this user to default (1)
		self.database['users'][self.current_user.get()]['default'] = 1

		self.database_saver()
	
	def database_alphabetiser(self,database):
		# Alphabetise Taxonomy
		alpha_taxonomy = []
		for item,dictionary in database.items():
			alpha_taxonomy.append(dictionary['iid'])
		alpha_taxonomy = sorted(alpha_taxonomy)
		return alpha_taxonomy
	
	##############################
	#           Adding           #
	##############################
	
	def collection_adder(self):

		i = -1
		loop = 1

		while loop == 1:
			i = i + 1
			loop = str(i) in self.database

		self.database[str(i)]= {"schema:editor":["","",""],'items' : {}}

		self.database_panels_displayer(self.database_window)
		
	def item_adder(self,type):

		i = -1
		loop = 1

		while loop == 1:
			i = i + 1
			loop = str(i) in self.database[self.collection_index]['items']

		if type == 'i':
			self.database[self.collection_index]['items'][str(i)]= {"schema:editor":["","",""],'item_type': 'i','annotations':[],'image_file': 'sample.jpg', 'segments' : {}}

		elif type == 't':
			self.database[self.collection_index]['items'][str(i)]= {"schema:editor":["","",""],'item_type': 't', 'annotations':[],'transcription': ['','',''], 'segments' : {}}
			
		else:
			pass

		self.collection_item_list_panel_displayer()

	def segment_adder(self):

		i = -1
		loop = 1

		while loop == 1:
			i = i + 1
			loop = str(i) in self.database[self.collection_index]['items'][self.item_index]['segments']


		if  self.database[self.collection_index]['items'][self.item_index]['item_type'] == 't':
			self.database[self.collection_index]['items'][self.item_index]['segments'][str(i)] = {"schema:editor":["","",""],'start':0,'end':len(self.database[self.collection_index]['items'][self.item_index]['transcription'][0].split()),'annotations':[]}

		elif self.database[self.collection_index]['items'][self.item_index]['item_type'] == 'i':
			self.database[self.collection_index]['items'][self.item_index]['segments'][str(i)] = {"schema:editor":["","",""],'top':0,'right':50,'bottom':50,'left':0,'annotations':[]}

		self.item_panels_displayer('s')

	def root_adder(self):
		# Add a Taxon Root

		# Set Loop Variables
		i = -1
		loop = 1

		while loop:
			i = i + 1
			loop = str(i) in self.taxonomy

		# Create new Root with Default Fields
		self.taxonomy[i] = {}
		self.taxonomy[i]['iid'] = "_New_Root"
		self.taxonomy[i]['name'] = "New Root"
		self.taxonomy[i]['type'] = "New Root"
		self.taxonomy[i]['definition'] = "New Root"
		self.taxonomy[i]['children'] = {}

		# Reload Taxonomy Viewer
		self.taxonomy_viewer(self.taxonomy_window)

	def child_adder(self,database,key):
		# Add a Taxon Child

		# Set Loop Variables
		i = -1
		loop = 1

		# Ascend Numerically until First Missing Number
		while loop:
			i = i + 1
			loop = str(i) in database[key]['children']
		
		# Create New Child with Default Fields
		database[key]['children'][i] = {}
		database[key]['children'][i]['iid'] = "New_Item_" + str(i)
		database[key]['children'][i]['name'] = "New Item " + str(i)
		database[key]['children'][i]['type'] = "New Item " + str(i)
		database[key]['children'][i]['definition'] = "New Item " + str(i)
		database[key]['children'][i]['children'] = {}
		
		savedata = json.dumps(self.taxonomy, indent=4)

		# Save JSON to Disk
		with open (self.current_taxonomy, 'w') as file:
			file.write(savedata)

		# Reload Taxonomy Viewer
		self.taxonomy_viewer(self.taxonomy_window)
	
	##############################
	#           Deleting         #
	##############################

	def user_deleter(self,current_user):
		# Delete a User

		# Delete User from Cached Database
		del self.database['users'][current_user]
		
		# Save Cached Database to Disk
		self.database_saver()
		
		# Clear Metadata Window
		self.metadata_window.destroy()

	def element_deleter(self,database,key):
		# Delete a Taxon

		# Delete Current Key
		del database[key]

		# Reload Taxonomy Viewer
		self.taxonomy_viewer(self.taxonomy_window)

	def unit_deleter(self,database,key,level):
	
		del database[key]
		
		if level == 'c':
			self.database_renumberer(database)
			self.database_panels_displayer(self.database_window)
		
		elif level == 'i':
			self.database_renumberer(database)
			self.collection_item_list_panel_displayer()
		
		elif level == 's':
			self.database_renumberer(database)
			self.item_panels_displayer('s')
	
	##############################
	#           Saving           #
	##############################
	
	def metadata_entry_saver(self,current_user):
		# Save a User's Metadata
		
		# Update Current User
		if current_user in self.database['users']:
			
			# Go through the rest of the entries and save the vaule
			for entry in self.entries:
				self.database['users'][current_user][entry[0]] = entry[1].get()
					
		else:
		
			# Create new entry in database
			self.database['users'][current_user] = {}
			
			# Go through the entries and save the vaule
			for entry in self.entries:
					self.database['users'][current_user][entry[0]] = entry[1].get()
					
			self.database['users'][current_user]['default'] = 0
		
		# Save Cached Database to Disk
		self.database_saver()
		
		# Clear Metadata Window
		self.metadata_window.destroy()
	
