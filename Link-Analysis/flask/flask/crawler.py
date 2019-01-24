# This file is used to simulate the crawler component when testing Link Analysis. It is run through flask and 
# returns constant responses to HTTP Requests

from flask import Flask, request
app = Flask(__name__)
import json

@app.route('/robots', methods=["GET"])
def findRobot():
	return '["/search", "/hidden", "/secretfolder/inner"]'

@app.route('/crawl', methods=["POST"])
def crawlNext():
	return '{"URLS": ["http://www.google.com", "http://www.rpi.edu"]}'