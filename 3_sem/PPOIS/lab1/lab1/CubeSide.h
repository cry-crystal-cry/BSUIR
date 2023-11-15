#pragma once
#include <iostream>
#include <vector>

using namespace std;

class CubeSide {
private:
	static const int SIZE = 3;
	char** side;
	char* charBuff;	//buff to store values from columns or lines, used in [get/set][Colomn/Line]
	static char* getReverseChar(char*);
	void showLine(const int&);	//need to use in showCubeCrossForSide() function
	void setLine(const int&, const char*);
	void setColumn(const int&, const char*);
	char* getLine(const int&);
	char* getColumn(const int&);
	char getChar(const int&, const int&);
	void chekColors(int&, int&, int&, int&, int&, int&);
	friend class RubiksCube;
public:
	CubeSide();
	~CubeSide();
	void setSide(const vector<char>&);
	void showSide();
	void rotateSide();			
	void backRotateSide();
	CubeSide* up;
	CubeSide* down;
	CubeSide* left;
	CubeSide* right;
	bool operator==(CubeSide&);
};
