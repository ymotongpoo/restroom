#ifndef BINARY_TREE_H
#define BINARY_TREE_H

#include <iostream>

class Node {
private:
	Node* left;
	Node* right;
	Node* parent;
	int data;
public:
	Node();
	int SetChild(Node* child);
};

class BinaryTree {
private:
	Node* root;
public:
	Node* GetRoot() { return this->root; };
};

#endif
