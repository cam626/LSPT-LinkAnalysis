from flask import Flask, request
app = Flask(__name__)
import json

@app.route('/robots', methods=["GET"])
def findRobot():
	return '["/search", "/hidden", "/secretfolder/inner"]'

@app.route('/crawl', methods=["POST"])
def crawlNext():
	return '{"URLS": ["http://www.google.com", "http://www.rpi.edu"]}'