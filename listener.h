
#include "pistache/endpoint.h"
#include <string>

using namespace Pistache;

class Listener : public Http::Handler {
public:
	HTTP_PROTOTYPE(Listener);

    void onRequest(const Http::Request& request, Http::ResponseWriter response) {
         response.send(Http::Code::Ok, "Hello, World");
    }
};