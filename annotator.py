#!/usr/bin/python3

import os
import json
import urllib # api python 
from urllib import parse, request

#Load data and extract content

path_data = []
for root, dirs, files in os.walk('kaggle/document_parses/'): 
    for file in files:
        path_data.append(os.path.join(root,file))

#Extract content of the all records. load into data_dictionari
data_dict = {'paper_idx':[], 'paper_id':[],'title':[],
             'content_to_annotate':[], 'document_text':[],
             'bioportal_anotations':[]}

idx = 0
for path in path_data:
    
    with open(path, 'r') as json_data:
        data = json.load(json_data)
        
    
    try:              #for pdf_json
        content_abstract = ''
        for paragraph in data['abstract']:
            content_abstract += ' ' + paragraph['text']
            
        
        content_body = ''
        for paragraph in data['body_text']:
            content_body += ' ' + paragraph['text']
        
        document_text = data['metadata']['title'] + content_abstract + content_body 
        
        content_to_annotate = data['metadata']['title'] + ' ' + content_abstract

                    
    except KeyError:    # for pmc_json
        
        content_to_annotate= data['metadata']['title'] + ' ' + data['body_text'][0]['text']
        content_body = ''
        for paragraph in data['body_text']:
            content_body += ' ' + paragraph['text']

        document_text = data['metadata']['title'] + content_body
    
    data_dict['paper_idx'].append(idx)
    data_dict['paper_id'].append(data['paper_id'])        
    data_dict['title'].append(data['metadata']['title'])
    data_dict['content_to_annotate'].append(content_to_annotate)
    data_dict['document_text'].append(document_text)
    idx += 1

#API CONNECTION
#url params

REST_URL = "http://data.bioontology.org"
API_KEY = " "	

ontologies = 'NHC,MESH,COVID-19,HPIO,SNOMEDCT,OCHV,PREMEDONTO,NCIT,CIDO,VO,IOBC,TheCOVID-19InfectiousDiseaseOntology,BAO,COVID19,MEDDRA,COVIDCRFRAPID,EFO'

#Api calls
for i in data_dict['paper_idx']:                     #data_dict['paper_idx']:

    text = parse.quote(data_dict['content_to_annotate'][i])
    url = REST_URL + "/annotator/?apikey=" + API_KEY + '&' + ontologies + '&' + 'text=' + text

    #call api
    api_call = request.urlopen(url)
    annotations = json.loads(api_call.read().decode('utf-8'))
    
    #store anotations
    data_dict['bioportal_anotations'].append(annotations)

#store data in disk
with open('paper_annotated.json','w') as outfile:
    json.dump(data_dict, outfile)
