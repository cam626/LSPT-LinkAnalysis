#ifndef WEBGRAPH_H
#define WEBGRAPH_H

#include <vector>
#include <string>
#include <set>

/* Node class */
class Node {
private:
    std::string url;
    std::vector<Node> children;  // outgoing connections
public:
    Node(const std::string &url_) : url(url_) {}
    const void addChild(const Node &child_) { children.push_back(child_); }
    const std::vector<Node> &getChildren() const;
    // ~Node() { }
};

/* Webgraph class */
class Webgraph {
private:
    std::set<Node> link_set;
public:
    Webgraph(/* args */);
    ~Webgraph();
};
#endif
