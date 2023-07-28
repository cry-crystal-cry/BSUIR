#pragma once
#include <iostream>

using namespace std;

struct Node {
    int value;
    int priority;
    Node* left;
    Node* right;
    Node(int value) : value(value), priority(rand()), left(nullptr), right(nullptr) {}
};

class CartesianTree {
private:
    Node* root;

    void split(Node* current, int value, Node*& left, Node*& right);
    Node* merge(Node* left, Node* right);
    void insert(Node*& current, int value);
    bool search(Node* current, int value);
    void remove(Node*& current, int value);
    void build(Node*& current, int* values, int size);
public:
    CartesianTree() : root(nullptr) {};
    void insert(int value);
    bool search(int value);
    void remove(int value);
    void build(int* values, int size);
    void merge(CartesianTree& tree);
    void intersect(CartesianTree& tree);
    void print();
private:
    void print(Node* current);

};