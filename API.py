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
#Need to confirm crawling API details for json from Crawling

def post(request):
	try:
		#Pull init data from file
		initilization_data = init()
		
		#Receive data from Crawling
		crawling_data = json.loads(request)
		
		#Run our functions
		output_json = Text_Transformation_controller(crawling_data,initilization_data['max_n_gram_size'])
		
		#Send metadata to Link Analysis
		r = requests.post(initilization_data['Link_Analysis_address'],output_json['metadata'])
		
		#Send data to Indexing
		r = requests.post(initilization_data['Indexing_address'],output_json)
		
		#Tell Crawling that this was a success
		response_obj = {"status": 200}
		return web.Response(text=json.dumps(response_obj), status=200)
		
	except Exception as e:		
		#Tell Crawling that this was a failure
		print(e)
		response_obj = {"status": 500, "message": "Incorrect JSON Format: "}
		return web.Response(text=json.dumps(response_obj), status=500)
		
app=web.Application()
app.add_routes([web.post('/',post)])
		
if __name__== "__main__":
	post("""{"url": "https://www.google.com", "metadata": { "timestamp": "2018-3-12", "forward_address" : ""}, "content": "<!DOCTYPE html>\\n<html>\\n\\t<head>\\n\\t\\t<title>Service Worker Toolbox</title>\\n\\t\\t<h1>Header Text testing</h1>\\t</head>\\n\\t<body>\\n\\t\\t<!-- Images -->\\n\\t\\t<h6>Testing header</h6>\\n\\t\\t<img src=\\"/images/contact.svg\\" height=\\"80\\" width=\\"80\\" />1\\n\\t\\t<img src=\\"/images/info.svg\\" height=\\"80\\" width=\\"80\\" />2\\n\\t\\t<img src=\\"/images/cv.svg\\" height=\\"80\\" width=\\"80\\" />3\\n\\t\\t<a href = \\"www.google.com\\">link</a>\\n\\t\\t<script>sdfsdf sdf</script>\\n\\t</body>4\\n</html>"}""")