#include <iostream>

using namespace std;
int main() {
	int n=0, m=0;
	cout << "enter n: ";
	while (!(cin >> n) || (n <= 0)) {
		std::cout << "ATTENTION FIRE ALARM WORKERS AND CUSTOMERS PLEASE LEAVE THE BUILDING ACCORDING TO THE EVACUATION PLAN" << std::endl;
		std::cin.clear();
		std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); //MAGIIIIIIIC
	}
	cout << "enter m: ";
	while (!(cin >> m) || (m <= 0)) {
		std::cout << "ATTENTION FIRE ALARM WORKERS AND CUSTOMERS PLEASE LEAVE THE BUILDING ACCORDING TO THE EVACUATION PLAN" << std::endl;
		std::cin.clear();
		std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); //MAGIIIIIIIC
	}
	int** a = new int* [n];

	for (int i = 0; i < n; i++) 
		a[i] = new int[m+1];



	for (int i = 0; i < n; i++) { //vvod
		int max = a[i][0];
		for (int j = 0; j < m; j++) {
			
			while (!(cin >> a[i][j])) {
				std::cout << "ATTENTION FIRE ALARM WORKERS AND CUSTOMERS PLEASE LEAVE THE BUILDING ACCORDING TO THE EVACUATION PLAN" << std::endl;
				std::cin.clear();
				std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); //MAGIIIIIIIC

			}
			if (a[i][j] > max) 
				max = a[i][j];
		}
		a[i][m] = max;
	}
	cout << endl;


	for (int i = 0; i < n-1; i++) {//sort
		for (int j = i + 1; j < n; j++) {
			if (a[i][m] > a[j][m]) {
				for (int k = 0; k < m + 1; k++) {
					int swap = a[j][k];
					a[j][k] = a[i][k];
					a[i][k] = swap;
				}
				
			}
		}
	}

	for (int i = 0; i < n; i++) {//vivod
		for (int j = 0; j < m; j++) {
			cout << a[i][j]<<" ";
		}
		cout << endl;
	}


	for (int i = 0; i< n; i++) 
		delete[] a[i];

	delete[] a;


}
