#include <stdlib.h>
#include <string>
#include <string.h>
#include <vector>
#include <map>
#include <set>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <curl/curl.h>

class Sender
{
public:
	Sender() {}
	int addConnection(std::string host, int port);
	int findConnection(std::string host, int port);
	std::pair<std::string, int> findConnectionBySocket(int sock);
	int requestRobot(int sock, std::string domain);
	int sendBatch(int sock, std::vector<std::string> batch);
	int sendRanks(int sock, std::map<std::string, std::pair<float, float>> ranks);

private:
	std::map<int, std::pair<std::string, int>> connections;
};