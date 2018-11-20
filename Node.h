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
    std::string timestamp;
    std::vector<std::string> children;  // outgoing connections
    std::vector<std::string> parents;   // incoming connections
public:
    // Constructor
    Node(const std::string &url_);
    // Accessor
    const std::string& getUrl() const;
    float getRank() const;
    const std::string& getTimestamp() const;
    const std::vector<std::string>& getChildren() const;
    const std::vector<std::string>& getParents() const;
    bool hasChild(const std::string &child_) const;
    bool hasParent(const std::string &parent_) const;
    // Modifier
    bool addChild(const std::string &child_);
    bool addParent(const std::string &parent_);
    void updateRank(const float rank_);
    void updateTimestamp(const std::string &timestamp_);
    // Operator
    bool operator<(const Node &n) const;
    bool operator==(const Node &n) const;
};
#endif
