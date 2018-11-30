import aiohttp
from aiohttp import web
import psycopg2
import json
import hashlib
from init import init
from Text_Transformation_controller import Text_Transformation_controller

#TO DO:
#Need Link Analysis and Indexing HTTP Address for init.py
#Need to confirm crawling API details for json

def post(request):
	"""
	{
		"url": string,
		"timestamp": int,
		"content": string
	}
	"""
	try:
		#Pull init data from file
		initilization_data = init()
		
		#DEBUG LINE
		#print(initilization_data)
		
		#Receive data from Crawling
		request = request.json()
		
		#Send request["metadata"] to Link Analysis
		client = aiohttp.ClientSession()
		client.post(str(initilization_data['Link_Analysis_address']),data=request("metadata").stringify)
		
		#Run our functions
		output_json = Text_Transformation_controller(request,initilization_data['max_n_gram_size'],initilization_data['max_threads'])
		
		#Send data to Indexing
		client = aiohttp.ClientSession()
		client.post(str(initilization_data['Indexing_address']),data=output_json.stringify)
		
		#Tell Crawling that this was a success
		response_obj = {"status": 200}
		return web.Response(text=json.dumps(response_obj), status=200)
		
	except Exception as e:
		#print(e)  #This line for debugging
		
		#Tell Crawling that this was a failure
		response_obj = {"status": 500, "message": "Incorrect JSON Format: " + str(e)}
		return web.Response(text=json.dumps(response_obj), status=500)
		
if __name__== "__main__":
	post('test')