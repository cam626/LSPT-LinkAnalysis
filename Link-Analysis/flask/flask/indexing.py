# This file is used to simulate the indexing component when testing Link Analysis. It is run through flask and 
# returns constant responses to HTTP Requests

from flask import Flask, request
app = Flask(__name__)
import json

@app.route('/', methods=["POST"])
def printRequestData():
	json_data = request.get_json()
	print(json_data)
	return '', 200