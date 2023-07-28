#include <iostream>
#include "treap.h"



int main() {
    CartesianTree tree1;
    tree1.insert(1);
    tree1.insert(26);
    tree1.insert(5);
    tree1.insert(57);
    tree1.insert(5);
    tree1.insert(6);
    tree1.insert(7);
    tree1.print();

    CartesianTree tree2;
    tree2.insert(23);
    tree2.insert(12);
    tree2.insert(94);
    tree2.insert(9);
    tree2.print();

    tree1.merge(tree2);
    tree1.print();

    CartesianTree tree3;
    int values[] = { 23, 57, 12, 9, 5, 6, 7, 8, 94 };
    tree3.build(values, sizeof(values) / sizeof(int));
    tree3.print();

    cout << "Search 1 in tree1 = " << tree1.search(1) << endl;
    tree1.remove(1);
    tree1.print();

    tree1.intersect(tree3);
    tree1.print(); 

    return 0;
}