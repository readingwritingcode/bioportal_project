### 
#IMPORTS

import os
import sys
import json
import pandas
import urllib
import requests
from urllib import parse, request

#VARIABLES

REST_URL = "http://data.bioontology.org"
API_KEY = '3b00793b-f3cc-489c-9d6e-7a888f4b656e'
PATH_TO_PAPERS = 'data/kaggle/'
PATH_TO_ONTS_SELECT = 'data/onts_select.csv'



#FUNCTIONS

def parse_directory():
    '''For parse and join paths in PATH_TO_PAPERS.
       Output:path_files: list with all paths to record 
    '''
    global path_files
    path_files = []

    for root, dirs, files in os.walk(PATH_TO_PAPERS):
        for file in files:
            path_files.append(os.path.join(root, file))

    return path_files

def get_metadata_record(path_to_record):
    '''Get dict keys from JSON-PAPER data structure.
       Input:path_to_json record.
       Output: record.keys.
    '''
    with open(path_to_record,'r') as json_handler:
        record=json.load(json_handler)
    return record.keys()

def load_json_record(path_to_record):
    ''' Load entire json record for a paper.
        Input: path to record.
        Output: json_record.
    '''
    global json_record
    with open(path_to_record, 'r') as json_handler:
        json_record = json.load(json_handler)
    return json_record

def load_select_onts():
    ''' For reading and proccess ontologies selected file in PATH_TO_ONTS_SELECT.
        Output: select_onts.
    '''
    #proces file.
    ont_sel = pandas.read_csv(PATH_TO_ONTS_SELECT)
    list_onto = [x.replace('\t','').replace(' ','').replace('\n','') for x in list(ont_sel['Ontology'].values)if type(x)!=float]
    #
    global select_onts
    select_onts= []
    for i in list_onto:
        if i not in select_onts:
            select_onts.append(i)
        else:
            next
            
    return select_onts

def get_json(url):
    
    '''
    General util: call some bioportal endpoint.
    Header Auth method.
    Input:general url bioportal.
    Output: json response fo a general urls requests.
    
    '''
    
    opener = urllib.request.build_opener()
    opener.addheaders = [('Authorization', 'apikey token=' + API_KEY)] 
    return json.loads(opener.open(url).read())

def load_bio_onts():
    '''Use bioportal endPoint to retrive all Bioportal Onts'''
    
    resources = get_json(REST_URL + "/")                    # call to retrieve json
    ontologies = get_json(resources["links"]["ontologies"]) # call again for especific fiels of json response
    
    global bio_onts
    bio_onts = []
    for ontology in ontologies:
        bio_onts.append(f"{ontology['name']}\n{ontology['@id']}\n")
        
    return bio_onts    

def onts():
    '''
       Merge select_onts and bio_onts,
       for  build later string-url-params that cotain only ontlogies
       selected and existing in bioportal.
       Output: ontologies url query parameter 
    '''
    
    select_onts = load_select_onts() # call other function
    bio_onts = load_bio_onts()       # call function
      
    #build an string characteres that contain a unique words: each word is a 
    # ontologie selected and existing in bio.
    global ontologies
    ontologies = '' 
    
    for ontosel in select_onts:          
        for ontobio in bio_onts:
            if ontobio.find(ontosel) > 1:          # bugOne: the word MESH make match twice and twice is append,
                if ontologies.find(ontosel) < 1:   # but they should be appended only once. i don't catch .
                    ontologies += ontosel +' '     # the reason of this.
                else:
                    pass
    ontologies = ontologies[:-1].replace(' ',',')
    
    return ontologies

def str_list_onts(ontologie_list):
    '''General util.
       make methamorfosis from list to string-of-elements
       Input:ontologies_list
       Output: ontologies url query parameter
    '''
    global ontologies
    ontologies = ""
    for ont in ontologie_list:
        ontologies += ','+ ont
    return ontologies[1:]

'''
#### nota: Es necesario estandarizar el archivo onts_select.csv: 
- se deben registrar las siglas oficiales de cada ontologia registrada. 
- se deben incluir ontologias que existan en bioportal.


para el caso de "TheCOVID-19InfectiousDiseaseOntology" la sigla oficias es IDO-COVID19. vease: https://bioportal.bioontology.org/ontologies/IDO-COVID-19

para el caso de: "NHC" no se encuentra en bioportal ontologias. vease: 
https://bioportal.bioontology.org/ontologies
'''

def make_url_query(text_to_annotate):
    '''return URL'''
    global URL 
    URL = REST_URL + "/annotator/?text=%s"%(parse.quote(text_to_annotate))
    return URL

#Call api V.2
def call_endpoint_annotator(URL, PARAMS):
    r = requests.get(url = URL, params = PARAMS)
    global json_api_results
    json_api_results = r.json()
    return json_api_results

### 
#CLASS

class dbMain:
    
    '''this class store data for tree schemas.
    s1: item collection.
    s2:chunks of paper
    s2:annotations for each chunk.
    contain methods for update schemas an store db main.
    Methods:
    annotations['matchTerm'].append(matchTerm)
    annotations['ontology'].append(ontology)
    annotations['annotatedClass'].append(annotatedClass)
    chunks['text'].append(text_to_annotate)
    chunks['sections'].append(section_text_to_annotated)
    chunks['chunks_paper'].append(annotations)
    collection['chunks_paper'].append(chunks)
    collection['paper_id'] += paper_id
    db.append(item_collection).
    '''
    
    db = [] # list of items_collections

    def __init__(self):

        self.item_collection = {
                                'paper_id':'',
                                'chunks_paper':[]
                                  }
        
        self.chunks = {
                        'texts':[],
                        'sections':[],
                        'annotations':[]
                        }

        self.annotations = {
                            'matchTerm':[],
                            'ontology':[],
                            'annotatedClass':[]
                            }

    #methods
    def restart_annotations(self):
        self.annotations = {
                            'matchTerm':[],
                            'ontology':[],
                            'annotatedClass':[]
                            }
    def update_annotations(self,matchTerm,
                                ontology,
                                annotatedClass):
        self.annotations['matchTerm'].append(matchTerm)
        self.annotations['ontology'].append(ontology)
        self.annotations['annotatedClass'].append(annotatedClass)
    
    def update_chunks(self,text,section,annotations):
        self.chunks['texts'].append(text)
        self.chunks['sections'].append(section)
        self.chunks['annotations'].append(annotations)

    def update_item_collection(self,paper_id,chunks_paper):
        self.item_collection['paper_id'] += paper_id
        self.item_collection['chunks_paper'].append(chunks_paper)
        
    def update_db_main(self):
        dbMain.db.append(self.item_collection)
        
    def store_db_main(self):
        
        with open('annotationsDBlist.json','w') as json_file:
            json_file.write(json.dumps(dbMain().db))

#MAIN CODE

ontologies = "MESH,COVID-19,HPIO,SNOMEDCT,OCHV,PREMEDONTO,NCIT,CIDO,VO,IOBC,BAO,COVID19,MEDDRA,COVIDCRFRAPID,EFO,CODO"

PARAMS = {'apikey':API_KEY,'ontologies':ontologies,
          'expand_class_hierarchy':'false','class_hierarchy_max_level':0,
           'longest_only':'true'
         }

#parse_directory()

parse_directory()

for idx, path in enumerate(path_files):
    
    load_json_record(path)
    emty_sections = []
    item = dbMain()
        
    try: 
        
        for idx, _chunk in enumerate(json_record['abstract']):

            #make url here
            text_to_annotate = _chunk['text']
            print(text_to_annotate)

            if text_to_annotate:
                make_url_query(text_to_annotate)
                print(URL)

                #call api here
                call_endpoint_annotator(URL,PARAMS)
                #init db schema annotations
                item.restart_annotations()

                #proccess and store resultsfor section here
                for i in range(len(json_api_results)):
                    item.update_annotations(json_api_results[i]['annotations'][0]['text'],
                                            json_api_results[i]['annotatedClass']['links']['ontology'],
                                            json_api_results[i]['annotatedClass']['@id']
                                           )
                print(item.annotations)
                item.update_chunks(_chunk['text'],
                                   _chunk['section'],
                                   item.annotations
                                  )
    
            else:
                emty_sections.append(idx)

        print('ok abstract')
        #Init api params

        for idx, _chunk in enumerate(json_record['body_text']):

            #make url here
            text_to_annotate = _chunk['text']
            print(text_to_annotate)

            if text_to_annotate:
                make_url_query(text_to_annotate)
                print(URL)

                #call api here
                call_endpoint_annotator(URL,PARAMS)
                #init schema annotations
                item.restart_annotations()

                #proccess and store resultsfor section here
                for i in range(len(json_api_results)):
                    item.update_annotations(json_api_results[i]['annotations'][0]['text'],
                                            json_api_results[i]['annotatedClass']['links']['ontology'],
                                            json_api_results[i]['annotatedClass']['@id']
                                           )
                item.update_chunks(_chunk['text'],
                                   _chunk['section'],
                                   item.annotations
                                  )
            else:
                emty_sections.append(idx)
                
    except KeyError:

        for idx, _chunk in enumerate(json_record['body_text']):

            #make url here
            text_to_annotate = _chunk['text']
            print(text_to_annotate)

            if text_to_annotate:
                make_url_query(text_to_annotate)
                print(URL)

                #call api here
                call_endpoint_annotator(URL,PARAMS)
                #init schema annotations
                item.restart_annotations()
                #proccess and store resultsfor section here
                for i in range(len(json_api_results)):
                    item.update_annotations(json_api_results[i]['annotations'][0]['text'],
                                            json_api_results[i]['annotatedClass']['links']['ontology'],
                                            json_api_results[i]['annotatedClass']['@id']

                                           )
                item.update_chunks(_chunk['text'],
                                   _chunk['section'],
                                   item.annotations
                                  )
            else:
                emty_sections.append(idx)

    finally:
        #for title
        text_to_annotate = json_record['metadata']['title']
        
        if text_to_annotate:
            make_url_query(text_to_annotate)
            print(URL)

            #call api here
            call_endpoint_annotator(URL,PARAMS)
            #init schema annotations
            
            item.restart_annotations()
            #proccess and store resultsfor section here
            for i in range(len(json_api_results)):
                item.update_annotations(json_api_results[i]['annotations'][0]['text'],
                                        json_api_results[i]['annotatedClass']['links']['ontology'],
                                        json_api_results[i]['annotatedClass']['@id']

                                           )
            item.update_chunks(_chunk['text'],
                                   _chunk['section'],
                                   item.annotations
                                  )
        item.update_item_collection(json_record['paper_id'], item.chunks)
        print('paper index:',idx,'processed')
        item.update_db_main()
item.store_db_main()
