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
import PIL.Image

class search_display(cache_maintenance):

	#########################
	#   Field Populators    #
	#########################

	def taxon_branch_builder(self,database,key):
	# Populates tree branches with data
		
		# Set Taxon Dictionary
		dictionary = database[key]
		
		# Create Root
		top=self.search_tree.insert("", "end", dictionary['iid'], text=dictionary['name'], values=(dictionary['type'],dictionary['definition']),open = True)

		def individual_branch_builder(child_dictionary,parent_branch):
		# Recursive Function to Go Through an Unknown Number of Layers

			alpha_child_taxonomy = self.database_alphabetiser(child_dictionary)	
						
			for taxon in alpha_child_taxonomy:	
			
				# Create Lambda Dictionary
				x, d = -1, {}

				# Go Through Every Key (Numerical Values) in Current "children" Dictionary
				for new_key,new_dictionary in child_dictionary.items():

					if new_dictionary['iid'] == taxon:
				
						# Advance Branch Lambda Variable
						x = x + 1

						# Create New Branch
						d[x+1]=self.search_tree.insert(parent_branch, "end", new_dictionary['iid'], text=new_dictionary['name'],values=(new_dictionary['type'],new_dictionary['definition']),open = False)

						# Re-Run Recursive Function with New "children" Dictionary
						individual_branch_builder(new_dictionary['children'],d[x+1])

		# Begin Recursive Function
		individual_branch_builder(dictionary['children'],top)


	#########################
	#   Event Processing    #
	#########################		

	def result_viewer(self,event):		
		segment_event_data = event.widget
		segment_selection = segment_event_data.curselection()[0]
		selection_coordinates = self.export_list[segment_selection]	
		
		self.segment_displayer(selection_coordinates)
		
	def taxon_informer(self,event):
	# Send Selected ID to Iterator

		# Get Selected ID from Click Event
		self.clicked_item = self.search_tree.identify('item',event.x,event.y)

		# Send to iid_iterator
		self.iid_iterator(self.taxonomy,self.search_tree.identify('item',event.x,event.y),self.taxon_list_displayer)

	#####################
	#   Panel Display   #
	#####################		
	
	def note_displayer(self,selection_coordinates):
	# Display notes on segment
	
		self.note_text = Text(self.pane_two_bottom_right, wrap=WORD)
		self.note_text.configure(font=(10))
		self.note_text.pack(anchor="nw", expand=Y, fill=BOTH)
		try:
			full_note = self.database[selection_coordinates[0]]['items'][selection_coordinates[1]]['segments'][selection_coordinates[2]]['nisaba:notes']
		except(KeyError):
			pass
		else:
			note = full_note[0]
			signature = full_note[1]
			date = '{}/{}/{}'.format(full_note[2][6:8],full_note[2][4:6],full_note[2][:4])
			
			notes = '{} -{} ({})'.format(note,signature,date)
			self.note_text.insert("0.0",notes)
	
	def segment_displayer(self,selection_coordinates):
	
		self.pane_two_bottom_left.destroy()		
		self.pane_two_bottom_right.destroy()		
		self.pane_two_bottom_left = ttk.Frame(self.search_window)
		self.pane_two_bottom_left.place(relx=.25, rely = .45, relwidth=.32, relheight=.4)
		self.pane_two_bottom_right = ttk.Frame(self.search_window)
		self.pane_two_bottom_right.place(relx=.65, rely = .45, relwidth=.32, relheight=.4)
		
		self.collection_index = selection_coordinates[0]
		self.item_index = selection_coordinates[1]
		self.segment_index = selection_coordinates[2]
	
		# If the Segment is Text
		if self.database[self.collection_index]['items'][self.item_index]['item_type'] == 't':
		
			# Pull segmentation data
			start = self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['start']
			end = self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['end']

			# Create Text Box
			self.transcription_text = Text(self.pane_two_bottom_left, wrap=WORD)

			# Populate Text Box
			
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
			self.transcription_text.pack(anchor="nw", expand=Y, fill=BOTH)

		# If the Segment is an Image
		elif self.database[self.collection_index]['items'][self.item_index]['item_type'] == 'i':

			# Pull segmentation data
			self.top = int(self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['top'])
			self.left = int(self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['left'])
			self.bottom = int(self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['bottom'])
			self.right = int(self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['right'])
			
			# Create Image Canvas
			self.segment_imageCanvas = Canvas(self.pane_two_bottom_left)

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
			self.segment_imageCanvas.config(width=self.segment_newImageSizeWidth+10, height = self.segment_newImageSizeHeight+10, background="light gray")
			self.segment_imageCanvas.pack()

			# Add Image to Canvas
			self.segment_imageCanvas.create_image(self.segment_newImageSizeWidth/2+6,
												  self.segment_newImageSizeHeight/2+6,
												  image=self.segment_photoImg,
												  anchor="center")
	
		# Display Notes
		self.note_displayer(selection_coordinates)
	
	def taxon_list_displayer(self,database,key):
	# Displays Taxon Editor Panel
	
		current_id = database[key]['iid']
	
		# Delete Any Existing Information
		try:
			self.pane_two.destroy()
			self.pane_two_bottom_left.destroy()
			self.pane_two_bottom_right.destroy()
		except (NameError, AttributeError):
			pass
		
		self.export_list = []
		
		# Setup search Window Panels
		self.pane_two = ttk.Frame(self.search_window)
		self.pane_two.place(y=15, relx=.25, relwidth=.74, relheight=.4)
		self.pane_two_bottom_left = ttk.Frame(self.search_window)
		self.pane_two_bottom_left.place(relx=.25, rely = .45, relwidth=.32, relheight=.4)
		self.pane_two_bottom_right = ttk.Frame(self.search_window)
		self.pane_two_bottom_right.place(relx=.65, rely = .45, relwidth=.32, relheight=.4)
		
		# Set up segment list scrollbar
		self.scrollbar = Scrollbar(self.pane_two)
		self.scrollbar.pack(side=RIGHT,fill=Y)

		# Set Up segment listbox
		self.segments = Listbox(self.pane_two)
		self.segments.pack(anchor=W, fill=BOTH, expand=True)

		#Populate Segment List Box
		for collection_number,dictionary in self.database.items():
			if collection_number != 'users':
				for item_number,item_dictionary in self.database[collection_number]['items'].items():
					for segment_number,segment_dictionary in self.database[collection_number]['items'][item_number]['segments'].items():
						if 'annotations' in segment_dictionary:
							for annotation in segment_dictionary['annotations']:
								if annotation[0] == current_id:
							
									# If the segment is text
									if self.database[collection_number]['items'][item_number]['item_type'] == "t":
									
										if 'fabio:pageRange' in self.database[collection_number]['items'][item_number]:
		
											if 'dc:description' in self.database[collection_number]['items'][item_number]['segments'][segment_number]:
		
												display_item = "Text " + str(int(segment_number) +1) + ' of Page ' + self.database[collection_number]['items'][item_number]['fabio:pageRange'][0] + ' of ' + self.database[collection_number]['dc:title'][0] + ': ' + self.database[collection_number]['items'][item_number]['segments'][segment_number]['dc:description'][0] 
												
											else:
												display_item = "Text " + str(int(segment_number) +1) + ' of Page ' + self.database[collection_number]['items'][item_number]['fabio:pageRange'][0] + ' of ' + self.database[collection_number]['dc:title'][0]
											
										else: 
                                        
											if 'dc:description' in self.database[collection_number]['items'][item_number]['segments'][segment_number]:
                                                
												display_item = 'Text ' + str(int(item_number) + 1) + ":" + str(int(segment_number) +1) + ' of ' + self.database[collection_number]['dc:title'][0] + ': ' + self.database[collection_number]['items'][item_number]['segments'][segment_number]['dc:description'][0] 
                                            
											else: 
                                            
												display_item = 'Text ' + str(int(item_number) + 1) + ":" + str(int(segment_number) +1) + ' of ' + self.database[collection_number]['dc:title'][0]

									# If the segment is an image
									elif self.database[collection_number]['items'][item_number]['item_type'] == "i":

										display_item = 'Image ' + str(int(item_number) + 1) + ":" + str(int(segment_number) +1) + ' of ' + self.database[collection_number]['dc:title'][0]

									# Display the number and title
									segment = display_item
									self.segments.insert(END, segment)
									
									# Save to export list
									self.export_list.append([collection_number,item_number,segment_number])
			
		# Bind scrollbar to listbox
		self.segments.config(yscrollcommand=self.scrollbar.set)
		self.scrollbar.config(command=self.segments.yview)
		
		# Bind command to double-click segment
		self.segments.bind('<Double-Button>', self.result_viewer)

	def taxon_tree_displayer(self):
	# Displays search Tree Panel
	
		window_width = self.search_window.winfo_screenwidth()
		window_height = self.search_window.winfo_screenheight()
		style = ttk.Style()		
		
		if window_width > 1200:
			style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 10)) # Modify the font of the body
			style.configure('Treeview', rowheight=20)
		else:
			style.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 8)) # Modify the font of the body
			style.configure('Treeview', rowheight=14)

		# Create Tree
		self.search_tree = ttk.Treeview(self.pane_one,height=int(window_height),selectmode='browse',show='tree',style="Treeview")

		# Create Tree Layout
		self.search_tree.column("#0", width=int(window_width/2), stretch=1)		

		# Alphabetise search
		alpha_search = []
		for item,dictionary in self.taxonomy.items():
			alpha_search.append(dictionary['iid'])
		alpha_search = sorted(alpha_search)
		
		# Go through search alphabetically and build branches
		for taxon in alpha_search:
			self.iid_iterator(self.taxonomy,taxon,self.taxon_branch_builder)
			
		# Display Tree
		self.search_tree.pack(anchor="w")
		self.search_tree.bind('<Button-1>', self.taxon_informer)
		
		self.search_tree.update()
        
	########################
	#         Main         #
	########################	
		
	def search_viewer(self,window):
	# Displays the search Panels

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
			self.pane_three.destroy()
		except (NameError, AttributeError):
			pass

		###################
		# search Window #
		###################

		# Setup search Window
		self.search_window = window

		# Setup search Window Panels
		self.pane_one = ttk.Frame(self.search_window)
		self.pane_two = ttk.Frame(self.search_window)
		self.pane_one.place(y=15, relwidth=.20, relheight=.85)
		self.pane_two.place(y=15, relx=.25, relwidth=.74, relheight=.4)

		#menubar.add_command(label="Add New Root", command=self.root_adder)

		# Set Up Annotation Selection (Tree) Panel 
		
		self.taxon_tree_displayer()
