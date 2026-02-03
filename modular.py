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
