#include <iostream>
#include <math.h>

using namespace std;

int main()
{
    //lab1.1
    const double PI = 3.1415926;
    double alf, z1 = 0, z2 = 0;
   cin >> alf;
    if (((sin(3 * alf - PI)) == 1) || ((sin(5. / 4 * PI + 3. / 2 * alf)) == 0)) { cout << "divide by zero" << endl; }
    else {
        z1 = sin(PI / 2. + 3 * alf) / (1 - sin(3 * alf - PI));
        z2 = cos(5. / 4 * PI + 3. / 2 * alf) / sin(5. / 4 * PI + 3. / 2 * alf);
    }
    cout <<"z1="<< z1 << " " <<"z2="<< z2 << "\t dif = " << z1 - z2 << endl;



 /*   for (double a = 0; a < 100; a+=0.1) {
        if (((sin(3 * a - PI)) == 1) || ((sin(5. / 4 * PI + 3. / 2 * a)) == 0)) { cout << "divide by zero" << endl; }
        else {
            z1 = sin(PI / 2. + 3 * a) / (1 - sin(3 * a - PI));
                z2 = cos(5. / 4 * PI + 3. / 2 * a) / sin(5. / 4 * PI + 3. / 2 * a);
                cout << "Attempt: " << a * 10 << "\t" << z1 - z2 << endl;
        }
    }*/

    //lab1.2
    system("pause");
    int a = 0;
    while (!(std::cin >> a) ||
        (a > (-3) && a <= 3)) {
        std::cout << "ATTENTION FIRE ALARM WORKERS AND CUSTOMERS PLEASE LEAVE THE BUILDING ACCORDING TO THE EVACUATION PLAN" << std::endl;
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); //MAGIIIIIIIC
    }
    z1 = (a * a + 2 * a - 3 + (a + 1) * sqrt(a * a - 9)) / (a * a - 2 * a - 3 + (a - 1) * sqrt(a * a - 9));
    z2 = sqrt((a + 3) / (a - 3));
    cout << "Attempt: " << "\t" << z1 - z2 << endl;

    //lab1.3
    system("pause");
    double x, y, z;
    while (!(std::cin >> x) || x == 0) {
        std::cout << "ATTENTION FIRE ALARM WORKERS AND CUSTOMERS PLEASE LEAVE THE BUILDING ACCORDING TO THE EVACUATION PLAN" << std::endl;
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); //MAGIIIIIIIC
    }
    while (!(std::cin >> y) || y == x) {
        std::cout << "ATTENTION FIRE ALARM WORKERS AND CUSTOMERS PLEASE LEAVE THE BUILDING ACCORDING TO THE EVACUATION PLAN" << std::endl;
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); //MAGIIIIIIIC
    }
    while (!(std::cin >> z)) {
        std::cout << "ATTENTION FIRE ALARM WORKERS AND CUSTOMERS PLEASE LEAVE THE BUILDING ACCORDING TO THE EVACUATION PLAN" << std::endl;
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); //MAGIIIIIIIC
    }

    z1 = abs(pow(x, y / x) - cbrt(y / x)) + (y - x) * (cos(y) - z / (y - x)) / (1 + pow(y - x, 2));
    cout << z1;

}