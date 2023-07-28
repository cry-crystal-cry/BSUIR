#include <iostream>

using namespace std;

double radical(long double a,long double rad) {
    if (a > 0) {
        rad = sqrt(rad)+(--a);
        radical(a, rad);
    }
    else {
        return rad;
    }

}

int main() {
    long double rad1 = 0, rad2 = 0, a;
    while (!(std::cin >> a) || (a < 1) || (a > 3000)) {
        std::cout << "ATTENTION FIRE ALARM WORKERS AND CUSTOMERS PLEASE LEAVE THE BUILDING ACCORDING TO THE EVACUATION PLAN" << std::endl;
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); //MAGIIIIIIIC
    }
   
    for (int i = a; i >= 1; i--) {
        rad2 = sqrt(i + rad2);
    }
        
    rad1= radical(a, a);
    cout << "recursion: " << rad2 << "\t function: " << rad2 << "\t diff: " << abs(rad1 - rad2);

}