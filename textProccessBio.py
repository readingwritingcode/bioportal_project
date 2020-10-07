# %load parsedir.py
#!/usr/bin/python3

def parse_directory(PATH_TO_PAPERS):
    '''For parse and join paths in PATH_TO_PAPERS.
       Output:path_files: list with all paths to record 
    '''
    global path_files
    path_files = []

    for root, dirs, files in os.walk(PATH_TO_PAPERS):
        for file in files:
            path_files.append(os.path.join(root, file))

    return path_files

# %load getMetadataRecord.py
def get_metadata_record(path_to_record):
    '''Get dict keys from JSON-PAPER data structure.
       Input:path_to_json record.
       Output: record.keys.
    '''
    with open(path_to_record,'r') as json_handler:
        record=json.load(json_handler)
        
    return record.keys()

# %load loadJsonRecord.py
def load_json_record(path_to_record):
    ''' Load entire json record for a paper.
        Input: path to record.
        Output: json_record.
    '''
    global json_record
    
    with open(path_to_record, 'r') as json_handler:
        json_record = json.load(json_handler)
        
    return json_record

def extract_sections(json_record):
    global text
    sections = []
    for i in range(len(json_record['body_text'])):
        if json_record['body_text'][i]['section'] in sections:
            next
        else:
            sections.append(json_record['body_text'][i]['section'])
                
    return sections

def join_text_by_section(json_record):
    
    global sections
    sections = []
    global text_by_section
    text_by_section = []
    global temp
    temp = '' 
    
    for chunk in json_record['body_text']:
        
        
        if len(sections) == 0:
            sections.append(chunk['section'])
            
        if chunk['section'] in sections:
            temp += chunk['text'] + ' '
            
        else:
            text_by_section.append(temp)
            temp = ''
            temp += chunk['text'] + ' '
            sections.append(chunk['section'])
            
    text_by_section.append(temp) #for all content of the last section
            
    return text_by_section

def _remove_stop_words(string, stops_words=stop_words):
    '''remove stop words from string of characters'''
    temp1 = string.lower().split(' ')
    temp2 = [x for x in temp1 if x not in stop_words]
    _text = ''
    for t in temp2:
        _text += t + ' '
    return _text

def remove_stop_words(text_by_section):
    
    '''remove stop words from list of string characters.
       input: list of paragraps.
       ouput: list of paragraps whitout stop words
    '''
    global text
    text =list(map(_remove_stop_words,text_by_section))
    return text

# %load wordcountvec.py
#!/usr/bin/python3

'''word count vectorize: put to much weight on words that apperar
   very frequently'''

def countWordVec(text):
	'''word count vectorize: put to much weight on words 
	that apperar very frequently. i mean on each paper section.
	input: list of paragraps, one by section of paper. 
	output: dataframe, columns each word, rows: count of appear 
	by section paper. 
	'''

	vec = CountVectorizer()
	X = vec.fit_transform(text)
	global df
	df = pandas.DataFrame(X.toarray(), 
		                  columns=vec.get_feature_names())
	return df

# %load dbWordProccess.py
#!/usr/bin/python3

class dbWordProccess:
	'''Schema db2: for text proces and word count. '''
	db = {

		'paper_id':[],
    	'sections':[],
    	'text_by_sections':[],
    	'df_word_count_by_section':[]

		 }

	def __init__(self):
		pass

	def add_paper_id(self,paper_id):
		dbWordProccess.db['paper_id'].append(paper_id)

	def add_sections(self,sections):
		dbWordProccess.db['sections'].append(sections)
		

	def add_text_by_section(self,text_by_section):
		dbWordProccess.db['text_by_sections'].append(text_by_section)
		pass

	def add_df_word_count(self,df):
		dbWordProccess.db['df_word_count_by_section'].append(df)

	def store_db(self):
		with open('dbwordproccess.json','a') as json_file:
			json_file.write(str(json.dumps(dbWordProccess.db)))
