// Node.h
// Author: Jinwei Shen
//
// Header file for the Node class

#ifndef NODE_H
#define NODE_H

#include <string>
#include <vector>

class Node {
private:
    std::string url;
    float rank;
    // TODO: timestamp format ???
    std::vector<Node> children;  // outgoing connections
public:
    // Constructor
    Node(const std::string &url_);
    // Accessor
    const std::string& getUrl() const;
    const std::vector<Node>& getChildren() const;
    bool hasChild(const Node &child_) const;
    // TODO: funcion to check timestamp expiration
    // Modifier
    void addChild(const Node &child_);
    void updateRank(const int rank_);
    // TODO: function to update timestamp
    // Operator
    bool operator< (const Node &n) const;
};
#endif
