#include <stdlib.h>
#include <string>
#include <string.h>
#include <vector>
#include <unordered_map>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

class Sender
{
  public:
	Sender() {}
	int addConnection(std::string host, int port);
	int findConnection(std::string host, int port);
	std::pair<std::string, int> findConnectionBySocket(int sock);
	int requestRobot(int sock, std::string domain);

  private:
	std::unordered_map<int, std::pair<std::string, int>> connections;
};