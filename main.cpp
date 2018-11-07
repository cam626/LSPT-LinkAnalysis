#include <iostream>
#include "listener.h"
#include "pistache/endpoint.h"

using namespace std;

int main() {

    Address addr(Ipv4::any(), Port(9080));
    auto opts = Http::Endpoint::options().threads(1);

    Http::Endpoint server(addr);
    server.init(opts);
    server.setHandler(Http::make_handler<Listener>());
    server.serve();

    server.shutdown();

    return 0;
}