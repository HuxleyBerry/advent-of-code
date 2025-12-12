#include "fractions.h"
#include <iostream>
#include <numeric>
#include <stdexcept>

Fraction::Fraction(int n, int d){
    if (d == 0) {
        std::cout << n << " " << d << "\n";
        throw std::invalid_argument("Denominator must not be zero.");
    }
    int gcd = std::gcd(n,d);
    numerator = n/gcd;
    denominator = d/gcd;
}

Fraction::Fraction(const Fraction& f): numerator{f.numerator}, denominator{f.denominator} {}

Fraction::Fraction(int integer): Fraction(integer, 1){}

Fraction& Fraction::operator=(const Fraction& f) {
    numerator = f.numerator;
    denominator = f.denominator;
    return *this;
}

Fraction Fraction::operator+=(const Fraction& f) {
    return *this = *this + f;
}

Fraction Fraction::operator-=(const Fraction& f) {
    return *this = *this - f;
}

Fraction Fraction::operator/=(const Fraction& f) {
    return *this = *this / f;
}

Fraction Fraction::operator+(const Fraction& f) const{
    //std::cout << "addtion: " << numerator << " " << denominator << " " << f.numerator << " " << f.denominator << "\n";
    auto x = Fraction(numerator*f.denominator + f.numerator*denominator, f.denominator*denominator);
    //std::cout << "??\n";
    return Fraction(numerator*f.denominator + f.numerator*denominator, denominator*f.denominator);
}

Fraction Fraction::operator*(const Fraction& f) const{
    return Fraction(numerator*f.numerator, denominator*f.denominator);
}

Fraction Fraction::operator/(const Fraction& f) const{
    if (f.numerator == 0) {
        throw std::invalid_argument("Divisor must be nonzero");
    }
    return Fraction(numerator*f.denominator, denominator*f.numerator);
}

Fraction Fraction::operator-() const{
    return Fraction(-numerator, denominator);
}

Fraction Fraction::operator-(const Fraction &f) const{
    return *this + (-f);
}

bool Fraction::operator==(const Fraction& f) const {
    return numerator*f.denominator == denominator*f.numerator;
}

bool Fraction::operator!=(const Fraction& f) const {
    return !(*this==f);
}

bool Fraction::operator>(const Fraction& f) const {
    bool sameSign = denominator * f.denominator > 0;
    return sameSign ? numerator*f.denominator > denominator*f.numerator : numerator*f.denominator < denominator*f.numerator;
}

bool Fraction::operator<(const Fraction& f) const {
    bool sameSign = denominator * f.denominator > 0;
    return sameSign ? numerator*f.denominator < denominator*f.numerator : numerator*f.denominator > denominator*f.numerator;
}

bool Fraction::isInt() const {
    return numerator%denominator == 0;
}

int Fraction::toInt() const {
    return numerator/denominator;
}