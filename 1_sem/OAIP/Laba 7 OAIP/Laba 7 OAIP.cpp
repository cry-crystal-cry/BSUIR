#include <iostream>
#include <fstream>


using namespace std;

int main() {
	setlocale(LC_ALL, "Russian");

	ifstream in;
	ofstream out;
	char str[1000];
	//				SAVE INPUT FILE IN ANSI CODING	
	//					NOT IN UTF-8 
	//					!!!!!!!!!
	try {
		cout << "enter the path to the file: ";
		char path[1000];
		cin >> path;
		in.open(path);
		out.open("output.txt");
		in.getline(str, 1000);
		if (!in.is_open()|| !out.is_open())  throw 1; 
		int i = 0;

		while (str[i] != '\0')
		{
			switch (str[i]) {
			case 'а':
				str[i] = 'ц';
				i++;
				break;
			case 'А':
				str[i] = 'Ц';
				i++;
				break;
			case 'о':
				str[i] = 'ш';
				i++;
				break;
			case 'О':
				str[i] = 'Ш';
				i++;
				break;
			case 'и':
				str[i] = 'щ';
				i++;
				break;
			case 'И':
				str[i] = 'Щ';
				i++;
				break;
			default:
				i++;
			}
		}

	}
		catch (...) {
			cout << "the file doesn't open\t";
			return 0;
		}
		out << str;
		cout << str;


	in.close();
	out.close();
	return 0;
}
//   C:\Users\USER\Desktop\34.txt