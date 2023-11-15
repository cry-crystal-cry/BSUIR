#pragma once
#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include "CubeSide.h"

using namespace std;

class RubiksCube
{
private:								//	4
	CubeSide* cube;						//0 1 2 3 scheme of sides lineup 
	void setDependency(CubeSide*);		//	5
	void setCube(const vector<char>&);
	bool chekColors();
	int random(const int&, const int&);
	void showCubeCrossForSideWithoutRotationNeighbourSides(CubeSide&);
	void setNeighboursForSideVision(CubeSide*, int&, int&, int&, int&);
	void setNeighboursBack(CubeSide*, int&, int&, int&, int&);
	void showCubeCrossForSide(CubeSide*);
	void rotateFace(CubeSide*);
	void backRotateFace(CubeSide*);
public:
	RubiksCube();
	~RubiksCube();
	void setRandom();
	void setFromFile(const string&);
	void showCube();
	void showCubeCrossForSide(const int&);
	void rotateFace(const int&);		//in professional terminology rotation of the right side of the cube by clockwise called (R), but rotation by counterclockwise called (R')
	void backRotateFace(const int&);	//so for this reason (') replased by (back...)
	bool operator==(RubiksCube&);
};

