#include <iostream>
#include <fstream>
#include <cstdlib>
#include <string>
#include <vector>
#include <array>
#include <cassert>
#include <sstream>
#include <utility>
#include <algorithm>

struct Region {
    int width;
    int height;
    std::vector<int> shapeCounts;
};

int countBitsInNum(int num) {
    int count = 0;
    while (num > 0) {
        count += num & 1;
        num >>= 1;
    }
    return count;
}

enum class Result {
    POSSIBLE,
    IMPOSSIBLE,
    UNKNOWN
};

Result testRegion(const Region& region, const std::vector<int>& shapes) {
    int regionArea = region.width * region.height;
    assert(region.shapeCounts.size() == shapes.size());
    int shapesTotalArea = 0;
    int shapesRequired = 0;
    for (int i = 0; i < region.shapeCounts.size(); ++i) {
        shapesTotalArea += region.shapeCounts[i] * countBitsInNum(shapes[i]);
        shapesRequired += region.shapeCounts[i];
    }
    if (shapesTotalArea > regionArea) {
        return Result::IMPOSSIBLE;
    }
    if ((region.width/3) * (region.height/3) >= shapesRequired) {
        return Result::POSSIBLE;
    }
    return Result::UNKNOWN;
}

int main() {
    std::ifstream is{"input.txt"};
    std::vector<int> shapes; // represent each string as 9-bit number;
    std::vector<Region> regions;
    std::string line;
    bool isReadingShapes = true;
    while (true) {
        bool notReachedEOF = bool(std::getline(is, line));
        if (!notReachedEOF) {
            break;
        }
        if (!isReadingShapes  || line[line.size() - 1] != ':') {
            isReadingShapes = false;

            std::vector<int> shapeCounts;
            int xPos = line.find('x');
            int colonPos = line.find(':', xPos+1);
            std::istringstream iss{line.substr(colonPos+2)};
            std::string buff;
            while (std::getline(iss, buff, ' ')) {
                shapeCounts.push_back(std::stoi(buff));
            }
            regions.push_back({std::stoi(line.substr(0,xPos)), std::stoi(line.substr(xPos+1, colonPos - xPos - 1)), shapeCounts});
        }
        if (isReadingShapes) {
            int num = 0;
            for (int i = 0; i < 3; ++i) {
                std::getline(is, line);
                assert(line.size() == 3);
                for (int j = 0; j < 3; ++j) {
                    num = num * 2 + (line[j] == '#' ? 1 : 0);
                }
            }
            shapes.push_back(num);
            std::getline(is, line);
        }
    }
    int possibleCount;
    int impossibleCount;
    int unknownCount;
    for (const Region& region: regions) {
        Result result = testRegion(region, shapes);
        switch (result)
        {
        case Result::POSSIBLE:
            ++possibleCount;
            break;
        case Result::IMPOSSIBLE:
            ++impossibleCount;
            break;
        case Result::UNKNOWN:
            ++unknownCount;
            break;
        }
    }
    if (unknownCount == 0) {
        std::cout << possibleCount << "\n";
    } else {
        std::cout << "answer unknown\n";
    }
}