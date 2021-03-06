#include "Sender.h"
#include <iostream>

/*
	Finds a connection corresponding to the given information.

	Parameters:
		- std::string host: The host of the connection to search for
		- int port: The port of the connection to search for

	Returns: The socket file descriptor corresponding to the described connection
				if it exists, -1 otherwise.
*/
int Sender::findConnection(std::string host, int port)
{
	std::pair<std::string, int> temp;
	temp.first = host;
	temp.second = port;
	std::map<int, std::pair<std::string, int>>::iterator itr;
	for (itr = this->connections.begin(); itr != this->connections.end(); ++itr)
	{
		if (itr->second == temp)
		{
			return itr->first;
		}
	}
	return -1;
}

/*
	Finds a connection that corresponds to the socket given.

	Parameters:
		- int sock: The socket to search for

	Returns: The connection information corresponding to the given socket.
*/
std::pair<std::string, int> Sender::findConnectionBySocket(int sock)
{
	if (this->connections.find(sock) != this->connections.end())
	{
		return this->connections[sock];
	}
	std::pair<std::string, int> temp;
	temp.first = "";
	temp.second = -1;
	return temp;
}

/*
	Adds a connection with the given host on the given port if it does not exist
	or finds the connection if one already exists.

	Parameters:
		- std::string host: The host to connect to
		- int port: The port to connect on

	Returns: The socket file descriptor corresponding to the new or existing connection.
*/
int Sender::addConnection(std::string host, int port)
{
	int temp = this->findConnection(host, port);
	if (temp >= 0)
	{
		return temp;
	}

	struct sockaddr_in serv_addr;
	int sock = socket(AF_INET, SOCK_STREAM, 0);
	bzero(&serv_addr, sizeof(serv_addr));

	serv_addr.sin_family = AF_INET;
	serv_addr.sin_port = htons(port);
	if (inet_pton(AF_INET, host.c_str(), &serv_addr.sin_addr.s_addr) <= 0)
	{
		printf("Malformed host.\n");
		return -1;
	}

	if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
	{
		printf("Unable to establish a connection to the host.\n");
		return -1;
	}

	std::pair<std::string, int> temp2;
	temp2.first = host;
	temp2.second = port;

	this->connections[sock] = temp2;

	return sock;
}

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
std::string Sender::requestRobot(int sock, std::string domain)
{
	std::string message = domain + "/robots.txt";
	std::string request_url = "http://blue-x.cs.rpi.edu/robots?url=http://" + message;
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

int Sender::sendRanks(int sock, std::map<std::string, std::pair<float, float>> ranks)
{
	std::pair<std::string, int> connection = this->findConnectionBySocket(sock);
	std::string message = "POST / HTTP/1.1\nUser-Agent: Link-Analysis\nContent-Type: application/json\nAccept: application/json\nHost: " +
						  connection.first + "\n\n[\n";

	std::map<std::string, std::pair<float, float>>::iterator itr;
	for (itr = ranks.begin(); itr != ranks.end(); ++itr)
	{
		message += "\t{\n\t\t'url': '" + itr->first + "',\n\t\t'rank': '" + std::to_string(itr->second.first) + "'\n},\n";
	}

	message += "\n]\n";
	// TODO: handle response from Crawler

	send(sock, message.c_str(), strlen(message.c_str()), 0);
	return 200;
}