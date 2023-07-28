#include <iostream>
#include <stdio.h>

using namespace std;

int main() {
	char str[1000];
	int len, strint[500];
	gets_s(str,1000);

	len = strlen(str);

	for (int i = (len - 1); i >= 0; i--) {//delete multi' ' and text

		if (str[i] == ' ') {
			if (str[i + 1] == ' ') {
				for (int j = i; j < len; j++) {
					str[j] = str[j + 1];
				}
				len -= 1;
				i++;
			}
		}
		else {
			if ((str[i] < '0') || (str[i] > '9')) {

				for (int j = i; j < len; j++) 
					str[j] = str[j + 1];
				len -= 1;
			}
		}
	}

	if (str[len - 1] == ' ') 
		str[--len] = '\0';

	if (str[0] == ' ') {
		for (int j = 0; j < len; j++)
			str[j] = str[j + 1];
		len--;
	}


	/*for (int i = 0; i < len; i++)cout << str[i]; cout << "!!!";
	cout << endl;
	cout << "!!!!"<<len;
	cout << endl;*/

	int lenint = -1, value=0;
	str[++len] = '\0'; 
	str[len-1] = ' ';

	if ((len == 1 && str[0] == ' ') || ((len == 2)) && (str[0] == ' ') && (str[1] == ' ')) {
		cout << "there is no numbers";
		return 0;
	}

	for (int i = 0; i < len ; i++){
		if (str[i] == ' ') {
			strint[++lenint] = value;
			value = 0;
		}
		else {
			value = value * 10 + str[i] - '0';
		}
	}

	for (int i = 0; i < lenint; i++) {
		for (int j = i + 1; j < lenint+1; j++) {
			if (strint[i] > strint[j]) {
				int swap = strint[i];
				strint[i] = strint[j];
				strint[j] = swap;
			}
		}
	}

	for (int i = 0; i <= lenint; i++)cout << strint[i] << " ";

	return 0;
}