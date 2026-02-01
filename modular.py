from typing import Optional
def inverse_mod(a: int, m: int) -> Optional[int]:
    '''
    Computes the inverse of a mod m
    If a is not coprime with m it returns None (in this case there is no inverse).
    '''
    u0,u1 = 1,0

    b = m
    while b:
        q = a // b
        a, b = b, a % b
        u0, u1 = u1, u0 - q*u1
    if a != 1:
        return None

    return u0 if u0 > 0 else u0 + m

def pow_mod(a: int,b: int,n: int) -> int:
    '''
    Computes a**b (mod n) efficiently
    '''
    if b == 0:
        return 1
    if b == 1:
        return a % n
    result = 1
    while (b > 0):
        if b % 2 == 1:
            result = (result * a) % n
        a = (a*a) % n
        b >>= 1
    return result
