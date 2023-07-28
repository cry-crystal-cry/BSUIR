#include <iostream>
#include <math.h>

using namespace std;

int main()
{
    double a, b, h, S = 0, Y, Sx, x, k;
    int n;
    cout << "enter a:";
    while (!(std::cin >> a)) {
        std::cout << "SET ERROR" << std::endl;
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); //MAGIIIIIIIC
    }
    cout << "enter b:";
    while (!(std::cin >> b)) {
        std::cout << "SET ERROR" << std::endl;
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); //MAGIIIIIIIC
    }
    cout << "enter h:";
    while (!(std::cin >> h) || (h == 0) || (((a - b) / h) > 0)) {
        std::cout << "SET ERROR" << std::endl;
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); //MAGIIIIIIIC
    }
    cout << "enter n:";
    while (!(std::cin >> n) || (n < 1)) {
        std::cout << "SET ERROR" << std::endl;
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); //MAGIIIIIIIC
    }

    if ((a - b) <= 0) {
        for (x = a; x <= b; x += h) {
            Y = (1 + x * x) / 2 * atan(x) - x / 2;
            for (k = 1; k <= n; k++) {
                Sx = pow(-1, k + 1) * pow(x, 2 * k + 1) / (4 * k * k - 1);
                S += Sx;
            }
            cout << "Y(x)= " << Y << "\tS(x)= " << S << "\tdiff= " << abs(S - Y) << endl;;
        }
    }
    else {
        for (x = a; x >= b; x += h) {
            Y = (1 + x * x) / 2 * atan(x) - x / 2;
            for (k = 1; k <= n; k++) {
                Sx = pow(-1, k + 1) * pow(x, 2 * k + 1) / (4 * k * k - 1);
                S += Sx;
            }
            cout << "Y(x)= " << Y << "\tS(x)= " << S << "\tdiff= " << abs(S - Y) << endl;;
        }

    }

}
