try:
	# Used when executing with Python
	from database_maintenance import *
	from cache_maintenance import *
	from tooltip_creation import *
	from scrollframe_builder import *
except ModuleNotFoundError:
	# Used when calling as library
	from nisaba.database_maintenance import *
	from nisaba.cache_maintenance import *
	from nisaba.tooltip_creation import *
	from nisaba.scrollframe_builder import *

# Import TKinter Libraries
from tkinter import *
from tkinter import END
from tkinter import ttk
from tkinter.ttk import *

class taxonomy_display(cache_maintenance):

	#########################
	#   Field Populators    #
	#########################
	
	def taxon_branch_builder(self,database,key):
	# Populates tree branches with data
		
		# Set Taxon Dictionary
		dictionary = database[key]
		
		# Create Root
		top=self.taxonomy_tree.insert("", "end", dictionary['iid'], text=dictionary['name'], values=(dictionary['type'],dictionary['definition']),open = True)

		def individual_branch_builder(child_dictionary,parent_branch):
		# Recursive Function to Go Through an Unknown Number of Layers

			# Alphabetise children
			alpha_taxonomy = self.database_alphabetiser(child_dictionary)
		
			# Create Lambda Dictionary
			x, d = -1, {}
			
			# Go Through Every Key (Numerical Values) in Current "children" Dictionary
			for taxon in alpha_taxonomy:
				
				for key,value in child_dictionary.items():
					
					if value['iid'] == taxon:
					
						# Set Child Dictionary
						new_dictionary = value
					
						# Advance Branch Lambda Variable
						x = x + 1
						
						# Create New Branch
						d[x+1]=self.taxonomy_tree.insert(parent_branch, "end", new_dictionary['iid'], text=new_dictionary['name'],values=(new_dictionary['type'],new_dictionary['definition']),open = True)

				# Re-Run Recursive Function with New "children" Dictionary
				individual_branch_builder(new_dictionary['children'],d[x+1])

		# Begin Recursive Function
		individual_branch_builder(dictionary['children'],top)
	
	def taxon_metadata_field_displayer(self,database,key):
	# Populates entry boxes from disks

		# Reload Display Editor
		self.taxon_editor_displayer()

		# Fill in the Entries with Selected Item
		self.taxonomy_iid_entry.insert(0,database[key]['iid'])
		self.taxonomy_annotation_entry.insert(0,database[key]['name'])
		self.taxonomy_type_entry.insert(0,database[key]['type'])
		self.taxonomy_detail_entry.insert(0,database[key]['definition'])

	#########################
	#   Event Processing    #
	#########################			
		
	def taxon_informer(self,event):
	# Send Selected ID to Iterator

		# Get Selected ID from Click Event
		self.clicked_item = self.taxonomy_tree.identify('item',event.x,event.y)

		# Send to iid_iterator
		self.iid_iterator(self.taxonomy,self.taxonomy_tree.identify('item',event.x,event.y),self.taxon_metadata_field_displayer)

	#####################
	#   Panel Display   #
	#####################		
		
	def taxon_editor_displayer(self):
	# Displays Taxon Editor Panel
	
		# Delete Any Existing Information
		try:
			self.pane_two.destroy()
		except (NameError, AttributeError):
			pass

		# Setup Taxonomy Window Panels
		self.pane_two = ttk.Frame(self.taxonomy_window)
		self.pane_two.place(relx=.5, relwidth=.5, relheight=1)

		# Create static entry widgets
		iid_row = ttk.Frame(self.pane_two)
		annotation_row = ttk.Frame(self.pane_two)
		type_row = ttk.Frame(self.pane_two)
		detail_row = ttk.Frame(self.pane_two)
		self.taxonomy_iid_entry = ttk.Entry(iid_row)
		self.taxonomy_annotation_entry = ttk.Entry(annotation_row)
		self.taxonomy_type_entry = ttk.Entry(type_row)
		self.taxonomy_detail_entry = ttk.Entry(detail_row)
		entries = [(self.taxonomy_iid_entry,iid_row),(self.taxonomy_annotation_entry,annotation_row),(self.taxonomy_type_entry,type_row),(self.taxonomy_detail_entry,detail_row)]
		
		def row_builder(current_entry,current_row):
			row = ttk.Frame(self.pane_two)
			label =ttk.Label(row, text="ID", anchor='w', width=10)
			label.pack(side=LEFT)
			current_entry.pack(side=RIGHT, expand=YES, fill=X)
			current_row.pack(side=TOP, fill=X, padx=5, pady=5)
			
		for entry in entries:
			row_builder(entry[0],entry[1])

		# Create Add/Save/Delete Button Set
		row = ttk.Frame(self.pane_two)
		self.add_button = Button(row, image=self.add_icon, command=(lambda: self.iid_iterator(self.taxonomy,self.taxonomy_iid_entry.get(),self.child_adder)))
		add_button_tt = ToolTip(self.add_button, "Add Child Taxon",delay=0.01)
		self.add_button.pack(side=LEFT)
		self.save_button = Button(row, image=self.save_icon, command=self.taxonomy_saver)
		save_button_tt = ToolTip(self.save_button, "Save Current Taxon",delay=0.01)
		self.save_button.pack(side=LEFT)
		self.delete_button = Button(row, image=self.delete_icon, command=(lambda: self.iid_iterator(self.taxonomy,self.taxonomy_iid_entry.get(),self.element_deleter)))
		delete_button_tt = ToolTip(self.delete_button, "Delete Current Taxon",delay=0.01)
		self.delete_button.pack(side=LEFT)
		row.pack()

	def taxon_tree_displayer(self):
	# Displays Taxonomy Tree Panel
	
		# Determine Window Size / Screen Resolution
		window_width = self.taxonomy_window.winfo_screenwidth()
		window_height = self.taxonomy_window.winfo_screenheight()
	
		# Create Tree
		self.taxonomy_tree = ttk.Treeview(self.pane_one,height=int(window_height/22),selectmode='browse')

		# Create Tree Layout
		self.taxonomy_tree["columns"]=("Type","Detail","")
		self.taxonomy_tree.column("#0", minwidth=int(window_width/24*2.5), stretch=1)
		self.taxonomy_tree.column("Type", minwidth=int(window_width/24),  stretch=1)
		self.taxonomy_tree.column("Detail", minwidth=int(window_width/3.68), stretch=1)
		self.taxonomy_tree.heading("#0",text="Annotation",anchor=W)
		self.taxonomy_tree.heading("Type", text="Type",anchor=W)
		self.taxonomy_tree.heading("Detail", text="Detail",anchor=W)

		# Alphabetise Taxonomy
		alpha_taxonomy = self.database_alphabetiser(self.taxonomy)
		
		# Go through taxonomy alphabetically and build branches
		for taxon in alpha_taxonomy:
			self.iid_iterator(self.taxonomy,taxon,self.taxon_branch_builder)
			
		# Display Tree
		self.taxonomy_tree.pack()
		self.taxonomy_tree.bind('<Button-1>', self.taxon_informer)
		
		# Create Add/Save/Delete Button Set
		row = ttk.Frame(self.pane_one)
		self.add_button = Button(row, image=self.add_icon, command=self.root_adder)
		add_button_tt = ToolTip(self.add_button, "Add Root Taxon",delay=0.01)
		self.add_button.pack(side=LEFT)
		self.delete_button = Button(row, image=self.delete_icon, command=(lambda: self.iid_iterator(self.taxonomy,self.taxonomy_iid_entry.get(),self.element_deleter)))
		delete_button_tt = ToolTip(self.delete_button, "Delete Current Taxon",delay=0.01)
		self.delete_button.pack(side=LEFT)
		row.pack()
		
	########################
	#         Main         #
	########################	
		
	def taxonomy_viewer(self,window):
	# Displays the Taxonomy Panels

		# Set Icon Assets
		# Menu Bar Icons made by Pixel Buddha (https://www.flaticon.com/authors/pixel-buddha) from http://www.flaticon.com  CC-BY (http://creativecommons.org/licenses/by/3.0/)
		self.up_level_icon=PhotoImage(file=Path(self.assets_path) / 'uplevel.png')
		self.add_icon=PhotoImage(file=Path(self.assets_path) / 'add.png')
		self.delete_icon=PhotoImage(file=Path(self.assets_path) / 'delete.png')
		self.save_icon=PhotoImage(file=Path(self.assets_path) / 'save.png')
		self.refresh_icon=PhotoImage(file=Path(self.assets_path) / 'refresh.png')

		##################
		# Window Cleanup #
		##################

		# Delete Previous Panels and Menus or Create New Window
		try:
			self.pane_one.destroy()
			self.pane_two.destroy()
		except (NameError, AttributeError):
			pass

		###################
		# Taxonomy Window #
		###################

		# Setup Taxonomy Window
		self.taxonomy_window = window
		
		# Setup Taxonomy Window Panels
		self.pane_one = ttk.Frame(self.taxonomy_window)
		self.pane_two = ttk.Frame(self.taxonomy_window)
		self.pane_one.place(relwidth=.5, relheight=1)
		self.pane_two.place(relx=.5, relwidth=.5, relheight=1)

		# Set Up Annotation Selection (Tree) Panel 
		self.taxon_tree_displayer()

		# Set Up Definition Editor Panel 
		self.taxon_editor_displayer()
		
		
