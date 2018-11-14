// Webgraph.cpp
// Author: Jinwei Shen
//
// Implementation of Webgraph class functions

#include "Node.h"
#include "Webgraph.h"

using namespace std;

const vector<Node>& Webgraph::getAllLinks() const {
    return all_links;
}

bool Webgraph::hasLink(const string &url_) const {
    for (int i=0; i<all_links.size(); ++i) {
        if (all_links[i].getUrl() == url_) { return true; }
    }
    return false;
}

// Assume the node with the provided url exists
// checked through the function hasLink
const Node& Webgraph::getNode(const std::string &url_) const {
    for (int i=0; i<all_links.size(); ++i) {
        if (all_links[i].getUrl() == url_) {
            return all_links[i];
        }
    }
}

void Webgraph::addLink(const string &url_) {
    if (hasLink(url_)) { return; }
    Node n(url_);
    all_links.push_back(n);
    adj_matrix[n] = vector<Node>();
}

void Webgraph::addConnection(const std::string &from_url, const std::string &to_url) {
    if (hasLink(from_url) == false) {
        addLink(from_url);
    }
    if (hasLink(to_url) == false) {
        addLink(to_url);
    }
    Node n_from = getNode(from_url);
    Node n_to = getNode(to_url);
    if (n_from.hasChild(n_to)) { return; }
    adj_matrix[n_from].push_back(n_to);
}
