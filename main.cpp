#include <iostream>
#include "listener.h"
#include "pistache/endpoint.h"
#include "signal.h"

using namespace std;

int main()
{

    Address addr(Ipv4::any(), Port(9080));
    auto opts = Http::Endpoint::options().threads(1);

    Http::Endpoint server(addr);
    server.init(opts);
    server.setHandler(Http::make_handler<Listener>());
    server.serve();

    std::cout << "Shutting down server..." << std::endl
              << std::flush;
    server.shutdown();

    return 0;
}