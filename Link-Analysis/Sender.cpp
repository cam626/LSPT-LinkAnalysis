#include "Sender.h"
#include <iostream>

// #define CRAWL_HOST "129.161.139.90"
// #define CRAWL_PORT "3000"
// Testing:
#define CRAWL_HOST "127.0.0.1"
#define CRAWL_PORT "5000"

#define INDEXING_HOST "127.0.0.1"
#define INDEXING_PORT "5001"

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

	/*
		Construct the message -
			The message to the crawler is sending the next batch of URLs to Crawl. This is a JSON POST formatted
			as follows:

			{
				"URLS": [
					"http://www.rpi.edu",
					"http://www.rpi.edu/example.php",
					"http://www.rpi.edu/example2.php"
				]
			}

			All of the URLs should be on the same domain and there should be no duplicates.
	*/
	std::string message = "{\"URLS\": [";
	std::string url = CRAWL_HOST ":" CRAWL_PORT "/crawl";
	for (size_t i = 0; i < batch.size() - 1; ++i)
	{
		message += "\"http://" + batch[i] + "\",";
	}
	message += "\"http://" + batch[batch.size() - 1] + "\"";

	message += "]\n}\n";

	std::cout << message << std::endl;

	// This will be to receive the response from the crawler (and returned by this function)
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

		/* always cleanup */
		curl_slist_free_all(headers);
		curl_easy_cleanup(curl);
	}
	curl_global_cleanup();
	return readBuffer;
}

std::string Sender::sendRanks(std::map<std::string, std::pair<float, float>> ranks)
{
	std::string url = INDEXING_HOST ":" INDEXING_PORT;
	std::string readBuffer;

	/*
		The ranks sent to indexing are the non-normalized ranks (for now).

		Ex.
		{
			"URLS": [
				["www.a.com", 1.234],
				["www.b.com", 2.341],
				["www.c.com", 0.566]
			]
		}
	*/
	std::string message = "{\"URLS\": [";
	std::map<std::string, std::pair<float, float>>::iterator itr = ranks.begin();

	while (itr != ranks.end())
	{
		message += "[\"" + itr->first + "\", " + std::to_string(itr->second.first) + "]";

		if (++itr != ranks.end())
			message += ", ";
	}

	message += "]}";

	CURL *curl;
	CURLcode res;
	struct curl_slist *headers = NULL;

	std::cout << message << std::endl;

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

		std::cout << "Received crawl response from indexing. (No Action Required)" << std::endl;

		/* always cleanup */
		curl_easy_cleanup(curl);
	}
	curl_global_cleanup();

	// Return the response that we got from Indexing
	return readBuffer;
}