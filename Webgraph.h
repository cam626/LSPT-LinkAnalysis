// Webgraph.h
// Author: Jinwei Shen
//
// Header file for the Webgraph class

#ifndef WEBGRAPH_H
#define WEBGRAPH_H

#include <vector>
#include <string>
#include <set>
#include <map>

#include "Node.h"

class Webgraph {
private:
    std::vector<Node> all_nodes;
    std::map< Node, std::vector<Node> > adj_matrix;

public:
    // Accessor
    const std::vector<Node>& getAllNodes() const;
    bool hasLink(const std::string &url_) const;
    const Node& getNodeFromLink(const std::string &url_) const;
    const std::vector<Node>& getIncomingNodes(const Node &n) const;
    const std::vector<Node>& getOutgoingNodes(const Node &n) const;
    // TODO:
    //   1. get all ranks
    //   2. check timestamp

    // Modifier
    bool addLink(const std::string &url_);
    bool addConnection(const std::string &from_url, const std::string &to_url);
};
#endif
