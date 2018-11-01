#ifndef WEBGRAPH_H
#define WEBGRAPH_H

#include <string>
#include <set>

/* Node class */
class Node {
private:
    std::string url;
public:
    Node(/* args */) { }
    ~Node() { }
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
