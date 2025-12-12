#include <iostream>
#include <fstream>
#include <cassert>
#include <string>
#include <vector>
#include <utility>
#include <sstream>
#include <unordered_map>
#include <cstdlib>

int getMemoKey(int size, int startIndex, int endIndex) {
    return size*startIndex + endIndex;
}

long countPaths(const std::vector<std::vector<int>>& graph, int startIndex, int endIndex, std::unordered_map<int, int>& memo) {
    if (int key = getMemoKey(graph.size(), startIndex, endIndex); memo.count(key) > 0) {
        return memo[key];
    }
    else if (startIndex == endIndex) {
        return 1;
    } else {
        long sum = 0;
        for (int child: graph[startIndex]) {
            sum += countPaths(graph, child, endIndex, memo);
        }
        memo[getMemoKey(graph.size(), startIndex, endIndex)] = sum;
        return sum;
    }
}

int main(int argc, char** argv) {
    assert(argc > 1);
    int part = std::atoi(argv[1]);

    std::ifstream is{"input.txt"};
    std::vector<std::pair<std::string, std::vector<std::string>>> input;
    std::string line;
    while (std::getline(is, line)) {
        int pos = line.find(':');
        std::vector<std::string> outputs;
        std::istringstream iss{line.substr(pos+2)};
        std::string buff;
        while (std::getline(iss, buff, ' ')) {
            outputs.push_back(buff);
        }
        input.emplace_back(line.substr(0, pos), std::move(outputs));
    }

    int youIndex = -1;
    int svrIndex = -1;
    int dacIndex = -1;
    int fftIndex = -1;
    std::unordered_map<std::string, int> nameToIndex;
    for (int i = 0; const auto& [device, outputs]: input) {
        if (nameToIndex.count(device) == 0) {
            nameToIndex[device] = i;
        }
        if (device == "you") {
            youIndex = i;
        } else if (device == "svr") {
            svrIndex = i;
        } else if (device == "dac") {
            dacIndex = i;
        } else if (device == "fft") {
            fftIndex = i;
        }
        ++i;
    }
    int outIndex = nameToIndex.size();
    nameToIndex["out"] = outIndex;
    std::vector<std::vector<int>> graph(nameToIndex.size());
    for (int i = 0; const auto& [device, outputs]: input) {
        std::vector<int> outputNumbers;
        for (const std::string& os: outputs) {
            outputNumbers.push_back(nameToIndex[os]);
        }
        graph[i] = std::move(outputNumbers);
        ++i;
    }

    if (part == 1) {
        assert(youIndex != -1);
        std::unordered_map<int, int> memo;
        std::cout << countPaths(graph, youIndex, outIndex, memo) << "\n";
    } else if (part == 2) {
        assert(svrIndex != -1);
        assert(dacIndex != -1);
        assert(fftIndex != -1);

        std::unordered_map<int, int> memo;

        long dacToFft = countPaths(graph, dacIndex, fftIndex, memo);
        long fftToDac = countPaths(graph, fftIndex, dacIndex, memo);
        if (dacToFft > 0) {
            std::cout << countPaths(graph, svrIndex, dacIndex, memo) * dacToFft * countPaths(graph, fftIndex, outIndex, memo) << "\n";
        } else {
            assert(fftToDac > 0);
            std::cout << countPaths(graph, svrIndex, fftIndex, memo) * fftToDac * countPaths(graph, dacIndex, outIndex, memo) << "\n";
        }
    }
}