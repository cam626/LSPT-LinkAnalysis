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

const vector<Node>& Node::getChildren() const {
    return children;
}

bool Node::hasChild(const Node &child_) const {
    for (int i=0; i<children.size(); ++i) {
        if (children[i].getUrl() == child_.getUrl()) {
            return true;
        }
    }
    return false;
}

void Node::addChild(const Node &child_) {
    children.push_back(child_);
}

void Node::updateRank(const int rank_) {
    rank = rank_;
}

bool Node::operator< (const Node &n) const {
    return url < n.getUrl();
}
