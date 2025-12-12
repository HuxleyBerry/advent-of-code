#include <iostream>
#include <fstream>
#include <cstdlib>
#include <vector>
#include <queue>
#include <cassert>
#include <string>
#include <sstream>
#include <numeric>

int numsToBinary(const std::vector<int>& nums) {
    int ans = 0;
    for (int num : nums) {
        ans += 1 << num;
    }
    return ans;
}

struct QueueElement {
    int buttonPresses;
    int currentLightPattern;
    int lastButtonIndex;
};

struct QueueElement2 {
    int buttonPresses;
    std::vector<int> currentJoltages;
    int lastButtonIndex;
};

int findMinimumButtons(int targetLightPattern, const std::vector<int>& buttons) {
    std::queue<QueueElement> queue;
    queue.push({0, 0, -1});
    int count = 0;
    while (queue.size() != 0) {
        ++count;
        const auto [presses, pattern, lastButtonIndex] = queue.front();
        queue.pop();
        if (pattern == targetLightPattern) {
            return presses;
        } else {
            for (int i = std::max(0,lastButtonIndex); i < buttons.size(); ++i) {
                queue.push({presses+1, pattern ^ buttons[i], i});
            }
        }
    }
    assert(false); //should never reach here
    return -1;
}

int main(int argc, char** argv) {

    std::ifstream is{"input.txt"};
    std::string line;
    std::vector<int> lights; // represent as binary number
    std::vector<std::vector<int>> buttons; // represent as binary number
    std::vector<std::vector<int>> joltages;
    while (std::getline(is, line)) {
        std::string buff;
        std::istringstream ss{line};
        std::vector<int> buttonsFromLine;
        while(std::getline(ss, buff, ' ')) {
            if (buff[0] == '[') {
                int num = 0;
                for (int i = 1; i < buff.size() - 1; ++i) {
                    if (buff[i] == '#') {
                        num += 1 << (i-1);
                    }
                }
                //std::cout << num << "\n";
                lights.push_back(num);
            } else {
                std::string buff2;
                std::istringstream ss2{buff.substr(1, buff.size() - 2)};
                std::vector<int> nums;
                while(std::getline(ss2, buff2, ',')) {
                    nums.push_back(std::stoi(buff2));
                }
                if (buff[0] == '(') {
                    buttonsFromLine.push_back(numsToBinary(nums));
                } else {
                    joltages.push_back(nums);
                }
            }
        }
        buttons.push_back(buttonsFromLine);
    }

    int total = 0;
    for (int i = 0; i < lights.size(); ++i) {
        total += findMinimumButtons(lights[i], buttons[i]);
    }
    std::cout << total << "\n";
}