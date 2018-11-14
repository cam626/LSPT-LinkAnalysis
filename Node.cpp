// Node.cpp
// Author: Jinwei Shen
//
// Implementation of Node class functions

#include <vector>
#include <string>

#include "Node.h"

using namespace std;

Node::Node(const string &url_ ) {
    url = url_;
    rank = 0; // TODO: ? initial value
    // TODO: initialize timestamp
}

const string& Node::getUrl() const {
    return url;
}

float Node::getRank() const {
    return rank;
}

const std::string& Node::getTimestamp() const {
    return timestamp;
}

const vector<Node>& Node::getChildren() const {
    return children;
}

const std::vector<Node>& Node::getParents() const {
    return parents;
}

bool Node::hasChild(const Node &child_) const {
    for (int i=0; i<children.size(); ++i) {
        if (children[i].getUrl() == child_.getUrl()) {
            return true;
        }
    }
    return false;
}

bool Node::hasParent(const Node &parent_) const {
    for (int i=0; i<parents.size(); ++i) {
        if (parents[i].getUrl() == parent_.getUrl()) {
            return true;
        }
    }
    return false;
}

bool Node::addChild(const Node &child_) {
    if (hasChild(child_)) { return false; }
    children.push_back(child_);
    return true;
}

bool Node::addParent(const Node &parent_) {
    if (hasParent(parent_)) { return false; }
    parents.push_back(parent_);
    return true;
}

void Node::updateRank(const int rank_) {
    rank = rank_;
}

void Node::updateTimestamp(const std::string &timestamp_) {
    timestamp = timestamp_;
}


bool Node::operator<(const Node &n) const {
    return url < n.getUrl();
}
