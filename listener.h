
#include "pistache/endpoint.h"
#include "pistache/client.h"
#include "include/rapidjson/document.h"
#include <string>
#include <cstring>
#include <regex.h>
#include <vector>

#include "Sender.h"
#include "Webgraph.h"

#define CRAWL_HOST "127.0.0.1"
#define CRAWL_PORT 9877

#define INDEX_HOST "127.0.0.1"
#define INDEX_PORT 9876

using namespace Pistache;

class Listener : public Http::Handler
{
  public:
	HTTP_PROTOTYPE(Listener);
	Webgraph graph;
	void onRequest(const Http::Request &request, Http::ResponseWriter response);
	int processQueue();
	//void* calculatePageRank(void * arg);
	Sender sender;
  private:
	
	std::set<std::string> blacklist;
	std::map<std::string, std::vector<std::string>> queue;
	

	bool allowedURL(std::string URL);
};