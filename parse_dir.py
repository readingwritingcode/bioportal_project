#!/usr/bin/python3

import os
import sys
import json
import time
import pandas
import urllib
from urllib import parse, request


# Process directori kagle/document_parses
#                                       /pdf_json
#                                       /pmc_json

def parse_directory(path_to_directory):

	'''documentation'''
	global path_files
	path_files = []

	for root, dirs, files in os.walk(path_to_directory):
		for file in files:
			path_files.append(os.path.join(root, file))

	return path_files


if __name__ == '__main__':
	parse_directory(sys.argv[1])
	print(path_files)
                       	                       

 