
#include "listener.h"

/*
    Takes a URL and removes the http prefix if it exists.

    Parameters:
        - std::string URL: Represents a web URL.

    Returns: std::string with no http prefix.
*/
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

/*
	This function is used to organize a list of URLs into a map with a domain as the key
	and a list of URLs on that domain as the value.

	Parameters:
		- std::vector<std::string> URLs: A list of URLs

	Returns: A map where the keys are domains and the values are lists of URLs on the specified domain
*/
std::unordered_map<std::string, std::vector<std::string>> domainOrganizer(std::vector<std::string> URLs)
{
	std::unordered_map<std::string, std::vector<std::string>> domains;
	for (size_t i = 0; i < URLs.size(); ++i)
	{
		std::string current_domain = domainExtractor(URLs[i]);
		domains[current_domain].push_back(URLs[i]);
	}
	return domains;
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
	char json[1024];
	bzero(&json, 1024);
	strcpy(json, request.body().c_str());

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
			tails.push_back(itr->GetString());
		}

		// Send response to client that the data was correctly parsed
		response.send(Http::Code::Ok, "JSON successfully parsed.\n");

		// TODO: Use head and tails to update graph
		// TODO: Call rank updater

		int id = this->sender.addConnection(CRAWL_HOST, CRAWL_PORT);
		if (id != -1)
		{
			std::unordered_map<std::string, std::vector<std::string>> domains = domainOrganizer(tails);
			std::unordered_map<std::string, std::vector<std::string>>::iterator itr;
			for (itr = domains.begin(); itr != domains.end(); ++itr)
			{
				this->sender.requestRobot(id, domainExtractor(itr->first));
			}
		}
	}
	else if (doc.HasMember("Robots"))
	{
		// This section should be from the Crawling team. It should be a response to our request for a robots.txt file
		if (!doc.HasMember("Disallow") || !doc["Disallow"].IsArray() || !doc.HasMember("Domain"))
		{
			response.send(Http::Code::Bad_Request, "Required fields missing.\n");
			return;
		}

		std::string domain = doc["Domain"].GetString();
		const rapidjson::Value &disallowed = doc["Disallow"];
		rapidjson::Value::ConstValueIterator itr;
		for (itr = disallowed.Begin(); itr != disallowed.End(); ++itr)
		{
			this->blacklist.push_back(domain + itr->GetString());
		}
	}
	else if (doc.HasMember("BadURLs"))
	{
		// This section should be from the Crawling team. It should be a list of URLs that returned 404 or other errors
		// during crawling.
		// TODO: Implement this section
	}
	else
	{
		// Request could not be identified
		response.send(Http::Code::Bad_Request, "Required fields missing.\n");
	}
}