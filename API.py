import aiohttp
from aiohttp import web
import psycopg2
import json
import hashlib
from init import init
import requests
from Text_Transformation_controller import Text_Transformation_controller
import logging
import uuid
import os

if not os.path.exists('logs'):
  os.mkdir('logs')
  
logging.basicConfig(filename=os.path.join('logs','red_m.log'), format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())
  
#TO DO:
#Need Link Analysis and Indexing HTTP Address for init.py
#Need to confirm crawling API details for json from Crawling

async def post(request):
	try:
		unique_task_id = uuid.uuid1()
		#Pull init data from file
		initilization_data = init()
		logging.warn("{0} - received a request".format(unique_task_id))
		
		#Receive data from Crawling
		crawling_data = await request.json()
		
		#Run our functions
		output_json = Text_Transformation_controller(crawling_data,initilization_data['max_n_gram_size'])
		
		#Send metadata to Link Analysis
		r = requests.post(initilization_data['Link_Analysis_address'],output_json['metadata'])
		
		#Send data to Indexing
		r = requests.post(initilization_data['Indexing_address'],output_json)
		
		#Tell Crawling that this was a success
		response_obj = {"status": 200}
		logging.warn("{0} - Successfully finished processing request.".format(unique_task_id))
		return web.Response(text=json.dumps(response_obj), status=200)
		
	except Exception as e:		
		#Tell Crawling that this was a failure
		logging.error("{0} - An Exception occurred.\nREQUEST:\n{1}".format(unique_task_id,json.dumps(request, indent=4)), exc_info=True)
		response_obj = {"status": 500, "message": "Incorrect JSON Format: "}

		logging.warn("{0} - Finished processing request in error.".format(unique_task_id))
		return web.Response(text=json.dumps(response_obj), status=500)
		
app=web.Application()
app.add_routes([web.post('/',post)])
web.run_app(app)
		
#if __name__== "__main__":
#	post("""{"url": "https://www.google.com", "metadata": { "timestamp": "2018-3-12", "forward_address" : ""}, "content": "<!DOCTYPE html>\\n<html>\\n\\t<head>\\n\\t\\t<title>Service Worker Toolbox</title>\\n\\t\\t<h1>Header Text testing</h1>\\t</head>\\n\\t<body>\\n\\t\\t<!-- Images -->\\n\\t\\t<h6>Testing header</h6>\\n\\t\\t<img src=\\"/images/contact.svg\\" height=\\"80\\" width=\\"80\\" />1\\n\\t\\t<img src=\\"/images/info.svg\\" height=\\"80\\" width=\\"80\\" />2\\n\\t\\t<img src=\\"/images/cv.svg\\" height=\\"80\\" width=\\"80\\" />3\\n\\t\\t<a href = \\"www.google.com\\">link</a>\\n\\t\\t<script>sdfsdf sdf</script>\\n\\t</body>4\\n</html>"}""")
