from aiohttp import web
import psycopg2
import json
import hashlib
from main import settings

#TO DO:
#Need Link Analysis and Indexing HTTP Address
#Need crawling API details

async def post(request):
	"""
	{
		"url": string,
		"timestamp": int,
		"content": string
	}
	"""
	try:		
		#Receive data from Crawling
		request = await request.json()
		
		#Send request["metadata"] to Link Analysis
		client = aiohttp.ClientSession()
		client.post(('http://192.168.1.0:5000/TT',data=request["metadata"].stringify()))	#The address to send to is currently unknown
		
		#Run our functions
		output_json = Text_Transformation_controller(request)
		
		#Send data to Indexing
		client = aiohttp.ClientSession()
		client.post(('http://192.168.1.0:5000/tt',data=output_json.stringify()))		#ip:port/tt lowercase
		
		#Tell Crawling that this was a success
		response_obj = {"status": 200}
		return web.Response(text=json.dumps(response_obj), status=200)
		
	except Exception as e:
		#print(e)  #This line for debugging
		
		#Tell Crawling that this was a failure
		response_obj = {"status": 500, "message": "Incorrect JSON Format: " + str(e)}
		return web.Response(text=json.dumps(response_obj), status=500)