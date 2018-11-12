
#include "pistache/endpoint.h"
#include "include/rapidjson/document.h"
#include <string>
#include <cstring>
#include <iostream> // TODO: Remove before production

using namespace Pistache;

class Listener : public Http::Handler {
public:
	HTTP_PROTOTYPE(Listener);

    void onRequest(const Http::Request& request, Http::ResponseWriter response);
};