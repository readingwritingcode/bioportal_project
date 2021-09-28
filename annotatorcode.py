# bioportal
import json
import requests
import urllib
from urllib import parse, request

REST_URL = "http://data.bioontology.org"
API_KEY = '3b00793b-f3cc-489c-9d6e-7a888f4b656e'

def make_url_query(text_to_annotate):
    global URL 
    URL = REST_URL + "/annotator/?text=%s"%(parse.quote(text_to_annotate))
    return URL

def get_json(url):
    opener = urllib.request.build_opener()
    opener.addheaders = [('Authorization', 'apikey token=' + API_KEY)]
    return json.loads(opener.open(url).read())

def call_endpoint_annotator(URL, PARAMS):
    r = requests.get(url = URL, params = PARAMS)
    global json_api_results
    json_api_results = r.json()
    return json_api_results

def store_annotations(annotations,get_class=True):
    anns = []
    for result in annotations:
        ann = {}
        class_details = result["annotatedClass"]
        if get_class:
            try:
                class_details = get_json(result["annotatedClass"]["links"]["self"])
            except urllib.error.HTTPError:
                print(f"Error retrieving {result['annotatedClass']['@id']}")
                continue
        ann['id'] = class_details["@id"]
        ann['preflabel'] = class_details["prefLabel"]
        ann['ontology'] = class_details["links"]["ontology"]
        ann['annotation_details'] =  []
        for annotation in result['annotations']:
            ann['annotation_details'].append(
                {
                    'from': str(annotation["from"]),
                    'to': str(annotation["to"]),
                    'match_type': annotation["matchType"]
                })
        if result["hierarchy"]:
            ann['hierarchy'] = []
            for annotation in result["hierarchy"]:
                try:
                    class_details = get_json(annotation["annotatedClass"]["links"]["self"])
                except urllib.error.HTTPError:
                    print(f"Error retrieving {annotation['annotatedClass']['@id']}")
                    continue
                ann['hierarchy'].append(
                    {
                     'id':class_details["@id"],
                     'preflabel':class_details["prefLabel"],
                     'ontology':class_details["links"]["ontology"],
                     'distance_from_original_class':str(annotation["distance"])
                    })
        anns.append(ann)
    return anns

def get_annotations(text_to_annotate,ontologies,expand_class_hierarchy='false',class_hierarchy_max_level=0):
    
    PARAMS = {'apikey':API_KEY,'ontologies':ontologies,
              'expand_class_hierarchy':expand_class_hierarchy,
              'class_hierarchy_max_level':0,
              'longest_only':'true'
             }
    make_url_query(text_to_annotate)
    call_endpoint_annotator(URL,PARAMS)
    return store_annotations(json_api_results)
