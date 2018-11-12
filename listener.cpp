
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

int regexMatch(const char *string, char *pattern)
{
	int status;
	regex_t re;

	if (regcomp(&re, pattern, REG_EXTENDED | REG_NOSUB) != 0)
	{
		return (0); /* report error */
	}
	status = regexec(&re, string, (size_t)0, NULL, 0);
	regfree(&re);
	if (status != 0)
	{
		return (0); /* report error */
	}
	return (1);
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

	Http::Client client;

	auto opts = Http::Client::options()
					.threads(1)
					.maxConnectionsPerHost(8);
	client.init(opts);

	// Determine what was recieved
	if (doc.HasMember("Head"))
	{
		// This section should be from the Text Transformation team
		response.send(Http::Code::Ok, domainExtractor(doc["Head"].GetString()) + "\n");

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
		// TODO: Call sender to POST to Crawler
	}
	else if (doc.HasMember("Robots"))
	{
		// This section should be from the Crawling team. It should be a response to our request for a robots.txt file
		// TODO: Implement this section
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