from database_maintenance import *

# Import External Libraries
from pathlib import Path

# Import TKinter Libraries
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import scrolledtext

class metadata_display(database_maintenance):
	
	def database_metadata_viewer(self):
	
		###################
		# Metadata Window #
		###################

		# Setup Metadata Window
		self.metadata_window = Toplevel()
		self.metadata_window.title('Database Metadata')
		self.metadata_window.minsize(600,0)
		
		# Place Icon
		# "Writing" by IQON from the Noun Project
		self.metadata_window.iconbitmap('icon.ico')
		
