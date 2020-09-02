#!/usr/bin/python3
import sys
import json
import parse_dir


def annotated_records(path_to_directory):

	for path in parse_dir.parse_directory(path_to_directory):

		with open(path, 'r') as record_handler:
			record = json.load(record_handler)

		try: #for pdf_json
			pass 

			# call apy for abstract paraghraps
			# call apy for body paraghraps			

		except: #for pmc_json
			pass


		finally: # call api for title 
			pass


		print(record.keys())
		break
		

if __name__ == '__main__':
	annotated_records(sys.argv[1])