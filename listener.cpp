
#include "listener.h"

void Listener::onRequest(const Http::Request& request, Http::ResponseWriter response) {
    std::cout << request.body() << std::endl;

    char json[1024];
    strcpy(json, request.body().c_str());

    rapidjson::Document doc;
    doc.Parse(json);

    response.send(Http::Code::Ok, doc["username"].GetString());
}