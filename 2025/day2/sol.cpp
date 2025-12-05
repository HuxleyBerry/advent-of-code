#include <iostream>
#include <fstream>
#include <utility>
#include <vector>
#include <cstdlib>
#include <string>
#include <cassert>
#include <cmath>
#include <limits>

const int MAX_POWER = std::floor(std::log10(std::numeric_limits<long>::max()));
const std::vector<int> primes {2,3,5,7,9,11,13};

int countDigits(long num){
    if (num < 10){
        return 1;
    } else {
        return 1 + countDigits(num/10);
    }
}

long tenthPower(int power){
    assert(power <= MAX_POWER);
    long val = 1;
    for (int i = 0; i < power; ++i) {
        val *= 10;
    }
    return val;
}

long getDuplicatorMultiplier(int tenthPower, int divisionCount) {
    long answer = 1;
    for (int i = 1; i < divisionCount; ++i) {
        answer = answer*tenthPower + 1;
    }
    return answer;
}

long getOnesOnly(int length) {
    long answer = 1;
    for (int i = 1; i < length; ++i) {
        answer = answer*10 + 1;
    }
    return answer;
}

long sumMultiplesInRange(long min, long max, int divisor) {
    long minDivided = ((min + divisor - 1)/divisor);
    long maxDivided = (max/divisor);
    return divisor * ((maxDivided+1)*maxDivided - (minDivided-1)*minDivided)/2;
}

long countInvalid(long min, long max, int divisor, bool considerFuture=false) {
    long oldMin = min;
    long oldMax = max;
    if (int digitCount = countDigits(min); digitCount%divisor != 0)
    {
        min = tenthPower(divisor * ((divisor - 1 + digitCount)/divisor) - 1);
    }
    if (int digitCount = countDigits(max); digitCount%divisor != 0)
    {
        max = tenthPower(divisor*(digitCount/divisor)) - 1;
    }
    if (min > max) {
        return 0;
    }
    int lowerDigitCount = countDigits(min);
    int upperDigitCount = countDigits(max);
    int tenthPowerForDivision = tenthPower(lowerDigitCount/divisor);
    long duplicatorMultiplier = getDuplicatorMultiplier(tenthPowerForDivision, divisor);
    assert(lowerDigitCount == upperDigitCount);
    bool doubleCountOffsetRequired = false;
    if (considerFuture) {
        for (int p: primes) {
            if (p > divisor && lowerDigitCount%p == 0) {
                doubleCountOffsetRequired = true;
                break;
            }
        }
    }

    return sumMultiplesInRange(min, max, duplicatorMultiplier) - (doubleCountOffsetRequired  ? sumMultiplesInRange(min, max,  getOnesOnly(lowerDigitCount)) : 0);
}

int main(int argc, char** argv) {
    std::ifstream is {"input.txt"};
    std::string line;
    std::vector<std::pair<long,long>> input;
    while (std::getline(is, line, ',')) {
        size_t pos = line.find('-');
        assert(pos != std::string::npos);
        std::string left = line.substr(0, pos);
        std::string right = line.substr(pos+1);
        input.emplace_back(std::atol(left.c_str()), std::atol(right.c_str()));
    }
    long count = 0;
    for (const auto& pair: input) {
        if (std::atoi(argv[1]) == 1) {
            count += countInvalid(pair.first, pair.second, 2);
        } else if (std::atoi(argv[1]) == 2){
            for (const int prime: primes) {
                count += countInvalid(pair.first, pair.second, prime, true);
            }
        }
    }
    std::cout << count << "\n";
}