class Complex:
    def __init__(self, re=0, im=0):
        self.re = re
        self.im = im

    def __add__(self, other):
        return Complex(self.re + other.re, self.im + other.im)

    def __mul__(self, other):
        return 

    def __str__(self):
        if self.im >= 0:
            return f'{self.re} + {self.im}i'
        else:
            return f'{self.re}-{abs(self.im)}i'

    def __abs__(self):
        return (self.re ** 2 + self.im ** 2) ** 0, 5


c1 = Complex(1, 2)
c2 = Complex(2, 3)
print(c1 * c2)