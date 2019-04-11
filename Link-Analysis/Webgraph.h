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
#include <queue>
#include <cmath>
#include <utility>

#include "Node.h"

class Webgraph
{
private:
  float rank_threshold = 0.0001;
  float damping_factor = 0.85;
  std::vector<Node> all_nodes;
  void updateHelper(std::queue<unsigned int> work_queue);
  unsigned int getNodeIndexFromLink(const std::string &url_) const;
  const std::vector<std::string> &getIncomingLinks(const Node &n) const;
  const std::vector<std::string> &getOutgoingLinks(const Node &n) const;

public:
  // Accessor
  const Node &getNodeFromLink(const std::string &url_) const;
  const std::vector<Node> &getAllNodes() const;
  bool hasLink(const std::string &url_) const;
  const std::map<std::string, std::pair<float, float>> getAllRanks() const;
  // TODO:
  //   1. check timestamp

  // Modifier
  bool addLink(const std::string &url_);
  bool addConnection(const std::string &from_url, const std::string &to_url);
  void updateRank(const std::string &url_);
};
#endif
