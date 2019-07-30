from  database_maintenance import *

# Import TKinter Libraries
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *

class taxonomy_display(database_maintenance):
	
	def	delete_element_recursive(self,dictionary):
		# Delete item	
		for key,value in dictionary.items():
			if value['iid'] == self.taxonomy_iid_entry.get():
				del dictionary[key]
				break
				
			else:
				self.delete_element_recursive(value['children'])
					
	def	delete_element(self):
		# Delete item	
		for key,value in self.taxonomy.items():
			if value['iid'] == self.taxonomy_iid_entry.get():
				del dictionary[key]
				break
				
			else:
				self.delete_element_recursive(value['children'])

		self.taxonomy_window.destroy()
		self.taxonomy_viewer()
		
	def displayEditor(self):

		# Delete Any Existing Information
		try:
			self.taxonomy_pane_two.destroy()
		except (NameError, AttributeError):
			pass
			
		# Setup Taxonomy Window Panels
		split = 0.45
		self.taxonomy_pane_two = Frame(self.taxonomy_window)
		self.taxonomy_pane_two.place(relx=split, relwidth=1.0-split, relheight=1)
		
		row = Frame(self.taxonomy_pane_two)
		self.taxonomy_iid_label = Label(row, text="ID", anchor='w', width=10)
		self.taxonomy_iid_entry = Entry(row)
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		self.taxonomy_iid_label.pack(side=LEFT)
		self.taxonomy_iid_entry.pack(side=RIGHT, expand=YES, fill=X)
		
		row = Frame(self.taxonomy_pane_two)
		self.taxonomy_annotation_label = Label(row, text="Annotation", anchor='w', width=10)
		self.taxonomy_annotation_entry = Entry(row)
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		self.taxonomy_annotation_label.pack(side=LEFT)
		self.taxonomy_annotation_entry.pack(side=RIGHT, expand=YES, fill=X)
		
		row = Frame(self.taxonomy_pane_two)
		self.taxonomy_type_label = Label(row, text="Type", anchor='w', width=10)
		self.taxonomy_type_entry = Entry(row)
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		self.taxonomy_type_label.pack(side=LEFT)
		self.taxonomy_type_entry.pack(side=RIGHT, expand=YES, fill=X)
		
		row = Frame(self.taxonomy_pane_two)
		self.taxonomy_detail_label = Label(row, text="Definition", anchor='w', width=10)
		self.taxonomy_detail_entry = Entry(row)
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		self.taxonomy_detail_label.pack(side=LEFT)
		self.taxonomy_detail_entry.pack(side=RIGHT, expand=YES, fill=X)
		
		row = Frame(self.taxonomy_pane_two)		
		row.pack()
		self.save_button = Button(row, text='Save', command=self.save_taxonomy)
		self.save_button.pack(side=LEFT)
		self.delete_button = Button(row, text='Delete', command=self.delete_element)
		self.delete_button.pack(side=LEFT)

	def iidChecker(self,dictionary):

		for key,value in dictionary.items():
			if value['iid'] == self.clicked_item:
				self.taxonomy_iid_entry.insert(0,value['iid'])
				self.taxonomy_annotation_entry.insert(0,value['name'])
				self.taxonomy_type_entry.insert(0,value['type'])
				self.taxonomy_detail_entry.insert(0,value['definition'])
			else:
				self.iidChecker(value['children'])

	def treeItemSelector(self,event):

		self.clicked_item = self.taxonomy_tree.identify('item',event.x,event.y)

		self.displayEditor()
			
		for key,value in self.taxonomy.items():
			if value['iid'] == self.clicked_item:
				self.taxonomy_iid_entry.insert(0,value['iid'])
				self.taxonomy_annotation_entry.insert(0,value['name'])
				self.taxonomy_type_entry.insert(0,value['type'])
				self.taxonomy_detail_entry.insert(0,value['definition'])
			else:
				self.iidChecker(value['children'])

	def taxonomy_viewer(self):

		###################
		# Taxonomy Window #
		###################

		# Setup Taxonomy Window
		self.taxonomy_window = Toplevel()
		self.taxonomy_window.title('Taxonomy Development')
		self.taxonomy_window.state('zoomed') 
		window_width = self.taxonomy_window.winfo_screenwidth()
		window_height = self.taxonomy_window.winfo_screenheight()
		
		# Setup Taxonomy Window Panels
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
		#menubar.add_command(label="Load New Taxonomy", command=pass)
		#menubar.add_command(label="Refresh", command=pass)

		#####################################
		# Set Up Definition Selection Panel #
		#####################################
			
		# Create Tree Structure
		self.taxonomy_tree = ttk.Treeview(self.taxonomy_pane_one,height=int(window_height/21),selectmode='browse')

		self.taxonomy_tree["columns"]=("one","two","three")
		self.taxonomy_tree.column("#0", minwidth=int(window_width/24*2.5), stretch=1)
		self.taxonomy_tree.column("one", minwidth=int(window_width/24),  stretch=1)
		self.taxonomy_tree.column("two", minwidth=int(window_width/4), stretch=1)
		self.taxonomy_tree.heading("#0",text="Annotation",anchor=W)
		self.taxonomy_tree.heading("one", text="Type",anchor=W)
		self.taxonomy_tree.heading("two", text="Detail",anchor=W)

		# Create Root
		for item,dictionary in self.taxonomy.items():
			
			top=self.taxonomy_tree.insert("", 1, str(item), text=dictionary['name'], values=(dictionary['type'],dictionary['definition']),open = True)

			# Recursive Function to Go Through Unknown Number of Layers
			def iterateAllKeys(child_dictionary,parent_branch):
			
				# Create Lambda Dictionary
				x, d = -1, {}

				# Go through every key (numerical values) in current "children" dictionary
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
		self.taxonomy_tree.bind('<Button-1>', self.treeItemSelector)

		#####################################
		# Set Up Definition Editor Panel #
		#####################################

		self.displayEditor()

