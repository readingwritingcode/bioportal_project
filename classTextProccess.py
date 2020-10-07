#!/usr/bin/python3
class dbTextProccess(object):
	
	'''
	This database store results of text process data for each paper.

	db schema:

	db = {'paper_id':[str,str,str,...],

		  'sections':[list,list,list...],
		  'text_by_sections':[list,list,list...],
		  'df_word_count_for_sections': [json,json,json...]

	}

	Asserts:

	N = num of papers.
	assert N == len('papper_id')
	assert len(db['paper_id'])==len(db['sections'])
	assert len(db['sections'])==len(db['text_by_sections'])
	assert len(db['text_by_sections'])==len(db['df_word_count_for_sections'])

	assert len(db['sections'][n]) == len(db['text_by_sections'][n]) #for n in range 0...N
		
	'''
	db = {'paper_id':[],
		  'sections':[],
		  'text_by_sections':[],
		  'df_word_count_for_sections':[]
	}

	def __init__(self, paper_id, sections, text_by_sections, df_word_count_for_sections):

		'''init state for each paper, thus are 
			paper_id,sections, text_by_sections,
		'''

		self.paper_id = paper_id
		self.sections = sections
		self.text_by_sections = text_by_sections
		self.df_word_count_for_sections = df_word_count_for_sections

	def storePaperTextProccessData(self):
		dbTextProccess.db['paper_id'].append(self.paper_id)
		dbTextProccess.db['sections'].append(self.sections)
		dbTextProccess.db['text_by_sections'].append(self.text_by_sections)
		dbTextProccess.db['df_word_count_for_sections'].append(self.df_word_count_for_sections)
		pass

	def writeData(self):
		with open('textProccessBio.json','w') as json_handler:
			json_handler.write(json.dumps(dbTextProccess.db))
		pass

	def main():
		passdb
	if __name__ == '__main__':
		main()