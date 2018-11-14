
#include "pistache/endpoint.h"
#include "pistache/client.h"
#include "include/rapidjson/document.h"
#include <string>
#include <cstring>
#include <regex.h>
#include <vector>

#include "Sender.h"

#define TT_HOST "127.0.0.1"
#define TT_PORT 9877

using namespace Pistache;

class Listener : public Http::Handler
{
  public:
	HTTP_PROTOTYPE(Listener);

	void onRequest(const Http::Request &request, Http::ResponseWriter response);

  private:
	Sender sender;
};