#if 1
#include <iostream>
#include <fstream>
#include <string>
#include <conio.h>
#include <vector>
#include <time.h>

#define N 9


using namespace std;

int Table[N][N];
int backtracks;

int readFile();
int writeFile();
void printSudoku();

bool rowCheck(int row, int number);
bool colCheck(int col, int number);
bool boxCheck(int startrow, int startCol, int number);
bool isSafe(int row, int col, int number);
bool sudokuSolver();

//Normal Backtracking
bool isnextPositionAvailable(int &row, int &col);

int main()
{
	clock_t start;
	clock_t stop;

	if (readFile() == -1)
		return 0;

	start = clock();

	sudokuSolver();
	stop = clock();
	cout << "Backtracks " << backtracks << endl;
	cout << "time is " << float((stop - start)/CLOCKS_PER_SEC) << endl;
	writeFile();
	
	_getch();
}


bool sudokuSolver()
{
	int row = -1;
	int col = -1;

	if (!isnextPositionAvailable(row, col))
		return true;

	for (int num = 1; num <= N; num++)
	{
		if (isSafe(row, col, num))
		{
			Table[row][col] = num;
			if (sudokuSolver())
				return true;
			backtracks++;
			Table[row][col] = 0;
		}
	}
	return false;
}

void printSudoku()	//Printing the Sudoku
{
	for (int i = 0; i < N; i++)
	{
		for (int j = 0; j < N; j++)
			cout << Table[i][j] << " ";
		cout << endl;
	}
	cout << endl;
}

int writeFile() //Writing to the file
{
	string line;
	ofstream myfile("D:\\Sem 1\\AI\\Assignment 2\\Project\\project2\\CSP\\CSP\\solution.txt");
	if (myfile.is_open())
	{
		for (int i = 0; i < N; i++)
		{
			for (int j = 0; j < N; j++)
			{
				myfile << Table[i][j];
				if (j != N-1)
					myfile << " ";
			}
			myfile << endl;
		}
		myfile.close();
		return 0;
	}
	else
	{
		cout << "Unable to write file";
		return -1;
	}
}

int readFile()
{
	string line;
	ifstream myfile("D:\\Sem 1\\AI\\Assignment 2\\Project\\project2\\CSP\\CSP\\puzzle.txt");
	if (myfile.is_open())
	{
		int i = 0;
		int j = 0;
		while (getline(myfile, line))
		{
			int k = 0;
			j = 0;
			while (k!=line.size())
			{ 
				if (line[k] != ' ')
				{
					Table[i][j] = line[k] - '0';
					j++;
				}
				k++;
			}
			i++;

		}
		myfile.close();
		return 0;
	}
	else
	{
		cout << "Unable to open a file";
		return -1;
	}
}

bool rowCheck(int row, int number)
{
	for (int j = 0; j < N; j++)
		if (Table[row][j] == number)
			return true;
	return false;
}

bool colCheck(int col, int number)
{
	for (int i = 0; i < N; i++)
		if (Table[i][col] == number)
			return true;
	return false;
}

bool boxCheck(int startRow, int startCol, int number)
{
	for (int i = 0; i < N / 3; i++)
		for (int j = 0; j < N / 3; j++)
			if (Table[i + startRow][j + startCol] == number)
				return true;
	return false;
}

bool isSafe(int row, int col, int number)	//Function to check whether the addition of number is row,column, box safe
{
	return !rowCheck(row, number) && !colCheck(col, number) && !(boxCheck(row - row % 3, col - col % 3, number));
}

bool isnextPositionAvailable(int &row, int &col)	//Next position
{
	for (int i = 0; i < N; i++)
		for (int j = 0; j < N; j++)
			if (Table[i][j] == 0)
			{
				row = i;
				col = j;
				return true;
			}
	return false;
}
#endif