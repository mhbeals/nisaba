try: 
	# Used when executing with Python
	from database_maintenance import *
	from cache_maintenance import *
	from tooltip_creation import *
except ModuleNotFoundError:
	# Used when calling as library
	from nisaba.database_maintenance import *
	from nisaba.cache_maintenance import *
	from nisaba.tooltip_creation import *

# Import External Libraries
from pathlib import Path
import PIL.Image
import PIL.ImageTk
import os
import yaml

# Import TKinter Libraries
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from ttkwidgets import CheckboxTreeview

class database_display(cache_maintenance):

	#########################
	#   Event Processing    #
	#########################	
		
	def segment_informer(self, evt):
	# Collects Widget Event Data and Sets to Static Variable
	
		# Capture Event Information
		segment_event_data = evt.widget
		self.segment_index = str(segment_event_data.curselection()[0])
		self.segment_value = segment_event_data.get( int(self.item_index))

		# Open Segment Panels
		self.segment_panels_displayer()
		
	def item_informer(self, evt):
	# Collects Widget Event Data and Sets to Static Variable
	
		# Capture Event Information
		item_event_data = evt.widget
		self.item_index = str(item_event_data.curselection()[0])
		self.item_value = item_event_data.get(int(self.item_index))

		# Open Item Panels on Metadata Tab
		self.item_panels_displayer('m')
		
	def collection_informer(self, evt):
	# Collects Widget Event Data and Sets to Static Variable
	
		# Allows Reloading of Collections Screen Without Losing Original Index Number
		try:
			self.collection_event_data = evt.widget
			self.collection_index = str(self.collection_event_data.curselection()[0])
		except(AttributeError):	
			pass

		# Display Collection Panels
		self.collection_metadata_panel_displayer()
		self.collection_item_list_panel_displayer()
	
	#######################
	#   Content Display   #
	#######################	

	def transcription_updater(self,start,end):
	# Parses transcription data into greyed out (not selected) and black (selected) segments
	
		self.start_text.delete(0,END)
		self.end_text.delete(0,END)
		self.start_text.insert(0,start)
		self.end_text.insert(0,end)
	
		# Pull Transcription from self.database
		self.transcription_words = self.database[self.collection_index]['items'][self.item_index]['transcription'][0].split()
		
		# Get Snippets
		pre_start = start-20 if start > 20 else 0
		
		pre_transcription = ' '.join(self.transcription_words[pre_start:start]) + " "
		transcription = ' '.join(self.transcription_words[start:end]) + " "
		post_transcription = ' '.join(self.transcription_words[end:end+20])

		# Set Highlighting / Background Colours
		self.transcription_text.tag_config("faded", foreground="light gray", font=(10))
		self.transcription_text.tag_config("normal", font=(10))

		# Clear Existing Text
		self.transcription_text.insert(END,"...")
		self.transcription_text.delete("0.0",END)

		# Insert Snippet Text
		self.transcription_text.insert("0.0",pre_transcription[1:],('faded'))
		self.transcription_text.insert(END,transcription,('normal'))
		self.transcription_text.insert(END,post_transcription, ('faded'))

		# Display Textbox
		self.transcription_text.place(rely=.1, relwidth=1)
		
	def image_resetter(self):
	# Resets cropped image to 100%	
	
		self.top_text.delete(0,END)
		self.bottom_text.delete(0,END)
		self.left_text.delete(0,END)
		self.right_text.delete(0,END)
		self.top_text.insert(0,0)
		self.bottom_text.insert(0,100)
		self.left_text.insert(0,0)
		self.right_text.insert(0,100)
		self.cropped_image_updater()
	
	def cropped_image_updater(self):
	# Crops image to user-defined percentages
	
			try:
				# Set image file
				self.filename = str(Path(self.raw_data_images_path) / self.database[self.collection_index]['items'][self.item_index]['image_file'])
				self.segment_image = PIL.Image.open(self.filename)
				
			except(FileNotFoundError):
				# Use stand in if file is not found
				self.filename = str(Path(self.raw_data_images_path) / 'sample.jpg')
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

			# Compute Ratios
			[self.cropped_image_width, self.cropped_image_height] = self.segment_image.size
			self.cropped_image_ratio_h = self.cropped_image_height / self.cropped_image_width
			self.cropped_image_ratio_w = self.cropped_image_width /self.cropped_image_height
			
			# Implement Ratios for Portrait Images 
			if self.cropped_image_width < self.cropped_image_height:
				self.segment_sizeRatio = 600 / self.cropped_image_height
				self.segment_newImageSizeHeight = int(self.cropped_image_height*self.segment_sizeRatio)
				self.segment_newImageSizeWidth = int(self.segment_newImageSizeHeight*self.cropped_image_ratio_w)
			
			# Implement Ratios for Landscape Images
			else:
				self.segment_sizeRatio = 600 / self.cropped_image_width
				self.segment_newImageSizeWidth = int(self.cropped_image_width*self.segment_sizeRatio)
				self.segment_newImageSizeHeight = int(self.segment_newImageSizeWidth*self.cropped_image_ratio_h)

			# Resize Image to Fit Canvas
			self.segment_image = self.segment_image.resize((self.segment_newImageSizeWidth, self.segment_newImageSizeHeight), PIL.Image.ANTIALIAS)

			# Prepare Image for Insertion
			self.segment_photoImg = PIL.ImageTk.PhotoImage(self.segment_image)

			# Display Image Canvas
			self.segment_imageCanvas.config(width=self.segment_newImageSizeWidth+10, height = self.segment_newImageSizeHeight+10)
			self.segment_imageCanvas.place(relwidth=1,relheight=.5)

			# Add Image to Canvas
			self.segment_imageCanvas.create_image(self.segment_newImageSizeWidth/2+6,
												  self.segment_newImageSizeHeight/2+6,
												  image=self.segment_photoImg,
												  anchor="center")
			
			# Functions for cropping via mouse cursor 									  
			def onmouse(event):
			# When mouse clicks, start a yellow rectangle
			
				self.sx = event.x
				self.sy = event.y
				self.rect = self.segment_imageCanvas.create_rectangle(self.sx,self.sy,self.sx,self.sy, outline="yellow")
					
			def mousemove(event):
			# As mouse moves, expand rectangle
				self.ex = event.x
				self.ey = event.y
				self.segment_imageCanvas.coords(self.rect, self.sx,self.sy,self.ex,self.ey)
					
			def offmouse(event):
			# When mouse is released, change percentage boxes to new values
			
				# Clear Values
				self.segment_imageCanvas.delete(self.rect)				
				self.top_text.delete(0,END)
				self.bottom_text.delete(0,END)
				self.left_text.delete(0,END)
				self.right_text.delete(0,END)
			
				# If the box was created right to left	
				if self.sx < self.ex:
					self.left_text.insert(0,int(self.sx/self.segment_newImageSizeWidth*100))
					self.right_text.insert(0,int(self.ex/self.segment_newImageSizeWidth*100))
				else:
					self.left_text.insert(0,int(self.ex/self.segment_newImageSizeWidth*100))
					self.right_text.insert(0,int(self.sx/self.segment_newImageSizeWidth*100))
				
				# If the box was created left to right	
				if self.sy < self.ey:
					self.top_text.insert(0,int(self.sy/self.segment_newImageSizeHeight*100))
					self.bottom_text.insert(0,int(self.ey/self.segment_newImageSizeHeight*100))
				else:
					self.top_text.insert(0,int(self.ey/self.segment_newImageSizeHeight*100))
					self.bottom_text.insert(0,int(self.sy/self.segment_newImageSizeHeight*100))
				
				# Update Image Canvas
				self.cropped_image_updater()

			self.segment_imageCanvas.bind('<Button-1>',onmouse)
			self.segment_imageCanvas.bind('<B1-Motion>',mousemove)
			self.segment_imageCanvas.bind('<ButtonRelease>',offmouse)
				
	#########################
	#   Field Populators    #
	#########################

	def metadata_fields_displayer(self,tab,level):
		# Displays metadata fields (draws data from metadata_fields_dropdown_displayer)
		
		entries = []
		
		if level == "c": questions = self.collection_questions		
		if level == "i": questions = self.item_questions
		if level == "s": questions = self.segment_questions	
		
		# Create Entry Form Elements
		for field,question in questions.items():
		
			if field != "fabio_type":
			
				# Create Dropdown Menu
				self.provenance_user = StringVar(tab)
				
				# Set initial value
				self.provenance_user.set(self.default_user)
			
				# Create a row
				row = ttk.Frame(tab)

				# Create a label and text box
				label = ttk.Label(row, text=question, anchor='w', width=25)
				entry = ttk.Entry(row)
				provenance =  OptionMenu(row, self.provenance_user, *self.users)
				provenance.configure(width=int(4))

				# Package Row
				row.pack(side=TOP, fill=X)
				provenance.pack(side=RIGHT, padx=2)
				label.pack(side=LEFT)
				entry.pack(side=RIGHT, expand=YES, fill=X)

				# Fill entry with database values (if available)
				if level == 'c':
					try:
						entry_text = self.database[self.collection_index].get(field,'')[0]
						if self.database[self.collection_index].get(field,'')[1] != '':
							self.provenance_user.set(self.database[self.collection_index].get(field,'')[1])
					except(IndexError):
						entry_text = ''		

				if level == 'i':
					try:
						entry_text = self.database[self.collection_index]['items'][self.item_index].get(field,'')[0]
						if self.database[self.collection_index]['items'][self.item_index].get(field,'')[1] != '':
							self.provenance_user.set(self.database[self.collection_index]['items'][self.item_index].get(field,'')[1])
					except(IndexError):
						entry_text = ''	

				if level == 's':
					try:
						entry_text = self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index].get(field,'')[0]
						if self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index].get(field,'')[1] != '':
							self.provenance_user.set(self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index].get(field,'')[1])
					except(IndexError):
						entry_text = ''	

				entry.insert(0,entry_text)

				# Add field and value to save list
				entries.append((field, entry, self.provenance_user))

		# Save Entries to Level
		if level == "c": self.collection_entries = entries	
		if level == "i": self.item_entries = entries
		if level == "s": self.segment_entries = entries
		
	def metadata_fields_dropdown_displayer(self,event):
		# Loads metadata fields from configuration files (pulls data from metadata_tab_displayer)
		
		# Cleanup Exisiting Information
		try:
			self.entry_form.destroy()
		except(NameError,AttributeError):
			pass
		
		# Create Frames
		self.entry_form = ttk.Frame(self.current_tab)
		self.collection_entry_form = ttk.Frame(self.entry_form)
		self.item_entry_form = ttk.Frame(self.entry_form)
		self.segment_entry_form = ttk.Frame(self.entry_form)
		
		# Display Frames
		self.entry_form.pack(side=TOP, fill=X)
		self.collection_entry_form.pack(fill=X)
		self.item_entry_form.pack(fill=X)
		self.segment_entry_form.pack(fill=X)
				
		# Load Collection Metadata Questions
		if self.default_collection_type.get() != '':
			datafile = re.sub(' ','',self.default_collection_type.get()) + '.yaml'
		else:
			datafile = 'StandardCollection.yaml'
		
		with open (Path(self.config_path) / 'collections' / datafile, 'r') as collectionfile:
			self.collection_questions = yaml.safe_load(collectionfile)
		
		# Load Item Metadata Questions
		if self.current_level == 'i' or self.current_level == 's':

			if self.default_item_type.get() != '':
				datafile = re.sub(' ','',self.default_item_type.get()) + '.yaml'
			else:
				datafile = 'StandardItem.yaml'
			
			with open (Path(self.config_path) /'items' / datafile, 'r') as itemfile:
				self.item_questions = yaml.safe_load(itemfile)	  
		
		# Load Segment Metadata Questions
		if self.current_level == "s": 
		
			if self.default_segment_type.get() != '':
				datafile = re.sub(' ','',self.default_segment_type.get()) + '.yaml'
			else:
				datafile = 'StandardItem.yaml'
			with open (Path(self.config_path) /'segments' / datafile, 'r') as file:
				self.segment_questions = yaml.safe_load(file)
			
		# Print Metadata Set Based on Level
		self.metadata_fields_displayer(self.collection_entry_form,'c')
		if self.current_level == 'i' or self.current_level == 's': self.metadata_fields_displayer(self.item_entry_form,'i')
		if self.current_level == 's': self.metadata_fields_displayer(self.item_entry_form,'s')	
	
	####################
	#   Tab Display    #
	####################	

	def metadata_tab_displayer(self, tab, level):
		# Creates Metadata Tab
		
		self.current_tab = tab
		self.current_level = level
	
		# Populate Collection Types
		try:
			if level == 'c': self.types = [self.database[self.collection_index]['fabio_type'][len(self.collections_type_namespace):]]
			if level == 'i': self.types = [self.database[self.collection_index]['items'][self.item_index]['fabio_type'][len(self.item_type_namespace):]]
			if level == 's': self.types = ['StandardSegment']
		except(KeyError):
			if level == 'c': self.types = ['StandardCollection']
			if level == 'i': self.types = ['StandardItem']
			if level == 's': self.types = ['StandardSegment']
					
		# Create Types Drop Down Menu
		row = ttk.Frame(tab)
		
		def type_populator():
			# Looks up all available type YAML files
			for root, dirs, files in os.walk(Path(self.config_path) / self.directory):
				for file in files:
					if file.endswith(".yaml"):
						filename = re.sub('(?!^)([A-Z]+)', r' \1',os.path.splitext(file)[0])
						self.types.append(filename)
		
		# Set Options
		if level == "c": 
			self.directory = "collections"
			self.default_collection_type = StringVar(tab)
			type_populator()
			file_type_option = ttk.OptionMenu(row, self.default_collection_type, *self.types, command=self.metadata_fields_dropdown_displayer)
				
		elif level == "i": 
			self.directory = "items"
			self.default_item_type = StringVar(tab)
			type_populator()
			file_type_option = ttk.OptionMenu(row, self.default_item_type, *self.types, command=self.metadata_fields_dropdown_displayer)
				
		elif level == "s": 
			self.directory = "segments"
			self.default_segment_type = StringVar(tab)
			type_populator()
			file_type_option = ttk.OptionMenu(row, self.default_segment_type, *self.types, command=self.metadata_fields_dropdown_displayer)
		
		# Display Drop Down
		type_label =ttk.Label(row, text="Type:", width = 25)
		type_label.pack(side=LEFT)
		file_type_option.pack(side=LEFT)
		
		row.pack(side=TOP, fill=X, padx=5, pady=5)	
		
		# Load Saved or Default Type
		self.metadata_fields_dropdown_displayer('')

	def annotation_tab_displayer(self,tree_name,level):
	# Creates Annotation Tree Tab
	
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
			def individual_branch_builder(child_dictionary,parent_branch):

				# Create Lambda Dictionary
				x, d = -1, {}

				# Go through every key (numerical values) in current "children" dictionary
				for new_key,new_dictionary in child_dictionary.items():

					# Advance Branch Lambda Variable
					x = x + 1

					# Create New Branch
					d[x+1]=tree_name.insert(parent_branch, "end", new_dictionary['iid'], text=new_dictionary['name'],values=(new_dictionary[	'type'],new_dictionary['definition']))

					# Re-Run Recursive Function with New "children" Dictionary
					individual_branch_builder(new_dictionary['children'],d[x+1])

			# Begin Recursive Function
			individual_branch_builder(dictionary['children'],top)

		# Highlight Those Already Saved
		if level == 'i':

			if 'annotations' in self.database[self.collection_index]['items'][self.item_index]:
				for annotation in self.database[self.collection_index]['items'][self.item_index]['annotations']:
					tree_name.change_state(tree_name.parent(annotation[0]),"checked")
					tree_name.change_state(annotation[0],"checked")

		elif level == 's':

			if 'annotations' in self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]:
				for annotation in self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['annotations']:
					tree_name.change_state(tree_name.parent(annotation[0]),"checked")
					tree_name.change_state(annotation[0],"checked")

		# Display Tree
		tree_name.pack(anchor=NW)

	#####################
	#   Panel Display   #
	#####################	
	
	def segment_panels_displayer(self):
	# Creates Segment Level Panels
	
		##########################
		# Set Up Segment Display #
		##########################

		# Delete Previous Panels and Menus
		try:
			self.pane_one.destroy()
			self.pane_two.destroy()
			self.button_frame.destroy()
		except (NameError, AttributeError):
			pass			

		# Setup Segment Window Panels
		self.pane_one = ttk.Frame(self.database_window)
		self.pane_two = ttk.Frame(self.database_window)
		self.button_frame = ttk.Frame(self.database_window)
		self.button_frame.place(relwidth=1)
		self.button_frame.configure(relief=RIDGE)
		self.pane_one.place(y=42, relwidth=.49, relheight=1)
		self.pane_two.place(y = 77, x=15, relx=.5, relwidth=.45, relheight=1)

		# If the Segment is Text
		if self.database[self.collection_index]['items'][self.item_index]['item_type'] == 't':
		
			# Pull segmentation data
			start = self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['start']
			end = self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['end']

			# Create text boxes
			self.coord_box = ttk.Frame(self.pane_two)
			self.coord_box.place(relheight=.1, relwidth=1)
			
			# Starting Word
			self.start_box = ttk.Frame(self.coord_box)
			self.start_box.place(relwidth=.35, relx=.05)
			start_label = ttk.Label(self.start_box, text="Starting Word")
			self.start_text =  Spinbox(self.start_box,from_=0, to=len(self.database[self.collection_index]['items'][self.item_index]['transcription'][0].split()),command=(lambda: self.transcription_updater(int(self.start_text.get()),int(self.end_text.get()))))
			start_label.pack()
			self.start_text.pack()
			
			# Ending Word
			self.end_box = ttk.Frame(self.coord_box)
			self.end_box.place(relwidth=.35, relx=.45)
			end_label = ttk.Label(self.end_box, text="Ending Word")
			self.end_text =  Spinbox(self.end_box,from_=0, to=len(self.database[self.collection_index]['items'][self.item_index]['transcription'][0].split()),command=lambda: self.transcription_updater(int(self.start_text.get()),int(self.end_text.get())))
			end_label.pack()
			self.end_text.pack()
			
			# Update Button
			update_button = Button(self.coord_box, image=self.refresh_icon, command=(lambda: self.transcription_updater(0,len(self.transcription_words))))
			update_button_tt = ToolTip(update_button, "Reload Full Text",delay=0.01)
			update_button.place(relwidth=.1, relx=.9)

			# Fill Entry Boxes
			self.start_text.insert(4,start)
			self.end_text.insert(4,end)

			# Create Text Box
			self.transcription_text = Text(self.pane_two, wrap=WORD)
			
			# Create Segmentation Binder
			def text_selector(event):
				
				try:
					selection_index = self.database[self.collection_index]['items'][self.item_index]['transcription'][0].find(self.transcription_text.selection_get())
				except(TclError):
					pass
				else:
					pre_selection_length = self.database[self.collection_index]['items'][self.item_index]['transcription'][0][:selection_index].count(' ')
					selection_length = pre_selection_length + self.transcription_text.selection_get().count(' ')+1
					self.transcription_updater(pre_selection_length,selection_length)
					
			self.transcription_text.bind('<ButtonRelease>', text_selector)

			# Populate Text Box
			self.transcription_updater(int(self.start_text.get()),int(self.end_text.get()))

		# If the Segment is an Image
		elif self.database[self.collection_index]['items'][self.item_index]['item_type'] == 'i':

			# Pull segmentation data
			top = int(self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['top'])
			left = int(self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['left'])
			bottom = int(self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['bottom'])
			right = int(self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['right'])

			def segmenter_box_maker(frame,label,entry,xcoord,ycoord,width):
				# Create Label
				frame_label =ttk.Label(frame, text=label)
				
				# Pack All Pieces Together
				frame_label.pack()
				entry.pack()
				frame.place(relx=xcoord,rely=ycoord,relwidth=width)
			
			# Create Segmenter Frame
			self.segmenter_frame = ttk.Frame(self.pane_two)		
			
			# Create text boxes
			self.top_box = ttk.Frame(self.segmenter_frame)
			self.top_text =  Spinbox(self.top_box,from_=0, to=100,command=self.cropped_image_updater)
			segmenter_box_maker(self.top_box,'% from the Top',self.top_text,.05,.1,.4)
			
			self.bottom_box = ttk.Frame(self.segmenter_frame)
			self.bottom_text =  Spinbox(self.bottom_box,from_=0, to=100,command=self.cropped_image_updater)
			segmenter_box_maker(self.bottom_box,'% to the Bottom',self.bottom_text,.05,.4,.4)
			
			self.left_box = ttk.Frame(self.segmenter_frame)
			self.left_text =  Spinbox(self.left_box,from_=0, to=100,command=self.cropped_image_updater)
			segmenter_box_maker(self.left_box,'% from the Left',self.left_text,.45,.1,.4)
			
			self.right_box = ttk.Frame(self.segmenter_frame)
			self.right_text = Spinbox(self.right_box,from_=0, to=100,command=self.cropped_image_updater)
			segmenter_box_maker(self.right_box,'% to the Right',self.right_text,.45,.4,.4)

			# Fill Entry Boxes
			self.top_text.insert(4,top)
			self.bottom_text.insert(4,bottom)
			self.left_text.insert(4,left)
			self.right_text.insert(4,right)

			# Create and Pack Update Button
			update_button = Button(self.segmenter_frame, image=self.refresh_icon, command=self.image_resetter)
			update_button_tt = ToolTip(update_button, "Reload Full Image",delay=0.01)
			update_button.place(relx=.85,rely=.2,relheight=.25,relwidth=.1)
			
			# Create Image Canvas
			self.segment_imageCanvas = Canvas(self.pane_two)
			self.segmenter_frame.place(rely = .54, relwidth=1, relheight=.25)
			self.cropped_image_updater()
	
		# Setup Segment Window Tabs (Left / Pane 1)

		# Create "save", "reset" and "return" buttons
		save_button = Button(self.button_frame , image=self.save_icon, command=(lambda: self.database_entry_saver('s')))
		save_button_tt = ToolTip(save_button, "Save Segment",delay=0.01)
		refresh_button = Button(self.button_frame , image=self.refresh_icon, command=self.segment_panels_displayer)
		refresh_button_tt = ToolTip(refresh_button, "Reload Segment",delay=0.01)
		return_button = Button(self.button_frame, image=self.up_level_icon, command=(lambda: self.item_panels_displayer('m')))
		return_button_tt = ToolTip(return_button, "Return to Item View",delay=0.01)
		return_button.pack(side=LEFT)
		save_button.pack(side=LEFT)
		refresh_button.pack(side=LEFT)
		
		# Set Up Tabs
		self.segment_tab_control = ttk.Notebook(self.pane_one)
		self.segment_tab_one = ttk.Frame(self.segment_tab_control)
		self.segment_tab_two = ttk.Frame(self.segment_tab_control)
		self.segment_tab_three = ttk.Frame(self.segment_tab_control)
		
		# Pack Tabs into ttk.Frame
		self.segment_tab_control.add(self.segment_tab_one, text='Bibliographic Information')
		self.segment_tab_control.add(self.segment_tab_two, text='Annotations')
		self.segment_tab_control.add(self.segment_tab_three, text='Notes')
		self.segment_tab_control.pack(expand=1, fill='both')


		########################################
		# Set up bibliographic information tab #
		########################################

		# Display Editor Box for Record 
		
		# Create String Variable
		self.provenance_segment_editor = StringVar(self.segment_tab_one)
		
		# Set initial value
		if self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['schema:editor'][0] !='':
			self.provenance_segment_editor.set(self.database[self.collection_index]['items'][self.item_index]['schema:editor'][0])
		else:
			self.provenance_segment_editor.set(self.default_user)
	
		# Create a row
		row = ttk.Frame(self.segment_tab_one)

		# Create a labels and dropdown
		label =ttk.Label(row, text="Record Creator", anchor='w', width=25)
		provenance =  OptionMenu(row, self.provenance_segment_editor, *self.users)		
		modified_date = '{}/{}/{}'.format(self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['schema:editor'][2][6:8],self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['schema:editor'][2][4:6],self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['schema:editor'][2][:4])
		last_modified_label =ttk.Label(row, text='Last Modified: ' + modified_date, anchor='w', width=25)

		# Package Row
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		label.pack(side=LEFT)
		provenance.pack(side=LEFT)
		last_modified_label.pack(side=RIGHT)

		# Display bibliographic form and create entries database
		self.metadata_tab_displayer(self.segment_tab_one, 's')

		##########################
		# Set up Annotations Tab #
		##########################

		# Display Editor Box for Tree 
		
		# Create String Variable
		self.segment_annotation_editor = StringVar(self.segment_tab_two)
		
		# Set initial value
		self.segment_annotation_editor.set(self.default_user)
	
		# Create a row
		row = ttk.Frame(self.segment_tab_two)

		# Create a labels and dropdown
		label =ttk.Label(row, text="Current Annotator", anchor='w', width=25)
		provenance =  OptionMenu(row, self.segment_annotation_editor, *self.users)

		# Package Row
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		label.pack(side=LEFT)
		provenance.pack(side=LEFT)
		
		# Create Tree
		self.segment_tree=CheckboxTreeview(self.segment_tab_two,height="30")
		self.annotation_tab_displayer(self.segment_tree,'s')
		
		####################
		# Set up Notes Tab #
		####################
		
		# Display Editor Box for Tree 
		
		# Create String Variable
		self.segment_note_editor = StringVar(self.segment_tab_three)
		
		# Set initial value
		self.segment_note_editor.set(self.default_user)
	
		# Create a row
		row = ttk.Frame(self.segment_tab_three)

		# Create a labels and dropdown
		label =ttk.Label(row, text="Current Annotator", anchor='w', width=25)
		provenance =  OptionMenu(row, self.segment_note_editor, *self.users)

		# Package Row
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		label.pack(side=LEFT)
		provenance.pack(side=LEFT)
		
		self.note_text = Text(self.segment_tab_three, wrap=WORD)
		self.note_text.config(font=(10))
		try:
			self.note_text.insert("0.0",self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['nisaba:notes'][0])
		except(KeyError):
			pass
		self.note_text.pack(expand=Y,fill=BOTH)
	
	def item_panels_displayer(self,focus):
	# Creates Item Level Panels
	
		try:
			self.pane_one.destroy()
			self.pane_two.destroy()
			self.button_frame.destroy()
		except (NameError, AttributeError):
			pass			

		# Setup Segment Window Panels
		self.pane_one = ttk.Frame(self.database_window)
		self.pane_two = ttk.Frame(self.database_window)
		self.button_frame = ttk.Frame(self.database_window)
		self.button_frame.place(relwidth=1)
		self.button_frame.configure(relief=RIDGE)
		self.pane_one.place(y=42, relwidth=.45, relheight=1)
		self.pane_two.place(y = 52, x=15, relx=.48, relwidth=.4, relheight=1)

		####################################
		# Setup Item Display Panel (Right) #
		####################################

		# If the Item is Text
		if self.database[self.collection_index]['items'][self.item_index]['item_type'] == 't':

			# Pull Transcription from Database
			if 'transcription' in self.database[self.collection_index]['items'][self.item_index]:
				transcription = self.database[self.collection_index]['items'][self.item_index]['transcription'][0]
			else:
				transcription = ""

			# Create wrapping text box
			self.transcription_text = Text(self.pane_two, wrap=WORD)

			# Insert transcription in text box
			self.transcription_text.insert("1.0",transcription)
			self.transcription_text.configure(font=(10))
			
			# Create Dropdown Menu
			self.transcription_provenance_user = StringVar(self.pane_two)
			
			# Set initial value
			self.transcription_provenance_user.set(self.default_user)
			
			# Create Provenance Box
			self.transcription_provenance_row = ttk.Frame(self.pane_two)
			self.transcription_provenance_label =ttk.Label(self.transcription_provenance_row, text="Transcriber: ")
			self.transcription_provenance = OptionMenu(self.transcription_provenance_row, self.transcription_provenance_user, *self.users)
			
			if self.database[self.collection_index]['items'][self.item_index]['transcription'][1] != '':
				self.transcription_provenance_user.set(self.database[self.collection_index]['items'][self.item_index]['transcription'][1])
			
			# Display text boxes
			self.transcription_text.pack(padx=10,pady=10)
			self.transcription_provenance_row.pack()
			self.transcription_provenance_label.pack(side=LEFT)
			self.transcription_provenance.pack(side=RIGHT)		

		# If the Item is an Image
		elif self.database[self.collection_index]['items'][self.item_index]['item_type'] == 'i':

			# Create text boxes
			self.image_label =ttk.Label(self.pane_two, text="Image File")
			self.image_filename = ttk.Entry(self.pane_two)

			# Fill Entry Boxes
			self.image_filename.insert(4,self.database[self.collection_index]['items'][self.item_index]['image_file'])

			# Display Image Filename
			self.image_label.grid(column = 1, row = 0)
			self.image_filename.grid(column = 2, row = 0)

			try:
				# Set image file
				self.filename = str(Path(self.raw_data_images_path) / self.database[self.collection_index]['items'][self.item_index]['image_file'])
				image = PIL.Image.open(self.filename)	
				
			except(FileNotFoundError):
				self.filename = str(Path(self.raw_data_images_path) / 'sample.jpg')
				image = PIL.Image.open(self.filename)	
				label = ttk.Label(self.pane_two, text="Image Not Found!")
				label.grid(column=2,row=3)			

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
		self.item_tab_one = ttk.Frame(self.item_tab_control)
		self.item_tab_two = ttk.Frame(self.item_tab_control)
		self.item_tab_three = ttk.Frame(self.item_tab_control)

		# Pack Tabs into ttk.Frame
		self.item_tab_control.add(self.item_tab_one, text='Bibliographic Information')
		self.item_tab_control.add(self.item_tab_two, text='Annotations')
		self.item_tab_control.add(self.item_tab_three, text='Segments')
		self.item_tab_control.pack(expand=1, fill=BOTH)

		# Set Focus
		if focus == 'm':
			self.item_tab_control.select(self.item_tab_one)
		if focus == 'a':
			self.item_tab_control.select(self.item_tab_two)
		if focus == 's':
			self.item_tab_control.select(self.item_tab_three)
		
		# Create buttons for all tabs
		self.add_button = Button(self.button_frame, image=self.add_icon,command=self.segment_adder)
		add_button_tt = ToolTip(self.add_button, "Add Segment",delay=0.01)
		self.delete_segment_button = Button(self.button_frame, image=self.delete_icon, command=(lambda: self.unit_deleter(self.database[self.collection_index]['items'][self.item_index]['segments'],str(self.segments.curselection()[0]),'s')))
		delete_segment_tt = ToolTip(self.delete_segment_button, "Delete Selected Segment",delay=0.01)
		self.save_button = Button(self.button_frame, image=self.save_icon, command=(lambda: self.database_entry_saver('i')))
		save_button_tt = ToolTip(self.save_button, "Save Item",delay=0.01)
		self.refresh_button = Button(self.button_frame, image=self.refresh_icon, command=(lambda: self.item_panels_displayer('m')))
		refresh_button_tt = ToolTip(self.refresh_button, "Reload Item",delay=0.01)
		self.return_button = Button(self.button_frame, image=self.up_level_icon, command=(lambda: self.collection_informer('')))
		return_button_tt = ToolTip(self.return_button, "Return to Item View",delay=0.01)
		
		self.return_button.pack(side=LEFT)
		self.save_button.pack(side=LEFT)
		self.refresh_button.pack(side=LEFT)
		self.add_button.pack(side=LEFT)
		self.delete_segment_button.pack(side=LEFT)

		########################################
		# Set up Bibliographic Information Tab #
		########################################

		# Display Editor Box for Record 
			
		# Create String Variable
		self.provenance_item_editor = StringVar(self.item_tab_one)
		
		# Set initial value
		if self.database[self.collection_index]['items'][self.item_index]['schema:editor'][0] !='':
			self.provenance_item_editor.set(self.database[self.collection_index]['items'][self.item_index]['schema:editor'][0])
		else:
			self.provenance_item_editor.set(self.default_user)
	
		# Create a row
		row = ttk.Frame(self.item_tab_one)

		# Create a label and dropdown
		label =ttk.Label(row, text="Record Creator", anchor='w', width=25)
		provenance =  OptionMenu(row, self.provenance_item_editor, *self.users)
		modified_date = '{}/{}/{}'.format(self.database[self.collection_index]['items'][self.item_index]['schema:editor'][2][6:8],self.database[self.collection_index]['items'][self.item_index]['schema:editor'][2][4:6],self.database[self.collection_index]['items'][self.item_index]['schema:editor'][2][:4])
		last_modified_label =ttk.Label(row, text='Modified: ' + modified_date, anchor='w', width=25)

		# Package Row
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		label.pack(side=LEFT)
		provenance.pack(side=LEFT)
		last_modified_label.pack(side=RIGHT)
		
		# Display bibliographic form and create entries database
		self.metadata_tab_displayer(self.item_tab_one, 'i')

		##########################
		# Set up Annotations Tab #
		##########################

		# Display Editor Box for Tree 
		
		# Create String Variable
		self.item_annotation_editor = StringVar(self.item_tab_two)
		
		# Set initial value
		self.item_annotation_editor.set(self.default_user)
	
		# Create a row
		row = ttk.Frame(self.item_tab_two)

		# Create a labels and dropdown
		label =ttk.Label(row, text="Current Annotator", anchor='w', width=25)
		provenance =  OptionMenu(row, self.item_annotation_editor, *self.users)

		# Package Row
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		label.pack(side=LEFT)
		provenance.pack(side=LEFT)
		
		# Create Tree
		self.item_tree = CheckboxTreeview(self.item_tab_two,height="30",)
		self.annotation_tab_displayer(self.item_tree,'i')

		#######################
		# Set Up Segments Tab #
		#######################

		# Set up segment list scrollbar
		self.scrollbar = Scrollbar(self.item_tab_three)
		self.scrollbar.pack(side=RIGHT,fill=Y)

		# Set Up segment listbox
		self.segments = Listbox(self.item_tab_three)
		self.segments.pack(anchor=W, fill=BOTH, expand=True)

		#Populate Segment List Box
		for segment_number,dictionary in self.database[self.collection_index]['items'][self.item_index]['segments'].items():

			# If the segment is text
			if self.database[self.collection_index]['items'][self.item_index]['item_type'] == "t":

				# Obtain Snippet Transcription and Package for Display
				transcription_words = self.database[self.collection_index]['items'][self.item_index]['transcription'][0].split()
				display_item = ' '.join(transcription_words[dictionary['start']:dictionary['start']+10])

			# If the segment is an image
			elif self.database[self.collection_index]['items'][self.item_index]['item_type'] == "i":

				display_item = 'Image Snippet'
				# ACTION: Add coordinates to display_item text

			# Display the number and title
			segment_number_str = str(int(segment_number)+1)
			segment = " " + segment_number_str + ". " + display_item
			self.segments.insert(END, segment)

			# Bind scrollbar to listbox
			self.segments.config(yscrollcommand=self.scrollbar.set)
			self.scrollbar.config(command=self.segments.yview)

			# Bind selection to event
			self.segments.bind('<Double-Button>', self.segment_informer)
	
	def collection_metadata_panel_displayer(self):
	# Creates Collection Metadata Panel

	
		# Delete Previous Panels and Menus
		try:
			self.pane_one.destroy()
			self.button_frame.destroy()
		except (NameError, AttributeError):
			pass			

		# Setup Segment Window Panels
		self.button_frame = ttk.Frame(self.database_window)
		self.button_frame.place(relwidth=1)
		self.button_frame.configure(relief=RIDGE)
		self.pane_one = ttk.Frame(self.database_window)
		self.pane_one.place(y=42, relwidth=.45, relheight=1)
		item_metadata_frame = ttk.Frame(self.pane_one)
		item_metadata_buttonFrame = ttk.Frame(self.pane_one)
		item_metadata_frame.pack(side=TOP, expand=True, fill=X, anchor='nw')
		item_metadata_buttonFrame.pack(side=BOTTOM, anchor='w')
		
		# Retrieve Existing User List
		self.users = ['']
		self.default_user = ''

		for key,value in self.database['users'].items():
			self.users.append(key)
			if value.get('default',0,) == 1:
				self.default_user = key
		
		#####################
		# Display Editor Box #
		#####################
		
		# Create String Variable
		self.provenance_collection_editor = StringVar(item_metadata_frame)
		
		# Set initial value
		if self.database[self.collection_index]['schema:editor'][0] !='':
			self.provenance_collection_editor.set(self.database[self.collection_index]['schema:editor'][0])
		else:
			self.provenance_collection_editor.set(self.default_user)
	
		# Create a row
		row = ttk.Frame(item_metadata_frame)

		# Create a label and dropdown
		label =ttk.Label(row, text="Record Creator", anchor='w', width=25)
		provenance =  OptionMenu(row, self.provenance_collection_editor, *self.users)
		modified_date = '{}/{}/{}'.format(self.database[self.collection_index]['schema:editor'][2][6:8],self.database[self.collection_index]['schema:editor'][2][4:6],self.database[self.collection_index]['schema:editor'][2][:4])
		last_modified_label =ttk.Label(row, text='Modified: ' + modified_date, anchor='w', width=25)
		
		# Package Row
		row.pack(side=TOP, fill=X, padx=5, pady=5)
		label.pack(side=LEFT)
		provenance.pack(side=LEFT)
		last_modified_label.pack(side=RIGHT)
			
		####################
		# Display Metadata #
		####################
		
		# Display bibliographic form and create entries database
		self.metadata_tab_displayer(item_metadata_frame, 'c')

		# Create "save" button for all tabs
		save_item_button = Button(self.button_frame, image=self.save_icon, command=(lambda: self.database_entry_saver('c')))
		save_item_button_tt = ToolTip(save_item_button, "Save Collection",delay=0.01)
		
		collections_list_button = Button(self.button_frame, image=self.up_level_icon, command=(lambda: self.database_panels_displayer(self.database_window)))
		collections_list_button_tt = ToolTip(collections_list_button, "Return to Collections List",delay=0.01)
		
		collections_list_button.pack(side=LEFT)
		save_item_button.pack(side=LEFT)
				
	def collection_item_list_panel_displayer(self):
	# Creates Collection Item-List Panel

		# Delete Any Existing Information
		try:
			self.pane_two.destroy()
		except (NameError, AttributeError):
			pass

		self.pane_two = ttk.Frame(self.database_window)
		self.pane_two.place(y = 52, x=15, relx=.48, relwidth=.45, relheight=1)

		# Setup scroll bar
		scrollbar = Scrollbar(self.pane_two)
		scrollbar.pack(side=RIGHT,fill=Y)

		# Setup listbox
		items_list = Listbox(self.pane_two)
		items_list.pack(anchor=W, fill="both", expand=True)

		# Populate listbox
		for item_number,dictionary in self.database[self.collection_index]['items'].items():

			# If the item has a title
			if self.item_title_namespace in self.database[self.collection_index]['items'][item_number]:
				display_item = dictionary[self.item_title_namespace][0]
				
			# If the item has descriptive parts
			elif 'fabio_type' in self.database[self.collection_index]['items'][item_number]:
				if self.collections_title_namespace in self.database[self.collection_index]:
					if 'fabio:hasSequenceIdentifier' in self.database[self.collection_index]['items'][item_number] and dictionary['fabio:hasSequenceIdentifier'][0] != '':
						if 'fabio:pageRange' in self.database[self.collection_index]['items'][item_number] and self.database[self.collection_index]['items'][item_number]['fabio:pageRange'][0] !='':
							display_item = "{0} {1} on page(s) {2}".format(str(dictionary['fabio_type'][len(self.item_type_namespace):]),str(dictionary['fabio:hasSequenceIdentifier'][0]),str(dictionary['fabio:pageRange'][0]))
						else: 
							display_item = "{0} {1}".format(str(dictionary['fabio_type'][len(self.item_type_namespace):]),str(dictionary['fabio:hasSequenceIdentifier'][0]))
					elif 'fabio:pageRange' in self.database[self.collection_index]['items'][item_number]:
						display_item = "{0} on pages {1}".format(str(dictionary['fabio_type'][len(self.item_type_namespace):]),str(dictionary['fabio:pageRange'][0]))
					else:
						display_item = "{0} of the {1}".format(str(dictionary['fabio_type'][len(self.item_type_namespace):]),str(self.database[self.collection_index][self.collections_title_namespace][0]))
				else:
					display_item = "{0}, part of an unknown Collection".format(str(self.database[self.collection_index]['items'][item_number]['fabio_type'][len(self.item_type_namespace):]))

			else:
				display_item = "No title listed"

			# Display the item title and author
			item_number_str = str(int(item_number)+1)
			item = " " + item_number_str  + ". " + display_item
			items_list.insert(END, item)

		# Bind scrollbar to listbox
		items_list.config(yscrollcommand=scrollbar.set)
		scrollbar.config(command=items_list.yview)

		# Bind selected item to event
		items_list.bind('<Double-Button>', self.item_informer)

		# Create "save" button for all tabs
		self.buttonFrame = ttk.Frame(self.pane_two)
		
		self.add_text_button = Button(self.buttonFrame, image=self.text_icon, command=(lambda t="t": self.item_adder(t)))
		add_item_button_tt = ToolTip(self.add_text_button, "Add Text Item",delay=0.01)
		self.add_image_button = Button(self.buttonFrame, image=self.image_icon, command=(lambda t="i": self.item_adder(t)))
		add_image_button_tt = ToolTip(self.add_image_button, "Add Image Item",delay=0.01)
		self.add_audio_button = Button(self.buttonFrame, image=self.audio_icon, command=(lambda t="a": self.item_adder(t)))
		add_audio_button_tt = ToolTip(self.add_audio_button, "Add Audio Item",delay=0.01)
		self.add_audiovisual_button = Button(self.buttonFrame, image=self.audiovisual_icon, command=(lambda t="av": self.item_adder(t)))
		add_audiovisual_button_tt = ToolTip(self.add_audiovisual_button, "Add Audio-Visual Item",delay=0.01)
		self.delete_item_button = Button(self.buttonFrame, image=self.delete_icon, command=(lambda: self.unit_deleter(self.database[self.collection_index]['items'],str(items_list.curselection()[0]),'i')))
		delete_item_tt = ToolTip(self.delete_item_button, "Delete Selected Item",delay=0.01)
		
		self.add_text_button.pack(side=LEFT)
		self.add_image_button.pack(side=LEFT)
		self.add_audio_button.pack(side=LEFT)
		self.add_audiovisual_button.pack(side=LEFT)
		self.delete_item_button.pack(side=RIGHT, padx=5, pady=5)
		
		self.buttonFrame.pack(anchor=NW)
	
	def database_panels_displayer(self,window):
	# Display Database Panels
		
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

		# Setup Window Panes
		self.button_frame = ttk.Frame(self.database_window)
		self.button_frame.place(relwidth=1)
		self.button_frame.configure(relief=RIDGE)
		self.pane_one = ttk.Frame(self.database_window)
		self.pane_one.place(y=42, relwidth=1, relheight=.8)
		
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

				# If the collection has a title
				if self.collections_title_namespace in self.database[collection_number]:
					display_item = str(dictionary[self.collections_title_namespace][0])

				else:
					display_item = "No title listed"

				# Display the item title and author
				collection_number_str = str(int(collection_number)+1)
				item = " " + collection_number_str + ". " + display_item
				items.insert(END, item)

		# Bind scrollbar to listbox
		items.config(yscrollcommand=scrollbar.set)
		scrollbar.config(command=items.yview)

		# Bind selected item to event
		items.bind('<Double-Button>', self.collection_informer)

		# Add/Delete Collection Buttons
		self.add_collection_button = Button(self.button_frame, image=self.add_icon,command=self.collection_adder)
		add_collection_tt = ToolTip(self.add_collection_button, "Add Collection",delay=0.01)
		self.delete_collection_button = Button(self.button_frame, image=self.delete_icon, command=(lambda: self.unit_deleter(self.database,str(items.curselection()[0]),'c')))
		delete_collection_tt = ToolTip(self.delete_collection_button, "Delete Selected Collection",delay=0.01)
		self.add_collection_button.pack(side=LEFT)
		self.delete_collection_button.pack(side=LEFT)

	########################
	#         Main         #
	########################	
		
	def database_window_viewer(self,window):
	# Setup Database Frame
	
		##################
		# Window Cleanup #
		##################
		
		# Delete Previous Panels and Menus or Create New Window
		try:
			self.database_window.destroy()
		except (NameError, AttributeError):
			pass
			
		# Set Name of Collections Frame	
		self.database_window = window	
			
		# Set Style Information
		window_width = self.database_window.winfo_screenwidth()
		window_height = self.database_window.winfo_screenheight()
		style = ttk.Style()		
		style.configure("TLabel", font=('Calibri', 10))
		style.configure("TEntry", font=('Calibri', 10))
		style.configure("TNotebook", borderwidth=0)
		style.configure("Tab", focuscolor=style.configure(".")["background"])
		style.configure("TOptionMenu", focuscolor=style.configure(".")["background"])
		style.configure("Checkbox.Treeview", font=('Calibri', 10))
		style.configure('Checkbox.Treeview', rowheight=18)	
		style.configure('TMenubutton', relief='flat')
		
			
		# Set Icon Assets
		# Menu Bar Icons made by Pixel Buddha (https://www.flaticon.com/authors/pixel-buddha) from http://www.flaticon.com  CC-BY (http://creativecommons.org/licenses/by/3.0/)
		self.up_level_icon=PhotoImage(file=Path(self.assets_path) / 'uplevel.png')
		self.add_icon=PhotoImage(file=Path(self.assets_path) / 'add.png')
		self.delete_icon=PhotoImage(file=Path(self.assets_path) / 'delete.png')
		self.plus_icon=PhotoImage(file=Path(self.assets_path) / 'plus.png')
		self.minus_icon=PhotoImage(file=Path(self.assets_path) / 'minus.png')		
		self.save_icon=PhotoImage(file=Path(self.assets_path) / 'save.png')
		self.refresh_icon=PhotoImage(file=Path(self.assets_path) / 'refresh.png')
		self.text_icon=PhotoImage(file=Path(self.assets_path) / 'text.png')
		self.image_icon=PhotoImage(file=Path(self.assets_path) / 'image.png')
		self.audio_icon=PhotoImage(file=Path(self.assets_path) / 'audio.png')
		self.audiovisual_icon=PhotoImage(file=Path(self.assets_path) / 'audiovisual.png')

		# This is a prefix to put before the filename of the collection type, derived from the filename question config. For example 'book.tsv' with a namespace of 'fabio' would be 'fabio:book'
		self.collections_type_namespace = self.config['v_Collection_Namespace']
		
		# This the field that is pulled in the listboxes for collections
		self.collections_title_namespace = self.config['v_Collection_Title_Field']
		
		# This is a prefix to put before the filename of the type type, derived from a drop down in the item screen. For example 'page' with a namespace of 'fabio' would be 'fabio:page'
		self.item_type_namespace = self.config['v_Item_Namespace']
		
		# This the field that is pulled in the listboxes for items
		self.item_title_namespace = self.config['v_Collection_Title_Field']
		
		# Open Frame
		self.database_panels_displayer(self.database_window)