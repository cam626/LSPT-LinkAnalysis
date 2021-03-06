
#include "listener.h"
#include <thread>
#include <queue>
#include <pthread.h>
/*
    Takes a URL and removes the http prefix if it exists.

    Parameters:
        - std::string URL: Represents a web URL.

    Returns: std::string with no http prefix.
*/

//shared queue

std::set<std::string> current_domains;
std::queue<std::string> heads;
pthread_mutex_t mutex;

std::string stripHttp(std::string URL)
{
	// Make sure we don't try to take the substring if it isn't long enough
	if (URL.size() < 7)
		return URL;

	// Two cases: http or https
	if (URL.substr(0, 7) == "http://")
	{
		return URL.substr(7);
	}
	else if (URL.substr(0, 8) == "https://")
	{
		return URL.substr(8);
	}

	// Return unmodified URL if it did not have an http prefix
	return URL;
}

/*
    Extracts the domain from a given URL. This assumes that anything
    after an http prefix and before the next '/' is the domain.

    Parameters:
        - std::string URL: Represents a web URL

    Returns: std::string of the domain from the given URL
*/
std::string domainExtractor(std::string URL)
{
	std::string temp = stripHttp(URL);
	int ending = temp.find("/");
	return temp.substr(0, ending);
}

static void *calculatePageRank(void *arg)
{
	printf("Separate thread fetching from queue...\n");
	Listener *ptr = (Listener *)arg;
	pthread_mutex_lock(&mutex);
	std::string head;
	head = heads.front();
	heads.pop();
	pthread_mutex_unlock(&mutex);

	printf("Updating Ranks...\n");
	ptr->graph.updateRank(head);
	printf("Ranks successfully updated.\n");

	printf("Sending ranks to indexing...\n");
	int id = ptr->sender.addConnection(INDEX_HOST, INDEX_PORT);
	ptr->sender.sendRanks(id, ptr->graph.getAllRanks());
	printf("Ranks sent\n");

	printf("Sending robot requests...\n");
	std::set<std::string>::iterator itr;
	for (itr = current_domains.begin(); itr != current_domains.end(); ++itr)
	{
		std::string response = ptr->sender.requestRobot(id, *itr);

		// parse the json in response
		rapidjson::Document doc;
		rapidjson::ParseResult ok = doc.Parse(response.c_str());

		std::cout << response << std::endl;

		if (!ok)
		{
			std::cout << "Unable to parse response from crawler" << std::endl;
			return NULL;
		}

		if (doc.IsArray())
		{
			const rapidjson::Value &json = doc;

			for (rapidjson::Value::ConstValueIterator itr = json.Begin(); itr != json.End(); ++itr)
			{
				ptr->blacklist.insert(itr->GetString());
			}
		}
	}
	printf("All robots sent.\n");

	printf("POSTing next to crawl...\n");

	ptr->processQueue();

	return NULL;
}

/*
    This function is called by the Pistache Library each time there is data sent to our open port.
    It should parse the request into JSON and determine what to do based on the content of the request.

    Possible inputs come from Text Transformation and Crawling. Documentation on the format of these requests
    can be found here:

    https://docs.google.com/presentation/d/1CMwumUntfIJMWuTSMG6REci5STKPXVPRGI4hCk_vIH8/edit#slide=id.g4657f2d0cc_0_5
*/
void Listener::onRequest(const Http::Request &request, Http::ResponseWriter response)
{

	// Copy the JSON from the request to a c-string to be used in the rapidJSON library
	char json[1048576];
	bzero(&json, 1048576);
	strcpy(json, request.body().c_str());

	pthread_mutex_init(&mutex, NULL);
	pthread_t tid;

	// Parse the JSON and send an error response to the client if it is not valid
	rapidjson::Document doc;
	rapidjson::ParseResult ok = doc.Parse(json);

	if (!ok)
	{
		response.send(Http::Code::Bad_Request, "Malformed JSON.\n");
		return;
	}

	// Determine what was recieved
	if (doc.HasMember("Head"))
	{
		// This section should be from the Text Transformation team

		if (!doc["Head"].IsString())
		{
			response.send(Http::Code::Expectation_Failed, "Expected JSON form not followed.\n");
			return;
		}

		// Transfer the information from the JSON object into simple std objects
		std::string head = doc["Head"].GetString();

		const rapidjson::Value &tails_json = doc["Tails"];
		std::vector<std::string> tails;

		if (!tails_json.IsArray())
		{
			response.send(Http::Code::Expectation_Failed, "Expected JSON form not followed.\n");
			return;
		}

		for (rapidjson::Value::ConstValueIterator itr = tails_json.Begin(); itr != tails_json.End(); ++itr)
		{
			std::string domain = domainExtractor(itr->GetString());
			this->queue[domain].push_back(itr->GetString());

			current_domains.insert(domain);

			// Update graph
			this->graph.addConnection(head, itr->GetString());
		}

		// Send response to client that the data was correctly parsed
		response.send(Http::Code::Ok, "JSON successfully parsed.\n");

		// iterate through the unique domains and add them to the queue to be sent to crawling
		std::set<std::string>::iterator itr;
		for (itr = current_domains.begin(); itr != current_domains.end(); ++itr)
		{
			pthread_mutex_lock(&mutex);
			heads.push(*itr);
			pthread_mutex_unlock(&mutex);
		}

		if (pthread_create(&tid, NULL, calculatePageRank, this))
		{
			printf("pthread_create failed!\n");
			exit(0);
		}
		printf("Listener continuing.\n");
	}
	else if (doc.HasMember("BadURLs"))
	{
		// This section should be from the Crawling team. It should be a list of URLs that returned 404 or other errors
		// during crawling.

		if (!doc["BadURLs"].IsArray())
		{
			response.send(Http::Code::Bad_Request, "Required fields missing.\n");
			return;
		}

		const rapidjson::Value &broken = doc["BadURLs"];
		rapidjson::Value::ConstValueIterator itr;
		for (itr = broken.Begin(); itr != broken.End(); ++itr)
		{
			// TODO: set timeout on node in the graph
		}

		response.send(Http::Code::Ok, "Node status updated.\n");
	}
	else
	{
		// Request could not be identified
		response.send(Http::Code::Bad_Request, "Required fields missing.\n");
	}
}

/*
	Processes the entire queue and sends POST requests to the crawling team of what to
	crawl next.

	Returns: The number of links sent to the crawling team
*/
void Listener::processQueue()
{
	std::string response;
	std::map<std::string, std::vector<std::string>>::iterator itr;
	for (itr = this->queue.begin(); itr != this->queue.end(); ++itr)
	{
		std::vector<std::string> batch;
		for (size_t i = 0; i < itr->second.size(); ++i)
		{
			if (allowedURL(itr->second[i]))
			{
				/*
					TODO: Use information from graph to check timestamp
					      and add to batch if enough time has passed
				*/
				batch.push_back(itr->second[i]);
			}
		}
		itr->second.erase(itr->second.begin(), itr->second.end());

		response = this->sender.sendBatch(batch);

		std::cout << "Crawl Response: " << response << std::endl;
	}
}

/*
	Checks if a URL is allowed by the blacklist.

	Parameters:
		- std::string URL: A URL

	Returns: true if the URL is allowed by the blacklist, false otherwise
*/
bool Listener::allowedURL(std::string URL)
{
	std::set<std::string>::iterator itr;
	for (itr = this->blacklist.begin(); itr != this->blacklist.end(); ++itr)
	{
		std::string temp = stripHttp(*itr);
		std::string mod_URL = stripHttp(URL);
		if (mod_URL.substr(0, temp.size()) == temp)
		{
			return false;
		}
	}
	return true;
}
