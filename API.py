import aiohttp
from aiohttp import web
import psycopg2
import json
import hashlib
from init import init
import requests
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
		
		#Receive data from Crawling
		test = json.loads(request)
		
		#Send request["metadata"] to Link Analysis
		r = requests.post(initilization_data['Link_Analysis_address'],test)
		
		#Run our functions
		output_json = Text_Transformation_controller(request,initilization_data['max_n_gram_size'],initilization_data['max_threads'])
		
		#Send data to Indexing
		r = requests.post(initilization_data['Indexing_address'],output_json)
		
		#Tell Crawling that this was a success
		response_obj = {"status": 200}
		return web.Response(text=json.dumps(response_obj), status=200)
		
	except Exception as e:		
		#Tell Crawling that this was a failure
		response_obj = {"status": 500, "message": "Incorrect JSON Format: "}
		return web.Response(text=json.dumps(response_obj), status=500)
		
if __name__== "__main__":
	post("""{"url": "http://192.168.1.0:5000/tt", "timestamp": 5, "content": "string"}""")