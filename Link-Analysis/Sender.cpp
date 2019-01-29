#include "Sender.h"
#include <iostream>

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
		- int sock: A previously opened socket to communicate with the crawling team
		- std::string domain: The domain to request a robots.txt file for

	Returns: The HTTP response code given in the response from the crawling team.
*/
std::string Sender::requestRobot(std::string domain)
{
	std::string message = domain + "/robots.txt";
	std::string request_url = "127.0.0.1:9877?url=http://" + message;
	std::string readBuffer;

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
	std::string message = "'URLs': [";

	for (size_t i = 0; i < batch.size() - 1; ++i)
	{
		message += "'" + batch[i] + "',";
	}
	message += "'" + batch[batch.size() - 1] + "'";

	// TODO: handle response from Crawler

	message += "]\n}\n";

	std::string readBuffer;

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
		curl_easy_setopt(curl, CURLOPT_URL, "http://blue-x.cs.rpi.edu/crawl");
		/* Now specify the POST data */
		curl_easy_setopt(curl, CURLOPT_HTTPGET, 1L);
		curl_easy_setopt(curl, CURLOPT_POSTFIELDS, message);
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
	return readBuffer;
}

int Sender::sendRanks(std::map<std::string, std::pair<float, float>> ranks)
{
	// TODO: Rewrite this to use CURL

	return -1;
}