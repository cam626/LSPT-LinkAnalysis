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
    std::vector<Node> all_links;
    std::map< Node, std::vector<Node> > adj_matrix;

public:
    // Accessor
    const std::vector<Node>& getAllLinks() const;
    bool hasLink(const std::string &url_) const;
    const Node& getNode(const std::string &url_) const;
    // TODO:
    //   1. get all ranks
    //   2. check timestamp

    // Modifier
    void addLink(const std::string &url_);
    void addConnection(const std::string &from_url, const std::string &to_url);
};
#endif
