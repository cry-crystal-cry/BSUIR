#include <iostream>
#include <math.h>
using namespace std;

double min(double el1, double el2)
{
	if (el1 > el2) return el2;
	else return el1;
}

double max(double el1, double el2)
{
	if (el1 > el2) return el1;
	else return el2;
}




int main() 
{ //lab2.1
	double z, b, x, z1;
	cout << "enter Z:";
	cin >> z;
	if (z <= 0) {
		cin >> b;
		cout << "z<=0 --> x=Z^b-|b/2|" << endl;
		x = pow(z, b) + abs(b / 2);
	}
	else {
		cout << "z>0 --> x=sqrt(z)" << endl;
		x = sqrt(z);
	}
	if ((cos(x) == 0) || (cos(x / 2) == 0) || (sin(x / 2) == 0))
		cout << "not ODZ" << endl;
	else {
		z1 = 1 / cos(x) + log(abs(sin(x / 2) / cos(x / 2)));
		cout << "Result: " << z1 << endl;
	}

	//lab2.2
	system("pause");
	z = b = x = z1 = 0;
	double fx,a;
	short choose;
	cout << "enter Z:" << endl;
	while (!(std::cin >> z)){
		std::cout << "ATTENTION FIRE ALARM WORKERS AND CUSTOMERS PLEASE LEAVE THE BUILDING ACCORDING TO THE EVACUATION PLAN" << std::endl;
		std::cin.clear();
		std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); //MAGIIIIIIIC
	}
	cout << "enter B:" << endl;
	while (!(std::cin >> b)) {
		std::cout << "ATTENTION FIRE ALARM WORKERS AND CUSTOMERS PLEASE LEAVE THE BUILDING ACCORDING TO THE EVACUATION PLAN" << std::endl;
		std::cin.clear();
		std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); //MAGIIIIIIIC
	}
	cout << "enter A:" << endl;
	while (!(std::cin >> a)) {
		std::cout << "ATTENTION FIRE ALARM WORKERS AND CUSTOMERS PLEASE LEAVE THE BUILDING ACCORDING TO THE EVACUATION PLAN" << std::endl;
		std::cin.clear();
		std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); //MAGIIIIIIIC
	}
	if (z <= 0) {
		cout << "z<=1 --> x=z*z/2" << endl;
		x = z * z / 2;
	}
	else {
		cout << "z>0 --> x=sqrt(z)" << endl;
		x = sqrt(z);
	}
	cout << "switch the function:" << endl;
	cout << "1) F(x)=2x" << endl;
	cout << "2) F(x)=x^2" << endl;
	cout << "3) F(x)=x/3" << endl;

	while (!(std::cin >> choose)||(choose>3)||(choose<1)) {
		std::cout << "ATTENTION FIRE ALARM WORKERS AND CUSTOMERS PLEASE LEAVE THE BUILDING ACCORDING TO THE EVACUATION PLAN" << std::endl;
		std::cin.clear();
		std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); //MAGIIIIIIIC
	}
	switch (choose) {
		case 1:
			cout << "ur choose is: F(x)=2x" << endl;
			fx = x * 2;
			break;
		case 2:
			cout << "ur choose is: F(x)=x^2" << endl;
			fx = x * x;
			break;
		case 3:
			cout << "ur choose is: F(x)=x/3" << endl;
			fx = x / 3;
			break;
		}
	if ((cos(x) == 0) || (sin(x / 2) == 0) || (cos(x / 2) == 0)) {
		cout << "not ODZ" << endl; 
	}
	else {
		z1 = b * fx / cos(x) + a * log(abs(sin(x / 2) / cos(x / 2)));
		cout << "Result= " << z1 << endl;
	}

	////lab2.3
	system("pause");
	double y, m;
	x = z = 0;
	cout << "enter X:" << endl;
	while (!(std::cin >> x)) {
		std::cout << "ATTENTION FIRE ALARM WORKERS AND CUSTOMERS PLEASE LEAVE THE BUILDING ACCORDING TO THE EVACUATION PLAN" << std::endl;
		std::cin.clear();
		std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); //MAGIIIIIIIC
	}
	cout << "enter Y:" << endl;
	while (!(std::cin >> y)) {
		std::cout << "ATTENTION FIRE ALARM WORKERS AND CUSTOMERS PLEASE LEAVE THE BUILDING ACCORDING TO THE EVACUATION PLAN" << std::endl;
		std::cin.clear();
		std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); //MAGIIIIIIIC
	}
	cout << "enter Z:" << endl;
	while (!(std::cin >> z)) {
		std::cout << "ATTENTION FIRE ALARM WORKERS AND CUSTOMERS PLEASE LEAVE THE BUILDING ACCORDING TO THE EVACUATION PLAN" << std::endl;
		std::cin.clear();
		std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); //MAGIIIIIIIC
	}
	double proverka;
	proverka = min(min(x, y), min(y, z));
	if (proverka == 0) cout << "division by 0";
	else {
		m = max(y, z) / proverka;
		cout << "Result= " << m << endl;
	}
}