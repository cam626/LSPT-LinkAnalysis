// Node.cpp
// Author: Jinwei Shen
//
// Implementation of Node class functions

#include <vector>
#include <string>

#include "Node.h"

typedef unsigned int uint;

using namespace std;

Node::Node(const string &url_, const time_t timestamp_)
{
    url = url_;
    rank = 1.0;
    timestamp = timestamp_;
}

const string &Node::getUrl() const
{
    return url;
}

float Node::getRank() const
{
    return rank;
}

const time_t &Node::getTimestamp() const
{
    return timestamp;
}

const vector<string> &Node::getChildren() const
{
    return children;
}

const std::vector<string> &Node::getParents() const
{
    return parents;
}

bool Node::hasChild(const string &child_) const
{
    for (uint i = 0; i < children.size(); ++i)
    {
        if (children[i] == child_)
        {
            return true;
        }
    }
    return false;
}

bool Node::hasParent(const string &parent_) const
{
    for (uint i = 0; i < parents.size(); ++i)
    {
        if (parents[i] == parent_)
        {
            return true;
        }
    }
    return false;
}

bool Node::addChild(const string &child_)
{
    if (hasChild(child_))
    {
        return false;
    }
    children.push_back(child_);
    return true;
}

bool Node::addParent(const string &parent_)
{
    if (hasParent(parent_))
    {
        return false;
    }
    parents.push_back(parent_);
    return true;
}

void Node::updateRank(const float rank_)
{
    rank = rank_;
}

void Node::updateTimestamp(const time_t timestamp_)
{
    timestamp = timestamp_;
}

bool Node::operator<(const Node &n) const
{
    return url < n.getUrl();
}

bool Node::operator==(const Node &n) const
{
    return url == n.getUrl();
}
