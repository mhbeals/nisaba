try:
	# Used when executing with Python
	from database_maintenance import *
except ModuleNotFoundError:
	# Used when calling as library
	from nisaba.database_maintenance import *

# Import TKinter Libraries
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *

class taxonomy_display(database_maintenance):

	def root_adder(self):
		# Add a Taxon Root

		# Set Loop Variables
		i = -1
		loop = TRUE

		
		while loop:
			i = i + 1
			loop = str(i) in self.taxonomy

		# Create new Root with Default Fields
		self.taxonomy[i] = {}
		self.taxonomy[i]['iid'] = "New_Root"
		self.taxonomy[i]['name'] = "New Root"
		self.taxonomy[i]['type'] = "New Root"
		self.taxonomy[i]['definition'] = "New Root"
		self.taxonomy[i]['children'] = {}

		# Reload Taxonomy Viewer
		self.taxonomy_viewer()

	def child_adder(self,database,key):
		# Add a Taxon Child

		# Set Loop Variables
		i = -1
		loop = TRUE

		# Ascend Numerically until First Missing Number
		while loop:
			i = i + 1
			loop = str(i) in database[key]['children']

		# Create New Child with Default Fields
		database[key]['children'][i] = {}
		database[key]['children'][i]['iid'] = "New_Item"
		database[key]['children'][i]['name'] = "New Item"
		database[key]['children'][i]['type'] = "New Item"
		database[key]['children'][i]['definition'] = "New Item"
		database[key]['children'][i]['children'] = {}

		# Reload Taxonomy Viewer
		self.taxonomy_viewer()

	def element_deleter(self,database,key):
		# Delete a Taxon

		# Delete Current Key
		del database[key]
		
		# Reload Taxonomy Viewer
		self.taxonomy_viewer()

	def entry_filler(self,database,key):
		# Fill in entry boxes

		# Reload Display Editor 
		self.display_editor()
		
		# Fill in the Entries with Selected Item
		self.taxonomy_iid_entry.insert(0,database[key]['iid'])
		self.taxonomy_annotation_entry.insert(0,database[key]['name'])
		self.taxonomy_type_entry.insert(0,database[key]['type'])
		self.taxonomy_detail_entry.insert(0,database[key]['definition'])

	def tree_item_informer(self,event):
		# Send Selected ID to Iterator
		
		# Get Selected ID from Click Event
		self.clicked_segment = self.taxonomy_tree.identify('segment',event.x,event.y)
		
		# Send to iid_iterator
		self.iid_iterator(self.taxonomy,self.taxonomy_tree.identify('segment',event.x,event.y),self.entry_filler)

	def display_editor(self):

		# Delete Any Existing Information
		try:
			self.taxonomy_pane_two.destroy()
		except (NameError, AttributeError):
			pass

		# Setup Taxonomy Window Panels (45/65 Split)
		split = 0.45
		self.taxonomy_pane_two = Frame(self.taxonomy_window)
		self.taxonomy_pane_two.place(relx=split, relwidth=1.0-split, relheight=1)

		# Create ID Row
		row = Frame(self.taxonomy_pane_two)
		self.taxonomy_iid_label = Label(row, text="ID", anchor='w', width=10)
		self.taxonomy_iid_entry = Entry(row)
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		self.taxonomy_iid_label.pack(side=LEFT)
		self.taxonomy_iid_entry.pack(side=RIGHT, expand=YES, fill=X)

		# Create Annotation Name Row
		row = Frame(self.taxonomy_pane_two)
		self.taxonomy_annotation_label = Label(row, text="Annotation", anchor='w', width=10)
		self.taxonomy_annotation_entry = Entry(row)
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		self.taxonomy_annotation_label.pack(side=LEFT)
		self.taxonomy_annotation_entry.pack(side=RIGHT, expand=YES, fill=X)

		# Create Annotation Type Row
		row = Frame(self.taxonomy_pane_two)
		self.taxonomy_type_label = Label(row, text="Type", anchor='w', width=10)
		self.taxonomy_type_entry = Entry(row)
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		self.taxonomy_type_label.pack(side=LEFT)
		self.taxonomy_type_entry.pack(side=RIGHT, expand=YES, fill=X)

		# Create Annotation Definition Row
		row = Frame(self.taxonomy_pane_two)
		self.taxonomy_detail_label = Label(row, text="Definition", anchor='w', width=10)
		self.taxonomy_detail_entry = Entry(row)
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		self.taxonomy_detail_label.pack(side=LEFT)
		self.taxonomy_detail_entry.pack(side=RIGHT, expand=YES, fill=X)
		
		# Create Add/Save/Delete Button Set
		row = Frame(self.taxonomy_pane_two)
		self.add_button = Button(row, text='Add Child Taxon', command=(lambda: self.iid_iterator(self.taxonomy,self.taxonomy_iid_entry.get(),self.child_adder)))
		self.add_button.pack(side=LEFT)
		self.save_button = Button(row, text='Save', command=self.taxonomy_saver)
		self.save_button.pack(side=LEFT)
		self.delete_button = Button(row, text='Delete', command=(lambda: self.iid_iterator(self.taxonomy,self.taxonomy_iid_entry.get(),self.element_deleter)))
		self.delete_button.pack(side=LEFT)
		row.pack()

	def taxonomy_viewer(self):
		# Displays the Taxonomy
	
		##################
		# Window Cleanup #
		##################
		
		# Delete Any Existing Information
		try:
			self.taxonomy_window.destroy()
			#newRoot.destroy()
		except (NameError, AttributeError):
			pass
			
		###################
		# Taxonomy Window #
		###################

		# Setup Taxonomy Window
		self.taxonomy_window = Toplevel()
		self.taxonomy_window.title('Taxonomy Development')
		
		# Place Icon
		# "Writing" by IQON from the Noun Project
		if (sys.platform.startswith('win') or sys.platform.startswith('darwin')):
			self.taxonomy_window.iconbitmap(Path(self.assets_path) / 'icon.ico')
		else:
			logo = PhotoImage(file=Path(self.assets_path) / 'icon.gif')
			self.taxonomy_window.call('wm', 'iconphoto', self.taxonomy_window._w, logo)
			
		# Set to Full Screen
		try:
			self.taxonomy_window.state('zoomed')
		except (TclError):
			pass
			m = self.taxonomy_window.maxsize()
			self.taxonomy_window.geometry('{}x{}+0+0'.format(*m))

		# Determine Window Size / Screen Resolution 
		window_width = self.taxonomy_window.winfo_screenwidth()
		window_height = self.taxonomy_window.winfo_screenheight()

		# Setup Taxonomy Window Panels (45/65 Split)
		self.taxonomy_pane_one = Frame(self.taxonomy_window)
		self.taxonomy_pane_two = Frame(self.taxonomy_window)
		split = 0.45
		self.taxonomy_pane_one.place(y=5, relwidth=split, relheight=1)
		self.taxonomy_pane_two.place(relx=split, relwidth=1.0-split, relheight=1)

		# Setup Window Menu
		menubar = Menu(self.taxonomy_window)
		addMenu = Menu(menubar, tearoff=False)
		addItemMenu = Menu(addMenu, tearoff=False)
		self.taxonomy_window.config(menu=menubar)
		menubar.add_command(label="Add New Root", command=self.root_adder)

		############################################
		# Set Up Annotation Selection (Tree) Panel #
		############################################

		# Create Tree
		self.taxonomy_tree = ttk.Treeview(self.taxonomy_pane_one,height=int(window_height/21),selectmode='browse')

		# Create Tree Layout
		self.taxonomy_tree["columns"]=("one","two","three")
		self.taxonomy_tree.column("#0", minwidth=int(window_width/24*2.5), stretch=1)
		self.taxonomy_tree.column("one", minwidth=int(window_width/24),  stretch=1)
		self.taxonomy_tree.column("two", minwidth=int(window_width/4), stretch=1)
		self.taxonomy_tree.heading("#0",text="Annotation",anchor=W)
		self.taxonomy_tree.heading("one", text="Type",anchor=W)
		self.taxonomy_tree.heading("two", text="Detail",anchor=W)

		# Create Roots
		for segment,dictionary in self.taxonomy.items():
			top=self.taxonomy_tree.insert("", 1, dictionary['iid'], text=dictionary['name'], values=(dictionary['type'],dictionary['definition']),open = True)

			def iterateAllKeys(child_dictionary,parent_branch):
			# Recursive Function to Go Through an Unknown Number of Layers
			
				# Create Lambda Dictionary
				x, d = -1, {}

				# Go Through Every Key (Numerical Values) in Current "children" Dictionary
				for new_key,new_dictionary in child_dictionary.items():

					# Advance Branch Lambda Variable
					x = x + 1

					# Create New Branch
					d[x+1]=self.taxonomy_tree.insert(parent_branch, "end", new_dictionary['iid'], text=new_dictionary['name'],values=(new_dictionary['type'],new_dictionary['definition']),open = True)

					# Re-Run Recursive Function with New "children" Dictionary
					iterateAllKeys(new_dictionary['children'],d[x+1])

			# Begin Recursive Function
			iterateAllKeys(dictionary['children'],top)

		# Display Tree
		self.taxonomy_tree.pack()
		self.taxonomy_tree.bind('<Button-1>', self.tree_item_informer)

		##################################
		# Set Up Definition Editor Panel #
		##################################

		# Display Editor Panel
		self.display_editor()
