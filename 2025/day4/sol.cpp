#include <iostream>
#include <string>
#include <cstdlib>
#include <cassert>
#include <fstream>
#include <vector>
#include <utility>

int main(int argc, char** argv) {
    assert(argc == 2);
    int part = std::atoi(argv[1]);
    assert(part == 1 || part == 2);


    std::ifstream is {"input.txt"};
    std::vector<std::vector<bool>> grid;
    bool firstIteration = true;
    int width;
    int height = 0;
    std::string line;
    while (std::getline(is, line)) {
        std::vector<bool> row {false};
        for (const char c: line) {
            row.push_back(c == '@');
        }
        row.push_back(false);
        if (firstIteration) {
            width = row.size();
            firstIteration = false;
            grid.push_back(std::vector<bool>(width, false));
        }
        grid.push_back(row);
    }
    grid.push_back(std::vector<bool>(width, false));
    height = grid.size();

    const std::vector<std::pair<int,int>> offsets{{1,0}, {1,1}, {1,-1}, {0,1}, {0,-1}, {-1,0}, {-1,1}, {-1,-1}};

    int overallCount = 0;
    while (true) {
        int count = 0;
        for (size_t i = 1; i < width-1; ++i) {
            for (size_t j = 1; j < height-1; ++j) {
                if (grid[j][i]) {
                    int neighbourCount = 0;
                    for (const auto& offset : offsets) {
                        if (grid[j+offset.second][i+offset.first]) {
                            ++neighbourCount;
                            if (neighbourCount >= 4) {
                                break;
                            }
                        }
                    }
                    if (neighbourCount < 4) {
                        if (part == 2) {
                            grid[j][i] = false;
                        }
                        ++count;
                    }
                }
            }
        }
        if (count == 0) {
            break;
        } else {
            overallCount += count;
        }
        if (part == 1) {
            break;
        }
    }

    std::cout << overallCount << "\n";
}