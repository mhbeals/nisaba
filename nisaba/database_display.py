try:
	# Used when executing with Python
	from database_maintenance import *
except ModuleNotFoundError:
	# Used when calling as library
	from nisaba.database_maintenance import *

# Import External Libraries
import csv
from pathlib import Path
import PIL.Image
import PIL.ImageTk
import os

# Import TKinter Libraries
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from ttkwidgets import CheckboxTreeview

class database_display(database_maintenance):

	def transcription_updater(self):

		# Get Coordinate Information
		start = int(self.start_text.get())
		end = int(self.end_text.get())

		# Pull Transcription from self.database
		self.transcription_words = self.database[self.collection_index]['items'][self.item_index]['transcription'].split()

		# Get Snippets
		pre_transcription = ' '.join(self.transcription_words[start-20:start]) + " "
		transcription = ' '.join(self.transcription_words[start:end]) + " "
		post_transcription = ' '.join(self.transcription_words[end:end+20])

		# Set Highlighting / Background Colours
		self.transcription_text.tag_config("faded", foreground="light gray", font=(14))
		self.transcription_text.tag_config("normal", font=(14))

		# Clear Existing Text
		self.transcription_text.insert(END,"...")
		self.transcription_text.delete("1.0",END)

		# Insert Snippet Text
		self.transcription_text.insert(END,pre_transcription,('faded'))
		self.transcription_text.insert(END,transcription,('normal'))
		self.transcription_text.insert(END,post_transcription, ('faded'))

		# Display Textbox
		self.transcription_text.grid(column = 0, row = 1, columnspan=8, sticky=NSEW, padx =10, pady = 10)
		
	def cropped_image_updater(self):

			# Set image file
			self.filename = str(Path(self.raw_data_images_path) / self.database[self.collection_index]['items'][self.item_index]['image_file'])

			# Load Image
			self.segment_image = PIL.Image.open(self.filename)

			# Find Image Size
			[self.segment_imageSizeWidth, self.segment_imageSizeHeight] = self.segment_image.size
			self.segment_image_original_ratio = self.segment_imageSizeHeight / self.segment_imageSizeWidth

			# Pull Updated Coordinates

			self.top = int(self.top_text.get())
			self.bottom = int(self.bottom_text.get())
			self.left = int(self.left_text.get())
			self.right = int(self.right_text.get())

			# Find Crop Coordinates
			self.segment_top_x_coordinate =  int(self.left*self.segment_imageSizeWidth / 100)
			self.segment_top_y_coordinate = int(self.top*self.segment_imageSizeHeight / 100)
			self.segment_bottom_x_coordinate = int(self.right*self.segment_imageSizeWidth / 100)
			self.segment_bottom_y_coordinate = int(self.bottom*self.segment_imageSizeHeight / 100)

			# Crop Image
			self.segment_image = self.segment_image.crop((self.segment_top_x_coordinate,
														  self.segment_top_y_coordinate,
														  self.segment_bottom_x_coordinate,
														  self.segment_bottom_y_coordinate))

			[self.cropped_image_width, self.cropped_image_height] = self.segment_image.size
			self.cropped_image_ratio_h = self.cropped_image_height / self.cropped_image_width
			self.cropped_image_ratio_w = self.cropped_image_width /self.cropped_image_height

			# Resize Image to Fit Canvas
			if self.cropped_image_width < self.cropped_image_height:
				self.segment_sizeRatio = 600 / self.cropped_image_height
				self.segment_newImageSizeHeight = int(self.cropped_image_height*self.segment_sizeRatio)
				self.segment_newImageSizeWidth = int(self.segment_newImageSizeHeight*self.cropped_image_ratio_w)

			else:
				self.segment_sizeRatio = 600 / self.cropped_image_width
				self.segment_newImageSizeWidth = int(self.cropped_image_width*self.segment_sizeRatio)
				self.segment_newImageSizeHeight = int(self.segment_newImageSizeWidth*self.cropped_image_ratio_h)

			self.segment_image = self.segment_image.resize((self.segment_newImageSizeWidth, self.segment_newImageSizeHeight), PIL.Image.ANTIALIAS)

			# Prepare Image for Insertion
			self.segment_photoImg = PIL.ImageTk.PhotoImage(self.segment_image)

			# Display Image Canvas
			self.segment_imageCanvas.config(width=self.segment_newImageSizeWidth+10, height = self.segment_newImageSizeHeight+10)
			self.segment_imageCanvas.grid(column=0,row=0, columnspan = 8, padx =10, pady = 10)

			# Add Image to Canvas
			self.segment_imageCanvas.create_image(self.segment_newImageSizeWidth/2+6,
												  self.segment_newImageSizeHeight/2+6,
												  image=self.segment_photoImg,
												  anchor="center")

	def csv_importer(self,datafile):

		questions = {}

		# Populate dictionary with imported file
		with open (Path(self.config_path) / datafile, 'r') as file:
			reader = csv.reader(file, delimiter='\t')
			for line in reader:
				questions[line[0]] = line[1]

		return questions;
		
	def bibliographical_field_importer(self,level):

		# Set Collection-Level Questions
		self.collection_questions = self.csv_importer('collection_bibliographic_annotation.tsv')

		# Set Item-Level Questions
		if level == 'i' or level == 's':
			self.item_questions  = self.csv_importer('item_bibliographic_annotation.tsv')

		# Set Segment-Level Questions
		if level == 's':
			self.segment_questions  = self.csv_importer('segment_bibliographic_annotation.tsv')

		return;

	def entry_form_maker(self,tab,questions,level):

		entries = []

		# Create Entry Form Elements
		for field,question in questions.items():

			# Create a row
			row = Frame(tab)

			# Create a label and text box
			label = Label(row, text=question, anchor='w')
			entry = Entry(row)

			# Package Row
			row.pack(side=TOP, fill=X, padx=5, pady=5)
			label.pack(side=LEFT)
			entry.pack(side=RIGHT, expand=YES, fill=X)

			# Fill entry with database values (if available)

			if level == 'c':
				entry_text = self.database[self.collection_index].get(field,'')

			if level == 'i' or level == 's':
				entry_text = self.database[self.collection_index]['items'][self.item_index].get(field,'')

			if level == 's':
				entry_text = self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index].get(field,'')

			entry.insert(0,entry_text)

			# Add field and value to save list
			entries.append((field, entry))

		return entries
		
	def bibliographic_form_maker(self, tab, level):

		self.bibliographical_field_importer(level)

		self.collection_entries = self.entry_form_maker(tab,self.collection_questions,'c')
		
		if level == 'i' or level == 's':
			self.item_entries = self.entry_form_maker(tab,self.item_questions,'i')

		if level == 's':
			self.segment_entries = self.entry_form_maker(tab,self.segment_questions,'s')

	def annotation_tree_maker(self,tree_name,level):

		# Create Tree Structure

		tree_name["columns"]=("one","two","three")
		tree_name.column("#0")
		tree_name.column("one")
		tree_name.column("two")
		tree_name.heading("#0",text="Annotation",anchor=W)
		tree_name.heading("one", text="Type",anchor=W)
		tree_name.heading("two", text="Detail",anchor=W)

		# Create Root
		for item,dictionary in self.taxonomy.items():

			top=tree_name.insert("", 1, dictionary['iid'], text=dictionary['name'], values=(dictionary['type'],dictionary['definition']),open = True)

			# Recursive Function to Go Through Unknown Number of Layers
			def iterateAllKeys(child_dictionary,parent_branch):

				# Create Lambda Dictionary
				x, d = -1, {}

				# Go through every key (numerical values) in current "children" dictionary
				for new_key,new_dictionary in child_dictionary.items():

					# Advance Branch Lambda Variable
					x = x + 1

					# Create New Branch
					d[x+1]=tree_name.insert(parent_branch, "end", new_dictionary['iid'], text=new_dictionary['name'],values=(new_dictionary[	'type'],new_dictionary['definition']))

					# Re-Run Recursive Function with New "children" Dictionary
					iterateAllKeys(new_dictionary['children'],d[x+1])

			# Begin Recursive Function
			iterateAllKeys(dictionary['children'],top)

		# Highlight Those Already Saved
		if level == 'i':

			if 'annotations' in self.database[self.collection_index]['items'][self.item_index]:
				for annotation in self.database[self.collection_index]['items'][self.item_index]['annotations']:
					tree_name.change_state(tree_name.parent(annotation),"checked")
					tree_name.change_state(annotation,"checked")

		elif level == 's':

			if 'annotations' in self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]:
				for annotation in self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['annotations']:
					tree_name.change_state(tree_name.parent(annotation),"checked")
					tree_name.change_state(annotation,"checked")

		# Display Tree
		tree_name.pack(anchor=NW)

	def collection_adder(self):

		i = -1
		loop = TRUE

		while loop == TRUE:
			i = i + 1
			loop = str(i) in self.database

		self.database[str(i)]= {'dc:title': 'New Collection','items' : {}}

		self.database_window_displayer()
		
	def item_adder(self,type):

		i = -1
		loop = TRUE

		while loop == TRUE:
			i = i + 1
			loop = str(i) in self.database[self.collection_index]['items']

		if type == 'i':
			self.database[self.collection_index]['items'][str(i)]= {'item_type': 'i','image_file': 'sample.jpg', 'segments' : {}}

		elif type == 't':
			self.database[self.collection_index]['items'][str(i)]= {'item_type': 't', 'transcription': '', 'segments' : {}}

		self.collection_item_list_panel_displayer()

	def segment_adder(self):

		i = -1
		loop = TRUE

		while loop == TRUE:
			i = i + 1
			loop = str(i) in self.database[self.collection_index]['items'][self.item_index]['segments']


		if  self.database[self.collection_index]['items'][self.item_index]['item_type'] == 't':
			self.database[self.collection_index]['items'][self.item_index]['segments'][str(i)] = {'start':0,'end':len(self.database[self.collection_index]['items'][self.item_index]['transcription'].split())}

		elif self.database[self.collection_index]['items'][self.item_index]['item_type'] == 'i':
			self.database[self.collection_index]['items'][self.item_index]['segments'][str(i)] = {'top':0,'right':50,'bottom':50,'left':0}

		self.item_panel_displayer('s')

	def segment_panels_displayer(self):

		##########################
		# Set Up Segment Display #
		##########################

		# Delete Previous Panels and Menus
		try:
			self.pane_one.destroy()
			self.pane_two.destroy()
			self.pane_three.destroy()
		except (NameError, AttributeError):
			pass			
			
		# Retitle Window
		self.database_window.title("Segment: " + self.segment_value)

		# Setup Segment Window Panels
		self.segment_pane_one = Frame(self.database_window)
		self.segment_pane_two = Frame(self.database_window)
		split = 0.5
		self.segment_pane_one.place(rely=0, relwidth=split, relheight=1)
		self.segment_pane_two.place(relx=split, relwidth=1.0-split, relheight=1)

		# If the Segment is Text
		if self.database[self.collection_index]['items'][self.item_index]['item_type'] == 't':

			# Pull segmentation data
			start = self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['start']
			end = self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['end']

			# Create text boxes
			start_label = Label(self.segment_pane_two, text="Starting Word")
			self.start_text = Entry(self.segment_pane_two)
			end_label = Label(self.segment_pane_two, text="Ending Word")
			self.end_text = Entry(self.segment_pane_two)

			# Fill Entry Boxes
			self.start_text.insert(4,start)
			self.end_text.insert(4,end)

			# Pack Labels and Entry Boxes into Frame
			start_label.grid(column = 1, row = 0, sticky=NW, padx =10, pady = 10)
			self.start_text.grid(column = 2, row = 0, sticky=NW, padx =10, pady = 10)
			end_label.grid(column = 4, row = 0, sticky=NW, padx =10, pady = 10)
			self.end_text.grid(column = 5, row = 0, sticky=NW, padx =10, pady = 10)

			# Create Text Box
			self.transcription_text = Text(self.segment_pane_two, wrap=WORD)

			# Create and Pack Update Button
			update_button = Button(self.segment_pane_two, text='Refresh', command=self.transcription_updater)
			update_button.grid(column = 6, row = 0, sticky=W, padx =10, pady = 10)

			# Populate Text Box
			self.transcription_updater()

		# If the Segment is an Image
		elif self.database[self.collection_index]['items'][self.item_index]['item_type'] == 'i':

			# Pull segmentation data
			top = int(self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['top'])
			left = int(self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['left'])
			bottom = int(self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['bottom'])
			right = int(self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['right'])

			# Create text boxes
			self.top_label = Label(self.segment_pane_two, text="% from Top")
			self.top_text = Entry(self.segment_pane_two)
			self.bottom_label = Label(self.segment_pane_two, text="% to the Bottom")
			self.bottom_text = Entry(self.segment_pane_two)
			self.left_label = Label(self.segment_pane_two, text="% from Left")
			self.left_text = Entry(self.segment_pane_two)
			self.right_label = Label(self.segment_pane_two, text="% to the Right")
			self.right_text = Entry(self.segment_pane_two)

			# Create Image Canvas
			self.segment_imageCanvas = Canvas(self.segment_pane_two)

			# Fill Entry Boxes
			self.top_text.insert(4,top)
			self.bottom_text.insert(4,bottom)
			self.left_text.insert(4,left)
			self.right_text.insert(4,right)

			# Pack Labels and Entry Boxes into Frame
			self.top_label.grid(column = 0, row = 1, sticky=NW)
			self.top_text.grid(column = 1, row = 1, sticky=NW)
			self.bottom_label.grid(column = 0, row = 2,sticky=NW)
			self.bottom_text.grid(column = 1, row = 2, sticky=NW)
			self.left_label.grid(column = 2, row = 1, sticky=NW)
			self.left_text.grid(column = 3, row = 1, sticky=NW)
			self.right_label.grid(column = 2, row = 2, sticky=NW)
			self.right_text.grid(column = 3, row = 2, sticky=NW)

			self.cropped_image_updater()

			# Create and Pack Update Button
			update_button = Button(self.segment_pane_two, text='Refresh', command=self.cropped_image_updater)
			update_button.grid(column = 4, row = 1, sticky=W, padx =5, pady = 5)

		# Setup Segment Window Tabs (Left / Pane 1)

		# Set Up Tabs
		self.segment_tab_control = ttk.Notebook(self.segment_pane_one)
		self.segment_tab1 = ttk.Frame(self.segment_tab_control)
		self.segment_tab2 = ttk.Frame(self.segment_tab_control)

		# Pack Tabs into Frame
		self.segment_tab_control.add(self.segment_tab1, text='Bibliographic Information')
		self.segment_tab_control.add(self.segment_tab2, text='Annotations')
		self.segment_tab_control.pack(expand=1, fill='both')

		# Create "save", "reset" and "return" buttons
		buttonFrame = ttk.Frame(self.segment_pane_one)
		b1 = Button(self.segment_pane_one, text='Save Values', command=(lambda: self.database_entry_saver('s')))
		b2 = Button(self.segment_pane_one, text='Reset to Last Saved Values', command=self.segment_panels_displayer)
		b3 = Button(self.segment_pane_one, text='Return to Item View', command=(lambda: self.item_panel_displayer('m')))
		buttonFrame.pack(anchor=NW)
		b1.pack(side=LEFT, padx=5, pady=5)
		b2.pack(side=LEFT, padx=5, pady=5)
		b3.pack(side=LEFT, padx=5, pady=5)

		########################################
		# Set up bibliographic information tab #
		########################################

		# Display bibliographic form and create entries database
		self.bibliographic_form_maker(self.segment_tab1, 's')

		#################################
		# Set up annotations tab (tab2) #
		#################################

		self.segment_tree=CheckboxTreeview(self.segment_tab2,height="26")
		self.annotation_tree_maker(self.segment_tree,'s')
		
	def item_panel_displayer(self,focus):
	
		# Delete Previous Panels and Menus
		try:
<<<<<<< HEAD
			self.pane_one.destroy()
			self.pane_two.destroy()
			self.pane_three.destroy()
		except (NameError, AttributeError):
			pass			
		
		# Set up Item Display
		self.database_window.title("Item: " + self.item_value)
			
=======
			self.item_info.state('zoomed')
		except (TclError):
			pass
			m = self.item_info.maxsize()
			self.item_info.geometry('{}x{}+0+0'.format(*m))


		# Place Icon
		# "Writing" by IQON from the Noun Project
		if (sys.platform.startswith('win') or sys.platform.startswith('darwin')):
			self.item_info.iconbitmap(Path(self.assets_path) / 'icon.ico')
		else:
			logo = PhotoImage(file=Path(self.assets_path) / 'icon.gif')
			self.item_info.call('wm', 'iconphoto', self.item_info._w, logo)

>>>>>>> a4792820267d2e682b503e63599a6536473153d5
		# Set Up Item Information Window Menu
		menubar = Menu(self.database_window)
		self.database_window.config(menu=menubar)
		fileMenu = Menu(menubar, tearoff=False)
		menubar.add_command(label="Add New Segment", command=self.segment_adder)

		# Setup Item Window Panes
		self.pane_one = Frame(self.database_window)
		self.pane_two = Frame(self.database_window)
		split = 0.5
		self.pane_one.place(rely=0, relwidth=split, relheight=1)
		self.pane_two.place(relx=split, relwidth=1.0-split, relheight=1)

		####################################
		# Setup Item Display Panel (Right) #
		####################################

		# If the Item is Text
		if self.database[self.collection_index]['items'][self.item_index]['item_type'] == 't':

			# Pull Transcription from Database
			if 'transcription' in self.database[self.collection_index]['items'][self.item_index]:
				transcription = self.database[self.collection_index]['items'][self.item_index]['transcription']
			else:
				transcription = ""

			# Create wrapping text box
			self.transcription_text = Text(self.pane_two, wrap=WORD)

			# Insert transcription in text box
			self.transcription_text.insert("1.0",transcription)
			self.transcription_text.configure(font=(14))

			# Display text box
			self.transcription_text.pack(padx=10,pady=10)

		# If the Item is an Image
		elif self.database[self.collection_index]['items'][self.item_index]['item_type'] == 'i':

			# Create text boxes
			self.image_label = Label(self.pane_two, text="Image File")
			self.image_filename = Entry(self.pane_two)

			# Fill Entry Boxes
			self.image_filename.insert(4,self.database[self.collection_index]['items'][self.item_index]['image_file'])

			# Display Image Filename
			self.image_label.grid(column = 1, row = 0)
			self.image_filename.grid(column = 2, row = 0)

			# Set image file
			filename = str(Path(self.raw_data_images_path) / self.database[self.collection_index]['items'][self.item_index]['image_file'])

			# Load Image
			image = PIL.Image.open(filename)

			# Find Image Size
			[imageSizeWidth, imageSizeHeight] = image.size

			# Resize Image to Fit Canvas
			sizeRatio = 600 / imageSizeWidth
			newImageSizeWidth = int(imageSizeWidth*sizeRatio)
			newImageSizeHeight = int(imageSizeHeight*sizeRatio)
			image = image.resize((newImageSizeWidth, newImageSizeHeight), PIL.Image.ANTIALIAS)

			# Prepare Image for Insertion
			self.photoImg = PIL.ImageTk.PhotoImage(image)

			# Display Image Canvas
			imageCanvas = Canvas(self.pane_two, width=newImageSizeWidth+10, height=newImageSizeHeight+10, bg="black")
			imageCanvas.grid(column = 0, row = 1, columnspan=5)

			# Add Image to Canvas
			imageCanvas.create_image(newImageSizeWidth/2+6, newImageSizeHeight/2+6, anchor="center", image=self.photoImg)

		####################################
		# Setup Item Metadata Panel (Left) #
		####################################

		# Set Up Tabs
		self.item_tab_control = ttk.Notebook(self.pane_one)
		self.item_tab1 = ttk.Frame(self.item_tab_control)
		self.item_tab2 = ttk.Frame(self.item_tab_control)
		self.item_tab3 = ttk.Frame(self.item_tab_control)

		# Pack Tabs into Frame
		self.item_tab_control.add(self.item_tab1, text='Bibliographic Information')
		self.item_tab_control.add(self.item_tab2, text='Annotations')
		self.item_tab_control.add(self.item_tab3, text='Segments')
		self.item_tab_control.pack(expand=1, fill=BOTH)

		# Set Focus
		if focus == 'm':
			self.item_tab_control.select(self.item_tab1)
		if focus == 'a':
			self.item_tab_control.select(self.item_tab2)
		if focus == 's':
			self.item_tab_control.select(self.item_tab3)
		
		# Create "save", "reset" and "return" buttons for all tabs
		self.buttonFrame = ttk.Frame(self.pane_one)
		self.b1 = Button(self.buttonFrame, text='Save Values', command=(lambda: self.database_entry_saver('i')))
		self.b2 = Button(self.buttonFrame, text='Reset to Last Saved Values', command=(lambda: self.segment_list_refresher('a')))
		self.b3 = Button(self.buttonFrame, text='Return to Collections List', command=self.database_window_displayer)
		self.b1.pack(side=LEFT, padx=5, pady=5)
		self.b2.pack(side=LEFT, padx=5, pady=5)
		self.b3.pack(side=LEFT, padx=5, pady=5)
		self.buttonFrame.pack(anchor=NW)

		########################################
		# Set up bibliographic information tab #
		########################################

		# Display bibliographic form and create entries database
		self.bibliographic_form_maker(self.item_tab1, 'i')

		##########################
		# Set up annotations tab #
		##########################

		self.item_tree = CheckboxTreeview(self.item_tab2,height="26",)
		self.annotation_tree_maker(self.item_tree,'i')

		#######################
		# Set Up Segments Tab #
		#######################

		# Set up segment list scrollbar
		self.scrollbar = Scrollbar(self.item_tab3)
		self.scrollbar.pack(side=RIGHT,fill=Y)

		# Set Up segment listbox
		self.segments = Listbox(self.item_tab3)
		self.segments.pack(anchor=W, fill=BOTH, expand=True)

		#Populate Segment List Box
		for segment_number,dictionary in self.database[self.collection_index]['items'][self.item_index]['segments'].items():

			# If the segment is text
			if self.database[self.collection_index]['items'][self.item_index]['item_type'] == "t":

				# Obtain Snippet Transcription and Package for Display
				transcription_words = self.database[self.collection_index]['items'][self.item_index]['transcription'].split()
				display_item = ' '.join(transcription_words[dictionary['start']:dictionary['start']+10])

			# If the segment is an image
			elif self.database[self.collection_index]['items'][self.item_index]['item_type'] == "i":

				display_item = 'Image Snippet'
				# ACTION: Add coordinates to display_item text

			# Display the number and title
			segment_number_str = str(int(segment_number)+1)
			segment = segment_number_str + ". " + display_item
			self.segments.insert(END, segment)

			# Bind scrollbar to listbox
			self.segments.config(yscrollcommand=self.scrollbar.set)
			self.scrollbar.config(command=self.segments.yview)

			# Bind seleection to event
			self.segments.bind('<Double-Button>', self.segment_informer)
	
	def collection_metadata_panel_displayer(self):

		##########################################
		# Set up Bibliographic Information Panel #
		##########################################

		# Delete Any Existing Information
		try:
			self.pane_two.destroy()
		except (NameError, AttributeError):
			pass

		self.pane_two = Frame(self.database_window)
		self.pane_two.place(relx=.3, relwidth=.4, relheight=1)
		
		# Display bibliographic form and create entries database
		self.bibliographic_form_maker(self.pane_two, 'c')

		# Create "save" button
		b1 = Button(self.pane_two, text='Save Values', command=(lambda: self.database_entry_saver('c')))
		b1.pack(anchor=NW, padx=5, pady=5)

	def collection_item_list_panel_displayer(self):
		##############################
		# Set up List of Items Panel #
		##############################

		# Delete Any Existing Information
		try:
			self.pane_three.destroy()
		except (NameError, AttributeError):
			pass

		self.pane_three = Frame(self.database_window)
		self.pane_three.place(relx=.7, relwidth=.3, relheight=1)

		# Setup scroll bar
		scrollbar = Scrollbar(self.pane_three)
		scrollbar.pack(side=RIGHT,fill=Y)

		# Setup listbox
		items = Listbox(self.pane_three)
		items.pack(anchor=W, fill="both", expand=True)

		# Populate listbox
		for item_number,dictionary in self.database[self.collection_index]['items'].items():

			# If the item has a title
			if 'item_title' in self.database[self.collection_index]['items'][item_number]:
				if 'dc:title' in self.database[self.collection_index]:
					display_item = "{0}, part of the {1} Collection".format(str(dictionary['item_title']),str(self.database[self.collection_index]['dc:title']))
				else:
					display_item = "{0}, part of an unknown Collection".format(str(self.database[self.collection_index]['dc:title']))

			# If the item has no title
			elif 'dc:title' in self.database[self.collection_index]:
				display_item = "An Unknown Part of the {0} Collection".format(str(self.database[self.collection_index]['dc:title']))

			else:
				display_item = "No title listed"

			# Display the item title and author
			item_number_str = str(int(item_number)+1)
			item = item_number_str  + ". " + display_item
			items.insert(END, item)

		# Bind scrollbar to listbox
		items.config(yscrollcommand=scrollbar.set)
		scrollbar.config(command=items.yview)

		# Bind selected item to event
		items.bind('<Double-Button>', self.item_informer)

		# Create "save" button for all tabs
		self.buttonFrame = ttk.Frame(self.pane_three)
		self.b1 = Button(self.buttonFrame, text='Add New Text', command=(lambda t="t": self.item_adder(t)))
		self.b2 = Button(self.buttonFrame, text='Add New Image', command=(lambda t="i": self.item_adder(t)))
		self.b1.pack(side=LEFT, padx=5, pady=5)
		self.b2.pack(side=LEFT, padx=5, pady=5)
		self.buttonFrame.pack(anchor=NW)

	def segment_informer(self, evt):

		# Capture Event Information
		segment_event_data = evt.widget
		self.segment_index = str(segment_event_data.curselection()[0])
		self.segment_value = segment_event_data.get( int(self.item_index))

		self.segment_panels_displayer()
		
	def item_informer(self, evt):

	   # Capture Event Information
		item_event_data = evt.widget
		self.item_index = str(item_event_data.curselection()[0])
		self.item_value = item_event_data.get(int(self.item_index))

		self.item_panel_displayer('m')
		
	def collection_informer(self, evt):

		# Capture Event Information
		collection_event_data = evt.widget
		self.collection_index = str(collection_event_data.curselection()[0])

		# Display Collection Information Panels
		self.collection_metadata_panel_displayer()
		self.collection_item_list_panel_displayer()
		
	def database_window_displayer(self):
		# Display top-level window
		
		# Reload Taxonomy
		with open (Path(self.database_path) / "taxonomy.json", 'r') as file:
			loaddata = file.read()
		self.taxonomy = json.loads(loaddata)
		
		##################
		# Window Cleanup #
		##################
		
		# Delete Previous Panels and Menus or Create New Window
		try:
			self.pane_one.destroy()
			self.pane_two.destroy()
			self.pane_three.destroy()
		except (NameError, AttributeError):
			self.database_window = Toplevel()
			
		#####################
		# Collection Window #
		#####################
		
		# Setup Collections Window
<<<<<<< HEAD
		
		self.database_window.title('Collections')
		
		# Set to Full Screen
=======
		self.collection_selection_window = Toplevel()
		self.collection_selection_window.title('Collection Selection')

		# Delete Any Existing Item Windows
>>>>>>> a4792820267d2e682b503e63599a6536473153d5
		try:
			self.database_window.state('zoomed')
		except (TclError):
			m = self.database_window.maxsize()
			self.database_window.geometry('{}x{}+0+0'.format(*m))

		# Place Icon
		# "Writing" by IQON from the Noun Project
		if (sys.platform.startswith('win') or sys.platform.startswith('darwin')):
<<<<<<< HEAD
			self.database_window.iconbitmap(Path(self.assets_path) / 'icon.ico')
		else:
			logo = PhotoImage(file=Path(self.assets_path) / 'icon.gif')
			self.database_window.call('wm', 'iconphoto', self.database_window._w, logo)
=======
			self.collection_selection_window.iconbitmap(Path(self.assets_path) / 'icon.ico')
		else:
			logo = PhotoImage(file=Path(self.assets_path) / 'icon.gif')
			self.collection_selection_window.call('wm', 'iconphoto', self.collection_selection_window._w, logo)
>>>>>>> a4792820267d2e682b503e63599a6536473153d5

		# Setup Window Menu
		menubar = Menu(self.database_window)
		addMenu = Menu(menubar, tearoff=False)
		addItemMenu = Menu(addMenu, tearoff=False)
		self.database_window.config(menu=menubar)
		menubar.add_command(label="Load New Database", command=self.database_loader)
		menubar.add_cascade(label="Add", menu=addMenu)
		addMenu.add_command(label="Collection", command=self.collection_adder)

		# Setup Window Panes
		self.pane_one = Frame(self.database_window)
		self.pane_two = Frame(self.database_window)
		self.pane_three = Frame(self.database_window)
		split = 0.33
		self.pane_one.place(rely=0, relwidth=.3, relheight=1)
		self.pane_two.place(relx=.3, relwidth=.4, relheight=1)
		self.pane_three.place(relx=.7, relwidth=.3, relheight=1)

		##############################
		# Collection Selection Panel #
		##############################

		# Setup scroll bar
		scrollbar = Scrollbar(self.pane_one)
		scrollbar.pack(side=RIGHT,fill=Y, expand=True)

		# Setup listbox
		items = Listbox(self.pane_one)
		items.config(width=1000)
		items.pack(anchor=W, fill=BOTH, expand=True)

		# Populate listbox
		for collection_number,dictionary in self.database.items():

			if collection_number != 'users':

				# If the item has a title
				if 'dc:title' in self.database[collection_number]:
					display_item = str(dictionary['dc:title'])

				else:
					display_item = "No title listed"

				# Display the item title and author
				collection_number_str = str(int(collection_number)+1)
				item = collection_number_str + ". " + display_item
				items.insert(END, item)

		# Bind scrollbar to listbox
		items.config(yscrollcommand=scrollbar.set)
		scrollbar.config(command=items.yview)

		# Bind selected item to event
		items.bind('<Double-Button>', self.collection_informer)
