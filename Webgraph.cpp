#include "Webgraph.h"

using namespace std;

bool Webgraph::hasLink(const string &url_) const {
    for (int i=0; i<all_links.size(); ++i) {
        if (all_links[i].getUrl() == url_) { return true; }
    }
    return false;
}

void Webgraph::addLink(const string &url_) {
    if (hasLink(url_)) { return; }
    Node n(url_);
    all_links.push_back(n);
    adj_matrix[n] = vector<Node>();
}
