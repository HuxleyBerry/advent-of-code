#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <algorithm>
#include <cstdlib>
#include <cassert>
#include <numeric>

long tenthPower(int power){
    long val = 1;
    for (int i = 0; i < power; ++i) {
        val *= 10;
    }
    return val;
} 

long getMaxJoltage(std::vector<int>::const_iterator start, std::vector<int>::const_iterator end, int selectionCount) {
    if (selectionCount == 1) {
        return *std::max_element(start, end);
    } else {
        auto max = std::max_element(start, end - (selectionCount-1));
        return (*max) * tenthPower(selectionCount-1) + getMaxJoltage(max + 1, end, selectionCount - 1);
    }
}

long getMaxJoltage(std::vector<int> bank, int selectionCount) {
    return getMaxJoltage(bank.cbegin(), bank.cend(), selectionCount);
}

int main(int argc, char** argv) {
    std::ifstream is {"input.txt"};
    std::string line;
    std::vector<std::vector<int>> data;
    while(std::getline(is, line)) {
        std::vector<int> bank;
        for (const char c : line) {
            bank.push_back(c - '0');
        }
        data.push_back(bank);
    }
    assert(argc > 1);
    int part = std::atoi(argv[1]);
    assert(part == 1 || part == 2);
    std::cout << std::accumulate(data.cbegin(), data.cend(), 0L, [part](long total, std::vector<int> bank){
        return total + getMaxJoltage(bank, part == 1 ? 2 : 12);
    }) << "\n";
}