#include <stdlib.h>
#include <string>
#include <string.h>
#include <vector>
#include <map>
#include <set>
#include <curl/curl.h>

class Sender
{
  public:
	Sender() {}
	std::string requestRobot(std::string domain);
	std::string sendBatch(std::vector<std::string> batch);
	int sendRanks(std::map<std::string, std::pair<float, float>> ranks);

  private:
	std::map<int, std::pair<std::string, int>> connections;
};