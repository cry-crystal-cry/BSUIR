#include <iostream>

double rec(int a, int count) {
	if (count == 0) return 0.5 * (1 + a);
	return 0.5 * (rec(a, count - 1) + a / rec(a, count - 1));
}

int main() {
	int a;
	std::cin >> a;
	if (a == 0)std::cout<<"4e samyj umnyj?\n";

	double rez = 0.5 * (1 + a);
	for (int i = 0; i < a; i++) {
		rez = 0.5 * (rez + a / rez);
	}


	std::cout << rec(a, a) << std::endl << rez;
}