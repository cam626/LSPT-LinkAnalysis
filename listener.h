
#include "pistache/endpoint.h"
#include "pistache/client.h"
#include "include/rapidjson/document.h"
#include <string>
#include <cstring>
#include <regex.h>
#include <vector>

using namespace Pistache;

class Listener : public Http::Handler
{
  public:
	HTTP_PROTOTYPE(Listener);

	void onRequest(const Http::Request &request, Http::ResponseWriter response);
};