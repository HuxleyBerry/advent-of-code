#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>

int main(int argc, char** argv) {
    int part = atoi(argv[1]);

    std::ifstream is("input.txt");
    std::string line;
    int pos = 50;
    int count = 0;
    while (std::getline(is, line)) {
        int sign = line[0] == 'L' ? -1 : 1;
        std::cout << "oldpos: " << pos << "\n";
        int oldPos = pos;
        pos += sign * atoi(line.c_str() + 1);
        int posNormalised = ((pos % 100) + 100) % 100;
        if (part == 2)
        {
            if (sign == -1) {
                if (oldPos == 0) {
                    --count;
                }
                if (posNormalised == 0) {
                    ++count;
                }
            }
            count += std::abs((pos - posNormalised)/100);
        }
        pos = posNormalised;
        if (part == 1) {
            if (pos == 0)
            {
                ++count;
            }
        }
    }
    std::cout << count << "\n";
}