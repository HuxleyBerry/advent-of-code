#include <iostream>
#include <fstream>
#include <cstdlib>
#include <vector>
#include <queue>
#include <cassert>
#include <string>
#include <sstream>
#include <algorithm>
#include <numeric>
#include <iomanip>
#include <utility>
#include <limits>
#include "fractions.h"

const int INT_MAX = std::numeric_limits<int>::max();

std::ostream& operator<<(std::ostream& os, const Fraction& f) {
    os << f.numerator << "/" << f.denominator;
    return os;
}

typedef std::vector<std::vector<Fraction>> Matrix;

void printMatrix(Matrix m) {
    for (const auto& row: m) {
        for (const Fraction& f: row) {
            std::cout << std::setw(10) << f;
        }
        std::cout << "\n";
    }
}

// return -1 if none exists
int getIndexOfNonZeroinColumn(Matrix& m, int height, int columnIndex, int currentRowIndex) {
    for (int i = currentRowIndex; i < height; ++i) {
        if (m[i][columnIndex] != 0) {
            return i;
        }
    }
    return -1;
}

void switchRowsOfMatrix(Matrix& m, int index1, int index2) {
    //TODO: consider making this require less copies
    auto temp = m[index1];
    m[index1] = m[index2];
    m[index2] = temp;
}

void addMultipleOfRow(Matrix& m, int width, int targetIndex, int sourceIndex, const Fraction& multiple, bool debug=false) {
    for (int i = 0; i < width; ++i) {
        if (debug) {
            std::cout << m[targetIndex][i] << " " << multiple*m[sourceIndex][i] << " " << multiple << "\n";
        }
        m[targetIndex][i] += multiple*m[sourceIndex][i];
    }
}

void DivideRow(Matrix& m, int width, int rowIndex, const Fraction& divisor) {
    for (int i = 0; i < width; ++i) {
        m[rowIndex][i] /= divisor;
    }
}

std::vector<int> gaussianElimination(Matrix& m, int width, int height) {
    int currentRow = 0;
    int pivotColumn = 0;

    std::vector<int> pivotColumns;

    while(currentRow < height){
        //find the index of the next column which isn't all zeroes
        bool nonZeroColumnFound = false;
        int indexOfNonZero = -1;
        while (!nonZeroColumnFound && pivotColumn < width - 1) {
            int index = getIndexOfNonZeroinColumn(m, height, pivotColumn, currentRow);
            if (index != -1) {
                nonZeroColumnFound = true;
                indexOfNonZero = index;
                pivotColumns.push_back(pivotColumn);
            } else {
                ++pivotColumn;
            }
        }
        if (!nonZeroColumnFound) {
            break;
        }

        if (indexOfNonZero != currentRow) { //swap required
            switchRowsOfMatrix(m, currentRow, indexOfNonZero);
        }
        for (int i = currentRow+1; i < height; ++i) {
            if (m[i][pivotColumn] != 0) {
                Fraction multiple = (-m[i][pivotColumn]) / m[currentRow][pivotColumn];
                addMultipleOfRow(m, width, i, currentRow, multiple);    
            }
        }
        ++currentRow;
        ++pivotColumn;
    }
    assert(pivotColumns.size() <= std::min(height, width - 1));
    return pivotColumns;
}

void reduceRefMatrix(Matrix& m, int width, int height, const std::vector<int>& pivotColumns) {
    for (int i = 0; i < pivotColumns.size(); ++i) {
        Fraction divisor = m[i][pivotColumns[i]];
        DivideRow(m, width, i, divisor);
    }
    for (int i = 0; i < pivotColumns.size(); ++i) {
        for (int j = 0; j < pivotColumns.size(); ++j) {
            int column = pivotColumns[j];
            if (j != i) {
                addMultipleOfRow(m, width, i, j, -m[i][column]);
            }
        }
    }
}

// returns -1 if the solution is not valid
int solveGivenFreeVariableValues(const Matrix& m, int width, const std::vector<int>& pivotColumns, const std::vector<std::pair<int,int>>& freeIndicesAndValues) {
    int sum = std::accumulate(freeIndicesAndValues.cbegin(), freeIndicesAndValues.cend(), 0, [](int val, const std::pair<int,int>& pair){
        return val + pair.second;
    });
    for (int i = 0; i < pivotColumns.size(); ++i) {
        Fraction solvedVal = m[i][width - 1];
        for (const auto& [index, value]: freeIndicesAndValues) {
            solvedVal -= m[i][index] * value;
        }
        if (!solvedVal.isInt()) {
            return -1;
        }
        int solvedValAsInt = solvedVal.toInt();
        if (solvedValAsInt < 0) {
            return -1;
        }
        sum += solvedValAsInt;
    }
    return sum;
}

long getMaxPossibleForVariable(const std::vector<int>& targetJoltages, const std::vector<std::vector<int>>& buttons, int variableIndex) {
    int min = INT_MAX;
    for (int index : buttons[variableIndex]) {
        min = std::min(min, targetJoltages[index]);
    }
    return min;
}

int findMinimumButtons(const std::vector<int>& targetJoltages, const std::vector<std::vector<int>>& buttons) {
    Matrix m;
    int width = buttons.size() + 1; // final column for the equation RHSs
    int height = targetJoltages.size();
    for (int i = 0; i < height; ++i) {
        m.push_back(std::vector<Fraction>(width,0));
    }
    for (int i = 0; i < buttons.size(); ++i) {
        for (int j = 0; j < buttons[i].size(); ++j) {
            m[buttons[i][j]][i] = Fraction(1);
        }
    }
    for (int i = 0; i < height; ++i) {
        m[i][width-1] = Fraction(targetJoltages[i]);
    }
    //printMatrix(m);
    std::vector<int> pivotColumns = gaussianElimination(m, width, height);
    //std::cout << "=======================\n";
    //printMatrix(m);
    //std::cout << "=======================!!\n";
    reduceRefMatrix(m, width, height, pivotColumns);
    //printMatrix(m);
    std::vector<int> freeColumns;
    std::vector<int> maxJoltages;
    long maxJoltagesProduct = 1;
    for (int i = 0; i < width - 1; ++i) {
        if (std::find(pivotColumns.cbegin(), pivotColumns.cend(), i) == pivotColumns.cend()) {
            freeColumns.push_back(i);
            long maxPossibleForVariable = getMaxPossibleForVariable(targetJoltages, buttons, i);
            maxJoltages.push_back(maxPossibleForVariable);
            maxJoltagesProduct *= maxPossibleForVariable + 1; // +1 because we need to test the range 0 to n
        }
    }

    int min = INT_MAX;
    for (long i = 0; i < maxJoltagesProduct; ++i) {
        std::vector<std::pair<int,int>> values;
        long current = i;
        for (int j = 0; j < freeColumns.size(); j++) {
            values.push_back({freeColumns[j], current%(maxJoltages[j] + 1)});
            current/=((maxJoltages[j] + 1));
        }
        int sumOfSolution = solveGivenFreeVariableValues(m, width, pivotColumns, values);
        if (sumOfSolution != -1) {
            min = std::min(min, sumOfSolution);
        }
    }
    return min; 
}

int main(int argc, char** argv) {
    std::ifstream is{"input.txt"};
    std::string line;
    std::vector<std::vector<std::vector<int>>> buttons; 
    std::vector<std::vector<int>> joltages;
    while (std::getline(is, line)) {
        std::string buff;
        std::istringstream ss{line};
        std::vector<std::vector<int>> buttonsFromLine;
        while(std::getline(ss, buff, ' ')) {
            if (buff[0] == '(' || buff[0] == '{') {
                std::string buff2;
                std::istringstream ss2{buff.substr(1, buff.size() - 2)};
                std::vector<int> nums;
                
                while(std::getline(ss2, buff2, ',')) {
                    nums.push_back(std::stoi(buff2));
                }
                if (buff[0] == '(') {
                    buttonsFromLine.push_back(nums);
                } else {
                    joltages.push_back(nums);
                }
            }
        }
        buttons.push_back(buttonsFromLine);
    }
    int total = 0;
    for (int i = 0; i < joltages.size(); ++i) {
        total += findMinimumButtons(joltages[i], buttons[i]);
    }
    std::cout << total << "\n";
}