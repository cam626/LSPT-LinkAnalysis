#include "Sender.h"

int Sender::findConnection(std::string host, int port)
{
	std::pair<std::string, int> temp;
	temp.first = host;
	temp.second = port;
	std::unordered_map<int, std::pair<std::string, int>>::iterator itr;
	for (itr = this->connections.begin(); itr != this->connections.end(); ++itr)
	{
		if (itr->second == temp)
		{
			return itr->first;
		}
	}
	return -1;
}

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

int Sender::requestRobot(int sock, std::string domain)
{
	std::pair<std::string, int> connection = this->findConnectionBySocket(sock);
	std::string message = "POST / HTTP/1.1\nUser-Agent: Link-Analysis\nContent-Type: application/json\nAccept: application/json\nHost: " +
						  connection.first + "\n\n{\n\t'Robots': '" + domain + "/robots.txt'\n}\n";

	// TODO: handle response from Crawler

	return send(sock, message.c_str(), strlen(message.c_str()), 0);
}

int Sender::sendBatch(int sock, std::vector<std::string> batch)
{
	std::pair<std::string, int> connection = this->findConnectionBySocket(sock);
	std::string message = "POST / HTTP/1.1\nUser-Agent: Link-Analysis\nContent-Type: application/json\nAccept: application/json\nHost: " +
						  connection.first + "\n\n{\n\t'URLs': [";

	for (size_t i = 0; i < batch.size() - 1; ++i)
	{
		message += "'" + batch[i] + "',";
	}
	message += "'" + batch[batch.size() - 1] + "'";

	// TODO: handle response from Crawler

	message += "]\n}\n";
	return send(sock, message.c_str(), strlen(message.c_str()), 0);
}