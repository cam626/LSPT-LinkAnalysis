import json
import urllib.request


def standard_test():
	# POST a head-tail configuration
	message = {"Head": "www.a.com", "Tails": ["www.b.com", "www.c.com"]}

	myurl = "http://127.0.0.1:9080"
	req = urllib.request.Request(myurl)
	req.add_header('Content-Type', 'application/json; charset=utf-8')
	jsondata = json.dumps(message)
	jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
	req.add_header('Content-Length', len(jsondataasbytes))
	
	response = urllib.request.urlopen(req, jsondataasbytes)

	if response.status is not 200:
		print("Standard Test failed. Server returned status:", response.status)
	else:
		print("PASSED Standard Test")

def large_test():
	# POST a large head-tail configuration (lots of tails - 10,000)

	tails = []
	for i in range(10000):
		tails.append("www." + str(i) + ".com")
	message = {"Head": "www.a.com", "Tails": tails}

	myurl = "http://127.0.0.1:9080"
	req = urllib.request.Request(myurl)
	req.add_header('Content-Type', 'application/json; charset=utf-8')
	jsondata = json.dumps(message)
	jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
	req.add_header('Content-Length', len(jsondataasbytes))
	
	response = urllib.request.urlopen(req, jsondataasbytes)

	if response.status is not 200:
		print("Large Test failed. Server returned status:", response.status)
	else:
		print("PASSED Large Test")

if __name__ == "__main__":
	# This script will do a number of tests on the link-analysis component
	standard_test()
	large_test()