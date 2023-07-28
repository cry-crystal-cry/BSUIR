#include <iostream>
#include "treap.h"


void CartesianTree::split(Node* current, int value, Node*& left, Node*& right)
{
    if (current == nullptr) {
        left = nullptr;
        right = nullptr;
    }
    else if (current->value <= value) {
        split(current->right, value, current->right, right);
        left = current;
    }
    else {
        split(current->left, value, left, current->left);
        right = current;
    }
}

Node* CartesianTree::merge(Node* left, Node* right)
{
    if (left == nullptr || right == nullptr) {
        return left == nullptr ? right : left;
    }
    else if (left->priority > right->priority) {
        left->right = merge(left->right, right);
        return left;
    }
    else {
        right->left = merge(left, right->left);
        return right;
    }
}

void CartesianTree::insert(Node*& current, int value)
{
    Node* node = new Node(value);
    current = merge(current, node);
}

bool CartesianTree::search(Node* current, int value) {
        if (current == nullptr) {
            return false;
        }
        else if (current->value == value) {
            return true;
        }
        else if (current->value < value) {
            return search(current->right, value);
        }
        else {
            return search(current->left, value);
        }
    }

    void CartesianTree::remove(Node*& current, int value) {
        if (current == nullptr) {
            return;
        }
        else if (current->value == value) {
            Node* node = current;
            current = merge(current->left, current->right);
            delete node;
        }
        else if (current->value < value) {
            remove(current->right, value);
        }
        else {
            remove(current->left, value);
        }
    }

    void CartesianTree::build(Node*& current, int* values, int size) {
        for (int i = 0; i < size; i++) {
            insert(current, values[i]);
        }
    }

    void CartesianTree::insert(int value) {
        insert(root, value);
    }

    bool CartesianTree::search(int value) {
        return search(root, value);
    }

    void CartesianTree::remove(int value) {
        remove(root, value);
    }

    void CartesianTree::build(int* values, int size) {
        build(root, values, size);
    }

    void CartesianTree::merge(CartesianTree& tree) {
        root = merge(root, tree.root);
        tree.root = nullptr;
    }

    void CartesianTree::intersect(CartesianTree& tree) {
        CartesianTree result;
        Node* current = root;
        while (current != nullptr) {
            if (tree.search(current->value)) {
                result.insert(current->value);
            }
            if (current->value <= tree.root->value) {
                current = current->right;
            }
            else {
                current = current->left;
            }
        }
        root = result.root;
    }

    void CartesianTree::print() {
        cout << "Cartesian Tree: ";
        print(root);
        cout << endl;
    }

    void CartesianTree::print(Node* current) {
        if (current != nullptr) {
            print(current->left);
            cout << "(" << current->value << ", " << current->priority << ") ";
            print(current->right);
        }
    }