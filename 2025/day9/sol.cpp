#include <iostream>
#include <fstream>
#include <cassert>
#include <string>
#include <vector>
#include <utility>
#include <cstdlib>
#include <algorithm>

long getRectangleSize(std::pair<int,int> p, std::pair<int,int> q) {
    return (std::abs(p.first - q.first) + 1L)*(std::abs(p.second - q.second) + 1L);
}

long getRectangleSizeIfValid(std::pair<int,int> p, std::pair<int,int> q, const std::vector<std::pair<int,int>>& allPoints) {
    bool lineCrossing = false;
    for (int i = 0; i < allPoints.size(); ++i) {
        const std::pair<int,int>& point = allPoints[i];
        const std::pair<int,int>& nextPoint = i == allPoints.size() - 1 ? allPoints[0] : allPoints[i+1];
        //check that the line from point to nextPoint doesn't cross into the interior of the retangle formed by p and q
        bool lineAlongXAxis = point.second == nextPoint.second;
        if (lineAlongXAxis) {
            bool lineBetweenHorizontalEdges = point.second > std::min(p.second,q.second) && point.second < std::max(p.second, q.second);
            if (lineBetweenHorizontalEdges && std::max(point.first, nextPoint.first) > std::min(p.first, q.first) && std::min(point.first, nextPoint.first) < std::max(p.first, q.first)) {
                lineCrossing = true;
                break;
            }
        } else {
            assert(point.first == nextPoint.first);
            bool lineBetweenVerticalEdges = point.first > std::min(p.first,q.first) && point.first < std::max(p.first,q.first);
            if (lineBetweenVerticalEdges && std::max(point.second, nextPoint.second) > std::min(p.second,q.second) && std::min(point.second, nextPoint.second) < std::max(p.second,q.second)) {
                lineCrossing = true;
                break;
            }
        }
    }
    if (!lineCrossing) {
        return getRectangleSize(p, q);
    }
    return -1;
}


int main(int argc, char** argv) {
    assert(argc >= 1);
    int part = std::atoi(argv[1]);

    std::ifstream is{"input.txt"};
    std::string line;
    std::vector<std::pair<int,int>> points;
    while (std::getline(is, line)) {
        int pos = line.find(',');
        points.emplace_back(std::stoi(line.substr(0,pos)), std::stoi(line.substr(pos+1)));
    }

    long max = -1;
    for (int i= 0; i < points.size(); ++i) {
        for (int j = i+1; j < points.size(); ++j) {
            if (part == 1) {
                max = std::max(max, getRectangleSize(points[i], points[j]));
            } else {
                max = std::max(max, getRectangleSizeIfValid(points[i], points[j], points));
            }
        }
    }
    std::cout << max << "\n";
}