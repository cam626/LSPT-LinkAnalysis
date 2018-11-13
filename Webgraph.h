#ifndef WEBGRAPH_H
#define WEBGRAPH_H

#include <vector>
#include <string>
#include <set>
#include <map>

/* Node class */
class Node {
private:
    std::string url;
    std::vector<Node> children;  // outgoing connections
public:
    /* Constructor */
    Node(const std::string &url_) : url(url_) {}
    /* Accessor */
    const std::string& getUrl() const { return url; }
    const std::vector<Node>& getChildren() const;
    /* Modifier */
    void addChild(const Node &child_) { children.push_back(child_); }
};

/* Webgraph class */
class Webgraph {
private:
    std::set<Node> all_links;
    std::map< Node, std::vector<Node> > adj_matrix;

public:
    // Webgraph();
    // ~Webgraph();
    /* Accessor */
    const std::set<Node>& getAllLinks() const { return all_links; }
    bool hasLink(const std::string &url_) const;
    /* Modifier */
    void addLink(const std::string &url_);
    void addConnection(const std::string &from_url, const std::string &to_url);
};
#endif
