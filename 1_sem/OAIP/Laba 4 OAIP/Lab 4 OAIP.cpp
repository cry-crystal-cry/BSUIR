#include <iostream>
#include <math.h>
#include <conio.h>

using namespace std;

int random(int from, int to) {
	return rand() % (to - from + 1) + from;
}



int main() 
{
	srand(time(0));
	random(1, 10000); //to make 1 elemont more different

	bool work = true;
	int count, min_ind, last = -1;
	double sum = 0, min;
	

	cout << "enter number of array elements:" << endl;
	while (!(cin >> count) || (count <= 0)) {
		std::cout << "ATTENTION FIRE ALARM WORKERS AND CUSTOMERS PLEASE LEAVE THE BUILDING ACCORDING TO THE EVACUATION PLAN" << std::endl;
		std::cin.clear();
		std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); //MAGIIIIIIIC
	}
	cout << endl;
	double* a = new double[count];

		do {
			cout << "enter by yourself - press \"1\"" << endl;
			cout << "random enter - press \"2\"" << endl;
			cout << "press \"3\" to exit" << endl;
			cout << endl;
			switch (_getch()) {
					
			case '1':
				work = false;
						
				cout << "enter array elements:" << endl;
				for (int i = 0; i < count; i++) {
					while (!(cin >> a[i])) {
						std::cout << "ATTENTION FIRE ALARM WORKERS AND CUSTOMERS PLEASE LEAVE THE BUILDING ACCORDING TO THE EVACUATION PLAN" << std::endl;
						std::cin.clear();
						std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); //MAGIIIIIIIC
					}
				}

				min = a[0];
				min_ind = 0; //dibil

				for (int i = 0; i < count; i++) {
					if (a[i] < 0) last = i;
					if (a[i] < min) {
						min = a[i];
						min_ind = i;
					}
				}

				if (last == -1) {
					cout << "there is no negative numbers" << endl;
					break;
				}
				if (abs(last - min_ind) <= 1) {
					cout << "there is no number between last negative number and minimal number" << endl;
					break;
				}

				for (int i = min_ind + 1; i < last; i++) 
					sum += abs(a[i]);

				cout << "sum= " << sum << endl;
				break;
			case '2':
				work = false;
				
				cout << "this is your array elements:" << endl;
				for (int i = 0; i < count; i++) {
					a[i] = random(-1000, 1000);
					cout << a[i] << " ";
				}
				cout << endl;

				 min = a[0];
				 min_ind = 0;

				for (int i = 0; i < count; i++) {
					if (a[i] < 0) last = i;
					if (a[i] < min) {
						min = a[i];
						min_ind = i;
					}
				}

				if (last == -1) {
					cout << "there is no negative numbers" << endl;
					break;
				}
				if (abs(last - min_ind) <= 1) {
					cout << "there is no number between last negative number and minimal number" << endl;
					break;
				}

				for (int i = min_ind + 1; i < last; i++) {
					sum += abs(a[i]);
				}

				cout << "sum= " << sum << endl;
				break;
			case '3':
				return 0;
				break;
			default:
				cout << "ATTENTION FIRE ALARM..." << endl;

			}
		} 
	while (work == true);


		delete[] a;
		a = 0;

		return 0;
}