#This is the initialization file for the Red_M API
import json

def init():
	initilization_data = {}	#Use a json to move the data around
	
	#The address of the Indexing team
	initilization_data['Indexing_address'] = 'green-eth.cs.rpi.edu'

	#The address of the Link Analysis Team
	initilization_data['Link_Analysis_address'] = 'http://129.161.141.144:9080'

	#The address of the Crawling team
	initilization_data['Crawling_address'] = 'http://129.161.36.170:3000'

	#The max size n-gram to compute
	initilization_data['max_n_gram_size'] = 5

	#The number of threads to spin up (the number of concurrent calls we want to handle)
	initilization_data['max_threads'] = 1
	
	return initilization_data
