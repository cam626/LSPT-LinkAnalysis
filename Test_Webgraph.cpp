// This is a test file for functions in Node and Webgraph class
//
// Author: Jinwei Shen

#include <cassert>
#include <vector>
#include <string>
#include <iostream>

#include "Node.h"
#include "Webgraph.h"

typedef unsigned int uint;

using namespace std;

void test_node(vector<Node> nodes) {
    cout << "Begin testing Node class functions ..." << endl;
    cout << "Testing getUrl function ...\t\t";
    for (uint i=0; i<nodes.size(); ++i) {
        string url = to_string(i);
        assert (nodes[i].getUrl() == url);
    }
    cout << "Pass" << endl;

    cout << "Testing initial ranks ...\t\t";
    for (uint i=0; i<nodes.size(); ++i) {
        assert (nodes[i].getRank() == 1);
    }
    cout << "Pass" << endl;

    cout << "Testing updated ranks ...\t\t";
    for (uint i=0; i<nodes.size(); ++i) {
        nodes[i].updateRank(i*1.0);
    }
    for (uint i=0; i<nodes.size(); ++i) {
        assert (nodes[i].getRank() == i*1.0);
    }
    cout << "Pass" << endl;

    cout << "Testing hasChild function ...\t\t";
    Node n = nodes[0];
    string url = "child";
    Node child(url);
    assert (n.hasChild(child) == false);
    cout << "Pass" << endl;

    cout << "Testing addChild function ...\t\t";
    assert (n.addChild(child) == true);
    assert (n.addChild(child) == false);
    assert (n.hasChild(child) == true);
    cout << "Pass" << endl;

    cout << "Testing getChildren function ...\t";
    vector<Node> children;
    children.push_back(child);
    assert (n.getChildren() == children);
    cout << "Pass" << endl;

    cout << "Testing hasParent function ...\t\t";
    Node n1 = nodes[0];
    string url1 = "parent";
    Node parent(url1);
    assert (n1.hasParent(parent) == false);
    cout << "Pass" << endl;

    cout << "Testing addParent function ...\t\t";
    assert (n1.addParent(parent) == true);
    assert (n1.addParent(parent) == false);
    assert (n1.hasParent(parent) == true);
    cout << "Pass" << endl;

    cout << "Testing getParents function ...\t\t";
    vector<Node> parents;
    parents.push_back(parent);
    assert (n1.getParents() == parents);
    cout << "Pass" << endl;
    cout << "All tests for Node class passed!" << endl;
}

void test_webgraph(vector<string> links, vector<Node> nodes) {
    cout << "Begin testing Webgraph class functions ..." << endl;
    Webgraph graph = Webgraph();
    vector<Node> all_nodes;

    cout << "Testing hasLink function ...\t\t";
    assert (graph.hasLink(links[0]) == false);
    cout << "Pass" << endl;

    cout << "Testing addLink function ...\t\t";
    for (uint i=0; i<nodes.size(); ++i) {
        all_nodes.push_back(nodes[i]);
        assert (graph.addLink(links[i]) == true);
        assert (graph.addLink(links[i]) == false);
    }
    assert (graph.hasLink(links[0]) == true);
    cout << "Pass" << endl;

    cout << "Testing getAllNodes function ...\t";
    assert (graph.getAllNodes() == all_nodes);
    cout << "Pass" << endl;

    cout << "Testing getNodeFromLink function ...\t";
    Node n = graph.getNodeFromLink(links[0]);
    assert (n == nodes[0]);
    assert ( (n == nodes[1]) == false );
    cout << "Pass" << endl;

    cout << "All tests for Node class passed!" << endl;
}

int main() {
    // create a vector of urls
    vector<string> link_vec;
    for (int i=0; i<10; ++i) {
        string url = to_string(i);
        link_vec.push_back(url);
    }
    // create a vector of nodes
    vector<Node> node_vec;
    for (uint i=0; i<link_vec.size(); ++i) {
        Node n(link_vec[i]);
        node_vec.push_back(n);
    }
    assert (link_vec.size() == node_vec.size());
    test_node(node_vec);
    test_webgraph(link_vec, node_vec);
    return 0;
}
