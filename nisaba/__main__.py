# Import Classes
try:
	# Used when executing with Python
	from database_display import *
	from taxonomy_display import *
	from configuration_display import *
	from search_display import *
	
except ModuleNotFoundError:
	# Used when calling as library
	from nisaba.database_display import *
	from nisaba.taxonomy_display import *
	from nisaba.configuration_display import *
	from nisaba.search_display import *

# Import TKinter Libraries
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import scrolledtext

def main():

		####################
		# Option Functions #
		####################

		def option_switcher(switch):
		
			# Delete Any Existing Information
			try:
				main_pane_viewer.destroy()
			except (NameError, AttributeError):
				pass
				
			main_pane_viewer = ttk.Frame(main_window)
			main_pane_viewer.place(relx=.1, relwidth=.9, relheight=1)
			
			if switch == 'd': 
				database_window = database_display()				
				database_window.database_window_viewer(main_pane_viewer)
			elif switch == 't': 
				taxonomy_window = taxonomy_display()
				taxonomy_window.taxonomy_viewer(main_pane_viewer,False)
			elif switch == 's':
				search_window = search_display()
				search_window.search_viewer(main_pane_viewer)
			elif switch == 'c':
				configuration_window = configuration_display()
				configuration_window.configuration_viewer(main_pane_viewer) 
			elif switch == 'g':
				git_window = configuration_display()
				git_window.git_push_automation() 
		
		#######################
		# Setup Key Variables #
		#######################
		
		# Set asset path
		assets_path = os.path.join(os.path.dirname(__file__), "assets/")
	
		################
		# Setup Window #
		################

		# Setup Taxonomy Window
		main_window = Tk()
		main_window.title('Nisaba: Multi-Modal Annotation v.0.3.19')
		
		# Place Icon
		# "Writing" by IQON from the Noun Project
		if (sys.platform.startswith('win') or sys.platform.startswith('darwin')):
			main_window.iconbitmap(Path(assets_path) / 'icon.ico')
		else:
			logo = PhotoImage(file=Path(assets_path) / 'icon.gif')
			main_window.call('wm', 'iconphoto', main_window._w, logo)
			
		# Set to Full Screen
		try:
			main_window.state('zoomed')
		except (TclError):
			pass
			m = main_window.maxsize()
			main_window.geometry('{}x{}+0+0'.format(*m))

		# Determine Window Size / Screen Resolution 
		window_width = main_window.winfo_screenwidth()
		window_height = main_window.winfo_screenheight()

		# Setup Window Panels 
		main_pane_menu = ttk.Frame(main_window)
		main_pane_viewer = ttk.Frame(main_window)
		
		# Setup Fixed Panels
		main_pane_menu.place(relwidth=.1, relheight=1)
		main_pane_viewer.place(relx=.1, relwidth=.9, relheight=1)
		
		# Add Icons to Options
		# Left Menu Icons made by Freepik (https://www.flaticon.com/authors/freepik) from https://www.flaticon.com/ CC-BY (http://creativecommons.org/licenses/by/3.0/)
		database_logo=PhotoImage(file=Path(assets_path) / 'database.png')
		taxonomy_logo=PhotoImage(file=Path(assets_path) / 'taxonomy.png')
		search_logo=PhotoImage(file=Path(assets_path) / 'search.png')
		configuration_logo=PhotoImage(file=Path(assets_path) / 'configuration.png')
		git_logo=PhotoImage(file=Path(assets_path) / 'gist.png')
		
		# Setup Menu Options
		edit_configuration = Button(main_pane_menu,text='Configuration', image=configuration_logo, compound="top", command=(lambda: option_switcher('c')))
		edit_database = Button(main_pane_menu,text='Database', image=database_logo, compound="top", command=(lambda: option_switcher('d')))
		edit_vocabulary = Button(main_pane_menu,text='Taxonomy', image=taxonomy_logo, compound="top", command=(lambda: option_switcher('t')))
		search_database = Button(main_pane_menu,text='Browse', image=search_logo, compound="top", command=(lambda: option_switcher('s')))
		git_database = Button(main_pane_menu,text='Git Push', image=git_logo, compound="top", command=(lambda: option_switcher('g')))
		
		# Display Menu Options
		edit_configuration.place(relx=0.5, rely=0.15, anchor=CENTER)
		edit_database.place(relx=0.5, rely=0.3, anchor=CENTER)
		edit_vocabulary.place(relx=0.5, rely=0.45, anchor=CENTER)
		search_database.place(relx=0.5, rely=0.6, anchor=CENTER)
		git_database.place(relx=0.5, rely=0.75, anchor=CENTER)
		
		style = ttk.Style()
		style.configure('TButton')
		style.theme_use('clam')
		
		main_window.mainloop()


if __name__ == "__main__":
	main()
