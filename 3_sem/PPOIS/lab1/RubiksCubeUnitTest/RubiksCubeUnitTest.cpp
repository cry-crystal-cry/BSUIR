#include "pch.h"
#include "CppUnitTest.h"
#include "RubiksCube.h"

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace RubiksCubeUnitTest
{
	TEST_CLASS(RubiksCubeUnitTest)
	{
	public:
		TEST_METHOD(TestMethodSetRandom)
		{
			RubiksCube cube;
			cube.setRandom();
			Assert::IsTrue(true);
		}
		TEST_METHOD(TestMethodSetFromWrongFile)
		{
			RubiksCube cube;
			cube.setFromFile("C:\\Users\\USER\\Downloads\\1.txxxx");
			Assert::IsTrue(true);
		}
		TEST_METHOD(TestMethodSetFromFile)
		{
			RubiksCube cube;
			cube.setFromFile("C:\\Users\\USER\\Downloads\\1.txt");
			Assert::IsTrue(true);
		}
		TEST_METHOD(TestMethodSetRotateFace)
		{
			RubiksCube cube1,cube2;
			cube1.setFromFile("C:\\Users\\USER\\Downloads\\1.txt");
			cube2.setFromFile("C:\\Users\\USER\\Downloads\\1.txt");
			for (int i = 0; i < 6; i++) {
				for (int j = 0; j < 4; j++)
					cube1.rotateFace(i);
			}
			Assert::IsTrue(cube1 == cube2);
		}
		TEST_METHOD(TestMethodSetBackRotateFace)
		{
			RubiksCube cube1, cube2;
			cube1.setFromFile("C:\\Users\\USER\\Downloads\\1.txt");
			cube2.setFromFile("C:\\Users\\USER\\Downloads\\1.txt");
			for (int i = 0; i < 6; i++) {
				for (int j = 0; j < 4; j++)
					cube1.backRotateFace(i);
			}
			Assert::IsTrue(cube1 == cube2);
		}
		TEST_METHOD(TestMethodShowCubeCrossForSide)
		{
			RubiksCube cube;
			cube.setFromFile("C:\\Users\\USER\\Downloads\\1.txt");
			for (int i = 0; i < 6; i++) 
					cube.showCubeCrossForSide(i);
			Assert::IsTrue(true);
		}
	};
}
