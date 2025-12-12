#include <sstream>

class Fraction {
    private:
    int numerator;
    int denominator;

    public:
    Fraction(int n, int d);

    Fraction(const Fraction& f);

    Fraction(int integer);

    Fraction& operator=(const Fraction& f);

    Fraction operator+=(const Fraction& f);

    Fraction operator-=(const Fraction& f);

    Fraction operator/=(const Fraction& f);

    Fraction operator+(const Fraction& f) const;

    Fraction operator*(const Fraction& f) const;

    Fraction operator/(const Fraction& f) const;

    Fraction operator-() const;

    Fraction operator-(const Fraction &f) const;

    bool operator==(const Fraction& f) const;

    bool operator!=(const Fraction& f) const;

    bool operator>(const Fraction& f) const;

    bool operator<(const Fraction& f) const;

    bool isInt() const;

    int toInt() const;

    friend std::ostream& operator<<(std::ostream& os, const Fraction& f);
};