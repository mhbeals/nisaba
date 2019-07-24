# Import External Libaries
import json
import datetime
from pathlib import Path
from tkinter import END
from tkinter.filedialog import askopenfilename
from rdflib import Graph, URIRef, Namespace, RDF, RDFS, Literal
import urllib.parse

class database_maintenance:

    def __init__(self):

        with open (Path("databases/") / "database.json", 'r') as file:
            loaddata = file.read()

        self.database = json.loads(loaddata)

        # Load RDF database
        self.database_rdf = Graph()

        with open (Path("databases/") / "taxonomy.json", 'r') as file:
            loaddata = file.read()

        self.taxonomy = json.loads(loaddata)

    def save_database(self):
        # convert database to json and place in a variable
        savedata = json.dumps(self.database, indent=4)

        #save variable to 'most recent' file
        with open (Path("databases/") / "database.json", 'w') as file:
            file.write(savedata)

        #create a filename based on the time
        filename = 'database_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.json'


        #save backup
        with open (Path("databases/") / filename, 'w') as file:
            file.write(savedata)

        # map the saved JSON into RDF
        self.rdf_mapper()

        return

    def rdf_mapper(self):

        # Load previous triples, if any
        self.database_rdf.parse("databases/database.ttl", format='turtle')

        nisaba_vocab_uri = URIRef('http://purl.org/nisaba/vocab#')
        nisaba_resource_uri = URIRef('http://purl.org/nisaba/')
        nisaba_collection_uri = URIRef('http://purl.org/nisaba/collection/')
        nisaba_v = Namespace(nisaba_vocab_uri)
        nisaba_r = Namespace(nisaba_resource_uri)
        nisaba_c = Namespace(nisaba_collection_uri)

        for c,v in self.database.items():
            collection_uri = nisaba_c[c]
            self.database_rdf.add(( collection_uri, RDF.type, nisaba_v['CollectionEntry']))
            if 'collection_title' in v:
                self.database_rdf.add(( collection_uri, nisaba_v['collection_title'], Literal(v['collection_title']) ))
            if 'collection_date' in v:
                self.database_rdf.add(( collection_uri, nisaba_v['collection_date'], Literal(v['collection_date']) ))
            if 'collection_holder' in v:
                self.database_rdf.add(( collection_uri, nisaba_v['collection_holder'], Literal(v['collection_holder']) ))
            if 'collection_holder_reference' in v:
                self.database_rdf.add(( collection_uri, nisaba_v['collection_holder_reference'], Literal(v['collection_holder_reference']) ))
            if 'collection_holder_original' in v:
                self.database_rdf.add(( collection_uri, nisaba_v['collection_holder_original'], Literal(v['collection_holder_original']) ))
            if 'collection_holder_reference_original' in v:
                self.database_rdf.add(( collection_uri, nisaba_v['collection_holder_reference_original'], Literal(v['collection_holder_reference_original']) ))
            if 'collection_place_of_publication' in v:
                self.database_rdf.add(( collection_uri, nisaba_v['collection_place_of_publication'], Literal(v['collection_place_of_publication']) ))
            if 'collection_author' in v:
                self.database_rdf.add(( collection_uri, nisaba_v['collection_author'], Literal(v['collection_author']) ))

            if 'items' in self.database[c]:
                for i,v in self.database[c]['items'].items():
                    item_uri = URIRef(nisaba_c[c] + '/item/' + i)
                    self.database_rdf.add(( collection_uri, nisaba_v['hasItem'], item_uri ))
                    self.database_rdf.add(( item_uri, RDF.type, nisaba_v['ItemEntry']))
                    if 'item_type' in v:
                        self.database_rdf.add(( item_uri, nisaba_v['item_type'], Literal(v['item_type']) ))
                    if 'item_title' in v:
                        self.database_rdf.add(( item_uri, nisaba_v['item_title'], Literal(v['item_title']) ))
                    if 'image_file' in v:
                        self.database_rdf.add(( item_uri, nisaba_v['image_file'], Literal(v['image_file']) ))
                    if 'item_author' in v:
                        self.database_rdf.add(( item_uri, nisaba_v['item_author'], Literal(v['item_author']) ))
                    if 'item_date' in v:
                        self.database_rdf.add(( item_uri, nisaba_v['item_date'], Literal(v['item_date']) ))
                    if 'item_page_number' in v:
                        self.database_rdf.add(( item_uri, nisaba_v['item_page_number'], Literal(v['item_page_number']) ))
                    if 'item_document_number' in v:
                        self.database_rdf.add(( item_uri, nisaba_v['item_document_number'], Literal(v['item_document_number']) ))
                    if 'transcription' in v:
                        self.database_rdf.add(( item_uri, nisaba_v['transcription'], Literal(v['transcription']) ))
                    if 'annotations' in v:
                        for a in v['annotations']:
                            self.database_rdf.add(( item_uri, nisaba_v['hasAnnotation'], Literal(a) ))
                    if 'segments' in v:
                        for s,v in self.database[c]['items'][i]['segments'].items():
                            segment_uri = URIRef(item_uri + '/segment/' + s)
                            self.database_rdf.add(( item_uri, nisaba_v['hasSegment'], segment_uri ))
                            self.database_rdf.add(( segment_uri, RDF.type, nisaba_v['SegmentEntry']))
                            if 'start' in v:
                                self.database_rdf.add(( segment_uri, nisaba_v['start'], Literal(v['start']) ))
                            if 'end' in v:
                                self.database_rdf.add(( segment_uri, nisaba_v['end'], Literal(v['end']) ))
                            if 'top' in v:
                                self.database_rdf.add(( segment_uri, nisaba_v['top'], Literal(v['top']) ))
                            if 'bottom' in v:
                                self.database_rdf.add(( segment_uri, nisaba_v['bottom'], Literal(v['bottom']) ))
                            if 'left' in v:
                                self.database_rdf.add(( segment_uri, nisaba_v['left'], Literal(v['left']) ))
                            if 'right' in v:
                                self.database_rdf.add(( segment_uri, nisaba_v['right'], Literal(v['right']) ))
                            if 'segment_notes' in v:
                                self.database_rdf.add(( segment_uri, nisaba_v['segment_notes'], Literal(v['segment_notes']) ))
                            if 'annotations' in v:
                                for a in v['annotations']:
                                    self.database_rdf.add(( segment_uri, nisaba_v['hasAnnotation'], Literal(a) ))


        self.database_rdf.bind('nisaba', nisaba_v)

        # id RDF version
        filename_rdf = 'database_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.ttl'
        with open(Path("databases/") / filename_rdf, 'wb') as file:
            print('Writing {} triples to Turtle file'.format(len(self.database_rdf)))
            file.write(self.database_rdf.serialize(format='turtle'))


    def save_entries(self, level):
        # Save entries
        for entry in self.collection_entries:
            self.database[self.collection_index][entry[0]] = entry[1].get()

            # self.collection_uri = self.nisaba_c[urllib.parse.quote(entry[1].get())]
            # self.database_rdf.add(( self.collection_uri, RDF.type, self.nisaba_v['CollectionEntry']))
            # self.database_rdf.add(( self.collection_uri, RDFS.label, Literal(entry[1].get()) ))

        if level == 'i':
            annotations_list = self.database[self.collection_index]['items'][self.item_index].get('annotations',[])
            for item in self.item_tree.selection():
                annotations_list.append(item)
            self.database[self.collection_index]['items'][self.item_index]['annotations'] = annotations_list

            # self.item_uri = URIRef(self.collection_uri + '/item/' + self.item_index)
            # self.database_rdf.add(( self.collection_uri, self.nisaba_v['hasItem'], self.item_uri ))
            # self.database_rdf.add(( self.item_uri, RDF.type, self.nisaba_v['ItemEntry'] ))
            # for a in annotations_list:
            #     self.database_rdf.add(( self.item_uri, self.nisaba_v['hasAnnotation'], Literal(a) ))

            if self.database[self.collection_index]['items'][self.item_index]['item_type'] == 't':
                self.database[self.collection_index]['items'][self.item_index]['transcription'] = self.transcription_text.get("1.0",END)

                # self.database_rdf.add(( self.item_uri, self.nisaba_v['hasTranscription'], Literal(self.transcription_text.get("1.0",END)) ))

            elif self.database[self.collection_index]['items'][self.item_index]['item_type'] == 'i':
                self.database[self.collection_index]['items'][self.item_index]['image_file'] = self.image_filename.get()

                # self.database_rdf.add(( self.item_uri, self.nisaba_v['hasImage'], Literal(self.image_filename.get()) ))

				
        if level == 'i' or level == 's':
            for entry in self.item_entries:
                self.database[self.collection_index]['items'][self.item_index][entry[0]] = entry[1].get()

                # self.database_rdf.add(( item_uri, RDFS.label, entry[1].get() ))

        if level == 's':

            # self.segment_uri = URIRef(self.item_uri + '/segment/' + self.segment_index)
            # self.database_rdf.add(( self.item_uri, self.nisaba_v['hasSegment'], self.segment_uri ))
            # self.database_rdf.add(( self.segment_uri, RDF.type, self.nisaba_v['SegmentEntry'] ))

            for entry in self.segment_entries:
                self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index][entry[0]] = entry[1].get()

                # self.database_rdf.add(( self.segment_uri, RDFS.label, Literal(entry[1].get()) ))

            if self.database[self.collection_index]['items'][self.item_index]['item_type'] == 't':
                self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['start'] = int(self.start_text.get())
                self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['end'] = int(self.end_text.get())

                # self.database_rdf.add(( self.segment_uri, self.nisaba_v['start'], Literal(int(self.start_text.get())) ))
                # self.database_rdf.add(( self.segment_uri, self.nisaba_v['end'], Literal(int(self.end_text.get())) ))

            elif self.database[self.collection_index]['items'][self.item_index]['item_type'] == 'i':
                self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['top'] = int(self.top_text.get())
                self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['bottom'] = int(self.bottom_text.get())
                self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['right'] = int(self.right_text.get())
                self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['left'] = int(self.left_text.get())

                # self.database_rdf.add(( self.segment_uri, self.nisaba_v['top'], Literal(int(self.top_text.get())) ))
                # self.database_rdf.add(( self.segment_uri, self.nisaba_v['bottom'], Literal(int(self.bottom_text.get())) ))
                # self.database_rdf.add(( self.segment_uri, self.nisaba_v['right'], Literal(int(self.right_text.get())) ))
                # self.database_rdf.add(( self.segment_uri, self.nisaba_v['left'], Literal(int(self.left_text.get())) ))

            annotations_list = self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index].get('annotations',[])
            for item in self.segment_tree.selection():
                annotations_list.append(item)
            self.database[self.collection_index]['items'][self.item_index]['segments'][self.segment_index]['annotations'] = annotations_list

            # add segment annotations to RDF graph too
            # for a in annotations_list:
            #     self.database_rdf.add(( self.segment_uri, self.nisaba_v['hasAnnotation'], Literal(a) ))

        self.save_database()

    def load_database(self):

        # Load Database
        self.collection_selection_window.destroy()
        file = askopenfilename(initialdir = "databases/",title = "Select Database",filetypes = (("json files","*.json"),("all files","*.*")))
        with open (file, 'r') as file:
            loaddata = file.read()
        self.database = json.loads(loaddata)
        self.collection_selector()

    def save_taxonomy(self):
        # Save Taxon Definitions

        def iid_finder(dictionary):

            for ckey,cvalue in dictionary.items():
                print(self.clicked_item,cvalue['iid'])
                if cvalue['iid'] == self.clicked_item:
                    cvalue['iid'] = self.taxonomy_iid_entry.get()
                    cvalue['name'] = self.taxonomy_annotation_entry.get()
                    cvalue['type'] = self.taxonomy_type_entry.get()
                    cvalue['definition'] = self.taxonomy_detail_entry.get()
                    break
                else:
                    iid_finder(cvalue['children'])

        iid_finder(self.taxonomy)

        # convert database to json and place in a variable
        savedata = json.dumps(self.taxonomy, indent=4)

        #save variable to 'most recent' file
        with open (Path("databases/") / "taxonomy.json", 'w') as file:
            file.write(savedata)

        return
