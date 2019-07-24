from  database_maintenance import *

# Import External Libraries
import csv
from pathlib import Path
import PIL.Image
import PIL.ImageTk

# Import TKinter Libraries
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import scrolledtext

class taxonomy_display(database_maintenance):
    
    def half_pane_at_seventy_percent(self):
        screen_width = self.taxonomy_window.winfo_screenwidth()
        pane_width = int(0.3*screen_width)

        return pane_width

    def center_window_at_seventy_percent(self):
        screen_width = self.taxonomy_window.winfo_screenwidth()
        screen_height = self.taxonomy_window.winfo_screenheight()
        seventy_percent_width = str(int(0.8*screen_width))
        seventy_percent_height = str(int(0.6*screen_height))
        fifteen_percent_width = str(int(0.1*screen_width))
        fifteen_percent_height = str(int(0.2*screen_height))
        geometry_information = "{0}x{1}+{2}+{3}".format(seventy_percent_width,seventy_percent_height,fifteen_percent_width,fifteen_percent_height)
        
        return geometry_information    

    def displayEditor(self):

        # Delete Any Existing Information
        try:
            self.taxonomy_pane2.destroy()
        except (NameError, AttributeError):
            pass
            
        self.taxonomy_pane2 = ttk.Frame(self.taxonomy_panel_control)
        self.taxonomy_panel_control.add(self.taxonomy_pane2)
    
        self.taxonomy_iid_label =  Label(self.taxonomy_pane2, text="ID: ", anchor='w')
        self.taxonomy_annotation_label =  Label(self.taxonomy_pane2, text="Name: ", anchor='w')
        self.taxonomy_type_label =  Label(self.taxonomy_pane2, text="Type: ", anchor='w')
        self.taxonomy_detail_label =  Label(self.taxonomy_pane2, text="Definition: ", anchor='w')
        self.taxonomy_iid_entry = Entry(self.taxonomy_pane2, width = 100)
        self.taxonomy_annotation_entry = Entry(self.taxonomy_pane2, width = 100)
        self.taxonomy_type_entry = Entry(self.taxonomy_pane2, width = 100)
        self.taxonomy_detail_entry = Entry(self.taxonomy_pane2, width = 100)    

        self.taxonomy_iid_label.grid(column=0,row=0)
        self.taxonomy_annotation_label.grid(column=0,row=1)
        self.taxonomy_type_label.grid(column=0,row=2)
        self.taxonomy_detail_label.grid(column=0,row=3)
        self.taxonomy_iid_entry.grid(column=1,row=0)
        self.taxonomy_annotation_entry.grid(column=1,row=1)
        self.taxonomy_type_entry.grid(column=1,row=2)
        self.taxonomy_detail_entry.grid(column=1,row=3)

        self.save_button = Button(self.taxonomy_pane2, text='Save', command=self.save_taxonomy)
        self.save_button.grid(column = 0, row = 5, sticky=W, padx =10, pady = 10)


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
        self.taxonomy_window.state = 'zoomed'
        
        # Setup Window Menu
        menubar = Menu(self.taxonomy_window)
        addMenu = Menu(menubar, tearoff=False)
        addItemMenu = Menu(addMenu, tearoff=False)
        self.taxonomy_window.config(menu=menubar)
        #menubar.add_command(label="Load New Taxonomy", command=pass)
        #menubar.add_command(label="Refresh", command=pass)

        # Setup Paned Windows
        self.taxonomy_panel_control = ttk.Panedwindow(self.taxonomy_window, orient=HORIZONTAL)
        self.taxonomy_pane1 = ttk.Frame(self.taxonomy_panel_control)
        self.taxonomy_panel_control.add(self.taxonomy_pane1)

        # Pack Panes into Frame
        self.taxonomy_panel_control.pack(expand=1, fill='both')

        #####################################
        # Set Up Definition Selection Panel #
        #####################################
    
        # Get Sizes
        pane_width = self.half_pane_at_seventy_percent()
        
        # Create Tree Structure
        self.taxonomy_tree = ttk.Treeview(self.taxonomy_pane1,height="26",selectmode='browse')

        self.taxonomy_tree["columns"]=("one","two","three")
        self.taxonomy_tree.column("#0", minwidth=int(pane_width/6*1), stretch=1)
        self.taxonomy_tree.column("one", minwidth=int(pane_width/6*1), stretch=1)
        self.taxonomy_tree.column("two", minwidth=int(pane_width/6*2), stretch=1)
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
                    d[x+1]=self.taxonomy_tree.insert(parent_branch, "end", new_dictionary['iid'], text=new_dictionary['name'],values=(new_dictionary['type'],new_dictionary['definition']))
                
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

