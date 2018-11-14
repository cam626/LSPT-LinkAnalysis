// Webgraph.cpp
// Author: Jinwei Shen
//
// Implementation of Webgraph class functions

#include "Node.h"
#include "Webgraph.h"

typedef unsigned int uint;

using namespace std;

const vector<Node>& Webgraph::getAllNodes() const {
    return all_nodes;
}

bool Webgraph::hasLink(const string &url_) const {
    for (uint i=0; i<all_nodes.size(); ++i) {
        if (all_nodes[i].getUrl() == url_) { return true; }
    }
    return false;
}

// Assume the node with the provided url exists
const Node& Webgraph::getNodeFromLink(const std::string &url_) const {
    uint i = 0;
    for (; i<all_nodes.size(); ++i) {
        if (all_nodes[i].getUrl() == url_) { break; }
    }
    return all_nodes[i];
}

// Assume the provided node exists
const std::vector<Node>& Webgraph::getIncomingNodes(const Node &n) const {
    return n.getParents();
}

// Assume the provided node exists
const std::vector<Node>& Webgraph::getOutgoingNodes(const Node &n) const {
    return n.getChildren();
}

bool Webgraph::addLink(const string &url_) {
    if (hasLink(url_)) { return false; }
    Node n(url_);
    all_nodes.push_back(n);
    adj_matrix[n] = vector<Node>();
    return true;
}

bool Webgraph::addConnection(const std::string &from_url,
                                const std::string &to_url) {
    if (hasLink(from_url) == false) {
        addLink(from_url);
    }
    if (hasLink(to_url) == false) {
        addLink(to_url);
    }
    // update Node info
    Node n_from = getNodeFromLink(from_url);
    Node n_to = getNodeFromLink(to_url);
    bool added = n_from.addChild(n_to);
    n_to.addParent(n_from);
    // update adj matrix
    if (added == false) { return false; }
    adj_matrix[n_from].push_back(n_to);
    return true;
}
