


class factors:

    def __init__(self, num, factor = 1) -> None:
        self.num = num
        self.factor = factor
        if type(num) == factors:
            self.num = num.num
            self.factor = factor * num.factor
        if type(factor) == factors:
            a = self.num if self.num is not None else 1
            b = factor.num if factor.num is not None else 1
            self.num = a*b
            self.factor = self.factor.factor

    def __mul__(self, __value) -> object:
        return factors(self.num, __value * self.factor)
    
    def __add__(self, __value) -> object:
        if type(__value) == int or type(__value) == factors:
            __value = factors(__value)
            if self.num == __value.num:
                return factors(self.num, self.factor + __value.factor)
            return pair(self, -__value)
        return NotImplemented
    
    def __radd__(self, __value) -> object:
        return self + __value
    
    def __sub__(self, __value) -> object:
        return self + __value*-1
    
    def __rsub__(self, __value) -> object:
        return -self + __value

    def __neg__(self) -> object:
        return self * -1
    
    def __str__(self) -> str:
        return '{}({})'.format(self.num if self.num != None else 1, self.factor)
    
    def __repr__(self) -> str:
        return 'factors[ {} ]'.format(str(self))
    
    @property
    def value(self) -> int:
        return self.num * self.factor if self.num is not None else self.factor

class pair:

    def __init__(self, f1:factors, f2:factors) -> None:
        self.f1 = factors(f1)
        self.f2 = factors(f2)
    
    def __mul__(self, __value) -> object:
        return pair(self.f1 * __value, self.f2 * __value)
    
    def __add__(self, __value) -> object:
        if type(__value) == int or type(__value) == factors:
            __value = factors(__value)
            if self.f1.num == __value.num:
                return pair(self.f1 + __value, self.f2)
            if self.f2.num == __value.num:
                return pair(self.f1, self.f2 - __value)
        if type(__value) == pair:
            return self + __value.f1 - __value.f2
    
    def __radd__(self, __value) -> object:
        return self + __value
    
    def __sub__(self, __value) -> object:
        return self + (__value*-1)
    
    def __rsub__(self, __value) -> object:
        return -self + __value
    
    def __neg__(self) -> object:
        return self * -1
    
    def __str__(self) -> str:
        return '{} - {}'.format(self.f1, self.f2)
    
    def __repr__(self) -> str:
        return 'pair[ {} = {} ]'.format(self.value, str(self))
    
    def rotate(self) -> object:
        return pair(-self.f2, -self.f1)
    
    @property
    def value(self) -> int:
        return self.f1.value - self.f2.value
    
def bezout_id(k, n):
    if k == 0:
        return pair(factors(k, 0), n)
    r0 = pair(k, factors(n, 0))
    r1 = n - r0 * (n//r0.value)
    while(r1.value != 0):
        r2 = r0 - r1 * (r0.value//r1.value)
        r0, r1 = r1, r2
    return r0

def optimal_t(j, k, n):
    eq = bezout_id(k % n, n)
    j = j % n
    if j % eq.value != 0:
        return -1, eq.value   # doesn't exist
    return eq.f1.factor * (j//eq.value) % n, k * n // eq.value  # t, lcm

def lcm(args):
    lcm = 1
    for n in args:
        lcm = n * lcm // bezout_id(n, lcm).value
    return lcm