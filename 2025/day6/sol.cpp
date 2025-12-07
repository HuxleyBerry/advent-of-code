#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include <cassert>
#include <vector>
#include <sstream>
#include <algorithm>

enum class Operator {
    ADD,
    MULT
};

int main(int argc, char** argv) {
    assert(argc >= 2);
    int part = std::atoi(argv[1]);

    std::ifstream is {"input.txt"};
    std::string line;
    std::vector<std::string> numberLines;
    std::string operatorLine;
    std::vector<Operator> operators;
    
    bool firstRow = true;
    while(std::getline(is, line)) {
        if (line[0] == '*' || line[0] == '+') {
            operatorLine = line;
        } else {
            numberLines.push_back(line);
        }
    }

    std::vector<int> columnWidths;
    int gapSize = 0;
    for (int i = operatorLine.size() - 1; i >= 0; --i) {
        if (operatorLine[i] == '*') {
            operators.push_back(Operator::MULT);
            columnWidths.push_back(gapSize+1);
            gapSize = -1;
        } else if (operatorLine[i]  == '+') {
            operators.push_back(Operator::ADD);
            columnWidths.push_back(gapSize+1);
            gapSize = -1;
        } else {
            assert(operatorLine[i] == ' ');
            ++gapSize;
        }
    }
    std::reverse(columnWidths.begin(), columnWidths.end());
    std::reverse(operators.begin(), operators.end());

    std::vector<std::vector<int>> nums;

    int pos = 0;
    for (int i = 0; i < operators.size(); ++i) {
        std::vector<int> col;
        if (part == 1) {
            for (int j = 0; j < numberLines.size(); ++j) {
                std::string untrimmedNumAsString = numberLines[j].substr(pos, columnWidths[i]);
                size_t nonSpaceIndex = untrimmedNumAsString.find_first_not_of(' ');
                col.push_back(std::stoi(untrimmedNumAsString.substr(nonSpaceIndex)));
            }
        } else if (part == 2) {
            for (int j = 0; j < columnWidths[i]; j++) {
                int val = 0;
                for (int k = 0; k < numberLines.size(); ++k) {
                    if (char c = numberLines[k][pos+j]; c != ' ') {
                        val = val*10 + (c - '0');
                    }
                }
                col.push_back(val);
            }
        }
        pos += columnWidths[i]+1;
        nums.push_back(col);
    }

    long total = 0;
    for (int i = 0; i < nums.size(); ++i) {
        long val = operators[i] == Operator::MULT ? 1 : 0;
        for (int num: nums[i]) {
            if (operators[i] == Operator::MULT) {
                val *= num;
            } else {
                val += num;
            }
        }
        total += val;
    }
    std::cout << total << "\n";
}