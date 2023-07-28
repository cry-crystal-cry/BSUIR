#include <iostream>
#include <math.h>
#include <vector>

using namespace std;

void print(std::string* a, int n, int i, vector<vector<string>>* rez, int count) {
    if (n)
    {
        if (n % 2)
            (*rez)[count].push_back(a[i]);
        print(a, n / 2, ++i, rez, count);
    }
}

int main() {
    int r, i, size, count = 0;
    std::string a[] = { "A","a3","b3_A","<1,2>","{1,2,3,4}" };
    size = sizeof(a) / sizeof(*a);
    r = pow(2, size);
    vector<vector<string>> rez;
    rez.resize(r);
    for (i = 0; i < r; i++) {
        print(a, i, 0, &rez, count);
        count++;
    }

    cout << "{";
    for (i = 0; i < r; i++) {
        cout << "{ ";
        for (int j = 0; j < rez[i].size(); j++)
            cout << rez[i][j] << ", ";
        cout << "\b\b }" << endl;
    }

}