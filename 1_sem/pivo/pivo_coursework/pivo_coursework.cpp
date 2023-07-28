#define _CRT_SECURE_NO_WARNINGS
#include <iostream>
#include <vector>
#include <queue>


using namespace std;

int main()
{
	cout << "enter the path to the file: ";
	char path[100];
	cin >> path;
	FILE* in = fopen(path, "r"), * out = fopen("out.txt", "w");
	while (in == NULL) {
		cout << "enter the path to the file: ";
		cin >> path;
		in = fopen(path, "r");
	}

	vector<vector<int>> vec;
	int edge, point1, point2, maxpoint = -1;;

	while (fscanf(in, "%d: %d %d", &edge, &point1, &point2) != EOF) {
		vec.resize(edge);
		vec[edge - 1].resize(2);
		vec[edge - 1][0] = point1;
		vec[edge - 1][1] = point2;
		maxpoint = max(point1, max(maxpoint, point2));
	}
	// cout << vec.size() << endl;
	cout << "This is you graph:\n";
	for (int i = 0; i < vec.size(); i++)
		cout << i + 1 << ": " << vec[i][0] << " " << vec[i][1] << endl;


	vector<vector<int>> newvec(maxpoint);
	//convert List of incidence to Adjacency list
	for (int i = 0; i < vec.size(); i++) {
		newvec[vec[i][0] - 1].push_back(vec[i][1] - 1);
		newvec[vec[i][1] - 1].push_back(vec[i][0] - 1);
		if (newvec[vec[i][1] - 1] == newvec[vec[i][0] - 1])
			newvec[vec[i][1] - 1].pop_back(); //if edge is loop
	}

	vec.clear();
	/*cout << "new format:" << endl;

	for (int i = 0; i < newvec.size(); i++) {
		cout << i + 1 << ": ";
		for (int j = 0; j < newvec[i].size(); j++) {
			cout << newvec[i][j] + 1 << " ";
		}
		cout << "\n";
	}*/

	queue<int> q;
	int max_len = -1;
	for (int everypoint = 0; everypoint < newvec.size(); everypoint++) {
		q.push(everypoint);
		vector<bool> used(newvec.size(), false);
		vector<int> len(newvec.size(), -1);
		len[everypoint] = 0;
		while (q.empty() == false) {
			int i = q.front();
			q.pop();
			used[i] = true;
			for (int j = 0; j < newvec[i].size(); j++) {
				if (used[newvec[i][j]] == false) {
					q.push(newvec[i][j]);
					len[newvec[i][j]] = len[i] + 1;
					used[newvec[i][j]] = true;
				}

			}
		}
		for (int g = 0; g < len.size(); g++) {
			max_len = max(max_len, len[g]);
		}
	}
	cout << "\n Diameter of this graph is equal to " << max_len << endl;
	fprintf(out, "Diameter of this graph is equal to %d", max_len);


	fclose(in);
	fclose(out);
	return 0;
}//ilysha molodec