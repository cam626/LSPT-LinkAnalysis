#include "Sender.h"
#include <iostream>

#define CRAWL_HOST "129.161.139.90"
#define CRAWL_PORT "3000"

#define INDEXING_HOST "127.0.0.1"
#define INDEXING_PORT "9876"

/*
	Callback function for when we receive a response from a request to the crawler.
*/
static size_t WriteCallback(void *contents, size_t size, size_t nmemb, void *userp)
{
	((std::string *)userp)->append((char *)contents, size * nmemb);
	return size * nmemb;
}

/*
	Sends a POST request to the crawling team with the location of a robots.txt file
	for a specific domain.

	Parameters:
		- std::string domain: The domain to request a robots.txt file for (without http(s)://)

	Returns: The HTTP response code given in the response from the crawling team.
*/
std::string Sender::requestRobot(std::string domain)
{
	std::string message = domain + "/robots.txt";
	std::string request_url = "http://" CRAWL_HOST ":" CRAWL_PORT "/robots?url=http://" + message;
	std::string readBuffer;

	CURL *curl;
	CURLcode res;

	/* In windows, this will init the winsock stuff */
	curl_global_init(CURL_GLOBAL_ALL);

	/* get a curl handle */
	curl = curl_easy_init();
	if (curl)
	{
		/* First set the URL that is about to receive our GET. This URL can
    	just as well be a https:// URL if that is what should receive the
       	data. */
		curl_easy_setopt(curl, CURLOPT_URL, request_url.c_str());
		/* Now specify the POST data */
		curl_easy_setopt(curl, CURLOPT_HTTPGET, 1L);
		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
		curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);

		/* Perform the request, res will get the return code */
		res = curl_easy_perform(curl);
		/* Check for errors */
		if (res != CURLE_OK)
			fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));

		std::cout << "Received robot response from crawler.\nUpdating blacklist..." << std::endl;

		/* always cleanup */
		curl_easy_cleanup(curl);
	}
	curl_global_cleanup();
	return readBuffer;
}

/*
	Sends the next URLs that the crawling team should crawl in batches that contain URLs on
	a single domain.

	Parameters:
		- int sock: A previously opened socket to communicate with the crawling team
		- std::vector<std::string> batch: A list of URLs that the crawler should crawl next.
											Should all be from the same domain.

	Returns: The HTTP response code given in the response from the crawling team.
*/
std::string Sender::sendBatch(std::vector<std::string> batch)
{
	std::string message = "{\"URLS\": [";
	std::string url = CRAWL_HOST ":" CRAWL_PORT "/crawl";
	for (size_t i = 0; i < batch.size() - 1; ++i)
	{
		message += "\"http://" + batch[i] + "\",";
	}
	message += "\"http://" + batch[batch.size() - 1] + "\"";

	// TODO: handle response from Crawler

	message += "]\n}\n";

	std::cout << message << std::endl;

	std::string readBuffer;

	CURL *curl;
	CURLcode res;
	struct curl_slist *headers = NULL;

	/* In windows, this will init the winsock stuff */
	curl_global_init(CURL_GLOBAL_ALL);

	/* get a curl handle */
	curl = curl_easy_init();
	if (curl)
	{
		/* First set the URL that is about to receive our POST. This URL can
    	just as well be a https:// URL if that is what should receive the
       	data. */
		curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
		/* Now specify the POST data */
		curl_easy_setopt(curl, CURLOPT_HTTPPOST, 12L);
		headers = curl_slist_append(headers, "Content-Type: application/json");
		curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
		curl_easy_setopt(curl, CURLOPT_POSTFIELDS, message.c_str());
		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
		curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);

		/* Perform the request, res will get the return code */
		res = curl_easy_perform(curl);
		/* Check for errors */
		if (res != CURLE_OK)
			fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));

		std::cout << "Received crawl response from crawler.\nUpdating graph..." << std::endl;

		curl_slist_free_all(headers);
		/* always cleanup */
		curl_easy_cleanup(curl);
	}
	curl_global_cleanup();
	return readBuffer;
}

std::string Sender::sendRanks(std::map<std::string, std::pair<float, float>> ranks)
{
	// TODO: Create false indexing simulator to respond to this request (for testing)
	std::string url = INDEXING_HOST ":" INDEXING_PORT;
	std::string readBuffer;
	std::string message = "{\"URLS\": [";
	std::map<std::string, std::pair<float, float>>::iterator itr = ranks.begin();

	while (itr != ranks.end())
	{
		message += "[" + itr->first + ", " + std::to_string(itr->second.first) + "]";

		if (++itr != ranks.end())
			message += ", ";
	}

	message += "]}";

	// TODO: possible move the curl object to the listener object
	CURL *curl;
	CURLcode res;

	/* In windows, this will init the winsock stuff */
	curl_global_init(CURL_GLOBAL_ALL);

	/* get a curl handle */
	curl = curl_easy_init();
	if (curl)
	{
		/* First set the URL that is about to receive our POST. This URL can
    	just as well be a https:// URL if that is what should receive the
       	data. */
		curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
		/* Now specify the POST data */
		curl_easy_setopt(curl, CURLOPT_HTTPPOST, 1L);
		curl_easy_setopt(curl, CURLOPT_POSTFIELDS, message.c_str());
		curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
		curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);

		/* Perform the request, res will get the return code */
		res = curl_easy_perform(curl);
		/* Check for errors */
		if (res != CURLE_OK)
			fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));

		std::cout << "Received crawl response from crawler.\nUpdating graph..." << std::endl;

		/* always cleanup */
		curl_easy_cleanup(curl);
	}
	curl_global_cleanup();

	// Return the response that we got from Indexing
	return readBuffer;
}