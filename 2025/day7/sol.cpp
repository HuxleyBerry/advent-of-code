#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cassert>
#include <cstdlib>
#include <algorithm>
#include <stdexcept>
#include <map>
#include <utility>
#include <queue>

enum class Cell {
    EMPTY,
    BEAM,
    SPLITTER
};

int tick(std::vector<std::vector<Cell>>& grid, int width, int height, int row) {
    int count = 0;
    for (int i = 0; i < width; ++i) {
        if (grid[row][i] == Cell::BEAM) {
            grid[row][i] = Cell::EMPTY;
            if (grid[row+1][i] == Cell::EMPTY) {
                // move beam down
                grid[row+1][i] = Cell::BEAM;

            } else if (grid[row+1][i] == Cell::SPLITTER) {
                ++count;
                grid[row+1][i+1] = Cell::BEAM;
                grid[row+1][i-1] = Cell::BEAM;
            }
        }
    }
    return count;
}

int coordsToNum(int posX, int posY, int width) {
    return posY*width + posX;
}

void incrementAtMapKey(std::map<int, long>& pathsTo, int key, long val) {
    if (pathsTo.count(key) == 0) {
        pathsTo[key] = val;
    } else {
        pathsTo[key] += val;
    }
}

long countPaths(std::vector<std::vector<Cell>>& grid, int posX, int posY, int endY, int width) {
    long total = 0;
    std::map<int, long> pathsTo;
    pathsTo[coordsToNum(posX, posY, width)] = 1;

    std::queue<std::pair<int,int>> queue;
    queue.emplace(posX, posY);
    while (queue.size() != 0) {
        std::pair<int, int> current = queue.front();
        long pathsToCurrent = pathsTo[coordsToNum(current.first, current.second, width)];
        if (current.second != endY) {
            if (grid[current.second+1][current.first] == Cell::EMPTY) {
                if (pathsTo.count(coordsToNum(current.first, current.second+1, width)) == 0) {
                    queue.emplace(current.first, current.second+1);
                }
                incrementAtMapKey(pathsTo, coordsToNum(current.first, current.second+1, width), pathsToCurrent);
            } else if (grid[current.second+1][current.first] == Cell::SPLITTER) {
                if (pathsTo.count(coordsToNum(current.first+1, current.second+1, width)) == 0) {
                    queue.emplace(current.first+1, current.second+1);
                }
                incrementAtMapKey(pathsTo, coordsToNum(current.first+1, current.second+1, width), pathsToCurrent);
                if (pathsTo.count(coordsToNum(current.first-1, current.second+1, width)) == 0) {
                    queue.emplace(current.first-1, current.second+1);
                }
                incrementAtMapKey(pathsTo, coordsToNum(current.first-1, current.second+1, width), pathsToCurrent);
            }
        } else {
            total += pathsToCurrent;
        }
        queue.pop();
    }
    return total;
}

void printGrid(std::vector<std::vector<Cell>>& grid, int width, int height) {
    for (const auto& row: grid) {
        for (Cell c: row) {
            switch (c)
            {
            case Cell::EMPTY:
                std::cout << ".";
                break;
            case Cell::BEAM:
                std::cout << "|";
                break;
            case Cell::SPLITTER:
                std::cout << "^";
                break;
            }
        }
        std::cout << "\n";
    }
    std::cout << "\n";
}

int main(int argc, char** argv) {
    assert(argc > 1);
    int part = std::atoi(argv[1]);

    std::ifstream is{"input.txt"};
    std::string line;
    std::vector<std::vector<Cell>> grid;
    while (std::getline(is, line)) {
        std::vector<Cell> row;
        for (char c: line) {
            row.push_back(c == 'S' ? Cell::BEAM : (c == '^' ? Cell::SPLITTER : Cell::EMPTY));
        }
        grid.push_back(row);
    }
    int width = grid[0].size();
    int height = grid.size();

    if (part == 1) {
        int splitCount = 0;
        for (int i = 0; i < height - 1; ++i) {
            splitCount += tick(grid, width, height, i);
        }
        std::cout << splitCount << "\n";
    } else if (part == 2) {
        int x = std::find(grid[0].cbegin(), grid[0].cend(), Cell::BEAM) - grid[0].cbegin();
        grid[0][x] = Cell::EMPTY;
        std::cout << countPaths(grid, x, 0, height - 1, width) << "\n";
    }
}