from aiohttp import web
import psycopg2
import json
import hashlib
from main import settings
import logging
import uuid

if not os.path.exists('logs'):
  os.mkdir('logs')

logging.basicConfig(filename=os.path.join('logs','red_m.log'), format='%(asctime)s - %(levelname)s - %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())

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
    unique_task_id = uuid.uuid1()
    #Receive data from Crawling
    request = await request.json()
    logging.warn("{0} - received a request".format(unique_task_id))

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
    logging.warn("{0} - Successfully finished processing request.".format(unique_task_id))
    return web.Response(text=json.dumps(response_obj), status=200)

  except Exception as e:
    #print(e)  #This line for debugging
    logging.error("{0} - An Exception occurred.\nREQUEST:\n{1}".format(unique_task_id,json.dumps(request, indent=4)), exc_info=True)

    #Tell Crawling that this was a failure
    response_obj = {"status": 500, "message": "Incorrect JSON Format: " + str(e)}
    logging.warn("{0} - Finished processing request in error.".format(unique_task_id))
    return web.Response(text=json.dumps(response_obj), status=500)
