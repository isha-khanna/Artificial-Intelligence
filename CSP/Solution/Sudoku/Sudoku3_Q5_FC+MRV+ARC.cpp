#if 1
#include <iostream>
#include <fstream>
#include <string>
#include <conio.h>
#include <vector>
#include <time.h>

#define N 9

using namespace std;

struct cell{
	bool lock;
	int countValues;
	vector <int > values;
};

int Table[N][N];
struct cell mrvCell[N][N];
int backtracks;

int readFile();
int writeFile();
void printSudoku();

bool rowCheck(int row, int number);
bool colCheck(int col, int number);
bool boxCheck(int startrow, int startCol, int number);
bool isSafe(int row, int col, int number);
bool sudokuSolver(int x);

//Normal Backtracking
bool isnextPositionAvailable(int &row, int &col);

//Mrv heuristic
void initMrvTable();
bool isNextPosAvailUsingMrv(int &row, int &col);

void updateNeighborsAfterZeroCell(int row, int col, int num);
//FC + MRV
bool sudokuSolverFC(int x, struct cell **mrvCell);
void copyFcTable(struct cell **src, struct cell **dest);
struct cell** newObject();
bool checkZeroCell(int row, int col);
bool checkOneCell(int row, int col, int num);

void updateNeighbors(int row, int col, int num);

int main()
{
	struct cell **mrvCell = newObject();

	clock_t start;
	clock_t stop;

	if (readFile() == -1)
		return 0;

	start = clock();
	initMrvTable();
	//sudokuSolverFC(1, mrvCell);

	sudokuSolver(1);
	stop = clock();
	cout << "Backtracks " << backtracks << endl;
	cout << "time is " << (stop - start) << endl;
	writeFile();



	_getch();
}

struct cell** newObject()
{
	struct cell **mrvCell = new struct cell*[N];
	for (int i = 0; i < N; i++)
		mrvCell[i] = new struct cell[N];
	return mrvCell;
}

void copyFcTable(struct cell **src, struct cell **dest)
{
	for (int i = 0; i < N; i++)
		for (int j = 0; j < N; j++)
		{
		dest[i][j].countValues = src[i][j].countValues;
		dest[i][j].lock = src[i][j].lock;
		for (int k = 0; k < (int)src[i][j].values.size(); k++)
			dest[i][j].values.push_back(src[i][j].values[k]);
		}
}


bool checkZeroCellAlternative(int row, int col, int num)
{
	for (int i = 0; i < N; i++)
		if (i != col && !mrvCell[row][i].lock && (mrvCell[row][i].countValues == 1) && (mrvCell[row][i].values[0] == num))
			return true;

	for (int i = 0; i < N; i++)
		if (i != row && !mrvCell[i][col].lock && (mrvCell[i][col].countValues == 1) && (mrvCell[i][col].values[0] == num))
			return true;

	int startRow = row - row % 3;
	int startCol = col - col % 3;

	for (int i = 0; i < N / 3; i++)
	{
		for (int j = 0; j < N / 3; j++)
		{
			if (i + startRow == row && j + startCol == col)
				continue;
			if (!mrvCell[i + startRow][j + startCol].lock && mrvCell[i + startRow][j + startCol].countValues == 1 && mrvCell[i + startRow][j + startCol].values[0] == num)
				return true;
		}
	}

	return false;

}


bool checkZeroCell(int row, int col)
{
	for (int i = 0; i < N; i++)
		if (i != col && !mrvCell[row][i].lock && mrvCell[row][i].countValues == 0)
			return true;

	for (int i = 0; i < N; i++)
		if (i != row && !mrvCell[i][col].lock && mrvCell[i][col].countValues == 0)
			return true;

	int startRow = row - row % 3;
	int startCol = col - col % 3;

	for (int i = 0; i < N / 3; i++)
	{
		for (int j = 0; j < N / 3; j++)
		{
			if (i + startRow == row && j + startCol == col)
				continue;
			if (!mrvCell[i + startRow][j + startCol].lock && mrvCell[i + startRow][j + startCol].countValues == 0)
				return true;
		}
	}

	return false;

}

bool checkOneCell(int row, int col, int num)
{
	for (int i = 0; i < N; i++)
	{
		bool flag = false;
		if (mrvCell[row][i].values.size() != 2)
			continue;
		int val1 = mrvCell[row][i].values[0];
		int val2 = mrvCell[row][i].values[1];

		if (i != col && !mrvCell[row][i].lock && mrvCell[row][i].countValues == 2 && (val1 == num || val2 == num))
			flag = true;
		else
			continue;

		int temp = val1;
		if (temp == num)
			temp = val2;
		Table[row][col] = num;
		updateNeighbors(row, col, num);
		if (checkZeroCellAlternative(row,i,temp))
		{
			Table[row][col] = 0;
			//initMrvTable();
			updateNeighborsAfterZeroCell(row, i, temp);
			return false;
		}
		Table[row][col] = 0;
		initMrvTable();
	}


	for (int i = 0; i < N; i++)
	{
		bool flag = false;
		if (mrvCell[i][col].values.size() != 2)
			continue;
		int val1 = mrvCell[i][col].values[0];
		int val2 = mrvCell[i][col].values[1];
		if (i != row && !mrvCell[i][col].lock && mrvCell[i][col].countValues == 2 && (val1 == num || val2 == num))
			flag = true;
		else
			continue;
		int temp = val1;
		if (temp == num)
			temp = val2;
		Table[row][col] = num;
		updateNeighbors(row, col, num);
		if (checkZeroCellAlternative(i, col, temp))
		{
			Table[row][col] = 0;
			//initMrvTable();
			updateNeighborsAfterZeroCell(i, col, temp);
			return false;
		}
		Table[row][col] = 0;
		initMrvTable();
	}
	int startRow = row - row % 3;
	int startCol = col - col % 3;

	for (int i = 0; i < N / 3; i++)
	{
		for (int j = 0; j < N / 3; j++)
		{
			if (mrvCell[i + startRow][j + startCol].values.size() != 2)
				continue;
			if ((i + startRow == row) && (j + startCol == col))
				continue;
			bool flag = false;
			int val1 = mrvCell[i + startRow][j + startCol].values[0];
			int val2 = mrvCell[i + startRow][j + startCol].values[1];

			if (!mrvCell[i + startRow][j + startCol].lock && mrvCell[i + startRow][j + startCol].countValues == 2 && (val1 == num || val2 == num))
				flag = true;
			else 
				continue;
			int temp = val1;
			if (temp == num)
				temp = val2;
			Table[row][col] = num;
			updateNeighbors(row, col, num);
			if (checkZeroCellAlternative(i + startRow, j + startCol, temp))
			{
				Table[row][col] = 0;
				//initMrvTable();
				updateNeighborsAfterZeroCell(i + startRow, j + startCol, temp);
				return false;
			}
			Table[row][col] = 0;
			initMrvTable();
		}
	}

	return true;
}

void updateNeighbors(int row, int col, int num)
{
	for (int i = 0; i < N; i++)
	{
		if (col != i && Table[row][i] == 0)
		{
			for (int k = 0; k != mrvCell[row][i].values.size(); k++)
				if (num == mrvCell[row][i].values[k])
				{
				mrvCell[row][i].values.erase(mrvCell[row][i].values.begin() + k);
				mrvCell[row][i].countValues--;
				break;
				}
		}
	}

	for (int i = 0; i < N; i++)
	{
		if (row != i && Table[i][col] == 0)
		{
			for (int k = 0; k != mrvCell[i][col].values.size(); k++)
				if (num == mrvCell[i][col].values[k])
				{
				mrvCell[i][col].values.erase(mrvCell[i][col].values.begin() + k);
				mrvCell[i][col].countValues--;
				break;
				}
		}
	}
	int startRow = row - row % 3;
	int startCol = col - col % 3;

	for (int i = 0; i < N / 3; i++)
	{
		for (int j = 0; j < N / 3; j++)
		{
			if ((i + startRow == row) && (j + startCol == col))
				continue;
			if (Table[i + startRow][j + startCol] == 0)
			{
				for (int k = 0; k != mrvCell[i + startRow][j + startCol].values.size(); k++)
					if (num == mrvCell[i + startRow][j + startCol].values[k])
					{
					mrvCell[i + startRow][j + startCol].values.erase(mrvCell[i + startRow][j + startCol].values.begin() + k);
					mrvCell[i + startRow][j + startCol].countValues--;
					break;
					}
			}
		}

	}
}

void updateNeighborsAfterZeroCell(int row, int col, int num)
{
	for (int i = 0; i < N; i++)
	{
		if (col != i)
		{
			if (isSafe(row, i, num))
			{
				mrvCell[row][i].countValues++;
				mrvCell[row][i].values.push_back(num);
			}
		}
	}

	for (int i = 0; i < N; i++)
	{
		if (row != i)
		{
			if (isSafe(i, col, num))
			{
				mrvCell[i][col].countValues++;
				mrvCell[i][col].values.push_back(num);
			}
		}
	}
	int startRow = row - row % 3;
	int startCol = col - col % 3;

	for (int i = 0; i < N / 3; i++)
	{
		for (int j = 0; j < N / 3; j++)
		{
			if ((i + startRow == row) && (j + startCol == col))
				continue;
			if (isSafe(i + startRow, j + startCol, num))
			{
				mrvCell[i + startRow][j + startCol].countValues++;
				mrvCell[i + startRow][j + startCol].values.push_back(num);
			}
		}

	}
}

void initMrvTable()
{
	for (int i = 0; i < N; i++)
	{
		for (int j = 0; j < N; j++)
		{
			mrvCell[i][j].countValues = 0;
			if (Table[i][j] != 0)
			{
				mrvCell[i][j].lock = true;
				continue;
			}
			mrvCell[i][j].lock = false;
			mrvCell[i][j].values.clear();
			for (int num = 1; num <= 9; num++)
			{
				if (isSafe(i, j, num))
				{
					mrvCell[i][j].countValues++;
					mrvCell[i][j].values.push_back(num);
				}
			}
		}
	}
}

bool isNextPosAvailUsingMrv(int &row, int &col)
{
	int least = N + 1;
	for (int i = 0; i < N; i++)
		for (int j = 0; j < N; j++)
			if (Table[i][j] == 0 && mrvCell[i][j].countValues<least)
			{
		row = i;
		col = j;
		least = mrvCell[i][j].countValues;
			}

	if (row == -1 || col == -1)
		return false;
	else
		return true;
}

bool sudokuSolver(int x)
{
	int row = -1;
	int col = -1;

	if (!isNextPosAvailUsingMrv(row, col))
		return true;

	for (int k = 0; k < mrvCell[row][col].values.size(); k++)
	{
		int num = mrvCell[row][col].values[k];
		if (isSafe(row, col, num))
		{
			if (checkZeroCellAlternative(row, col, num))
			return false;
			if (checkOneCell(row, col, num) == false)
			return false;

			Table[row][col] = num;

			//initMrvTable();

			updateNeighbors(row, col, num);

			if (sudokuSolver(x))
				return true;
			backtracks++;
			Table[row][col] = 0;

			if (x)
			{
				initMrvTable();
			}

		}
	}
	return false;
}

void printSudoku()
{
	for (int i = 0; i < N; i++)
	{
		for (int j = 0; j < N; j++)
			cout << Table[i][j] << " ";
		cout << endl;
	}
	cout << endl;
}

int writeFile()
{
	string line;
	ofstream myfile("C:\\Users\\7jan\\Downloads\\Downloads\\solution1.txt");
	if (myfile.is_open())
	{
		for (int i = 0; i < N; i++)
		{
			for (int j = 0; j < N; j++)
			{
				myfile << Table[i][j];
				if (j != N - 1)
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
	ifstream myfile("C:\\Users\\7jan\\Downloads\\Downloads\\problem1.txt");
	if (myfile.is_open())
	{
		int i = 0;
		int j = 0;
		while (getline(myfile, line))
		{
			int k = 0;
			j = 0;
			while (k != line.size())
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

bool isSafe(int row, int col, int number)
{
	return !rowCheck(row, number) && !colCheck(col, number) && !(boxCheck(row - row % 3, col - col % 3, number));
}

bool isnextPositionAvailable(int &row, int &col)
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

