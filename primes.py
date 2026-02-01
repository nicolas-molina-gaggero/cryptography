from enum import Enum, auto
from functools import reduce
from operator import mul
from typing import List, Self
import random
import bisect
from math import gcd
from modular import pow_mod

class Primality(Enum):
    '''
    The posible results of miller-rabin primality test
    '''
    Prime = auto()
    Composite = auto()
    ProbablyPrime = auto()


def sieve(limit: int) -> List[int]:
    is_prime = [True for _ in range(limit + 1)]
    for p in range(3, limit, 2):
        if is_prime[p]:
            for mul in range(p*p, limit, p):
                is_prime[mul] = False

    primes = [2]
    for p in range(3, limit, 2):
        if is_prime[p]:
            primes.append(p)
    return primes

class PrimeGenerator:
    __slots__ = ['prefilter', 'offsets', 'small_primes_prod', 'rounds']

    def __init__(self: Self, max_prefilter: int = 7, max_small_prime: int = 100, rounds: int = 40):
        primes = sieve(max_small_prime)
        print(primes)
        index = bisect.bisect_right(primes, max_prefilter)
        self.prefilter = reduce(mul, primes[:index])
        self.small_primes_prod = reduce(mul, primes[index:])
        self.offsets = [b for b in range(3, self.prefilter) if gcd(self.prefilter, b) == 1]
        self.rounds =rounds

    def random_prime(self: Self, lower: int, upper: int) -> int:
        while True:
            c = self.prefilter*random.randint(lower//self.prefilter, upper//self.prefilter) + random.choice(self.offsets)
            if gcd(self.small_primes_prod, c) > 1:
                continue
            if miller_rabin(c, self.rounds) != Primality.Composite:
                return c

def miller_rabin(n: int, k: int) -> Primality:
    if (n == 2):
        return Primality.Prime
    if (n % 2 == 0):
        return Primality.Composite
    for _ in range(k):
        match one_round_miller_rabin(n):
            case Primality.Composite:
                return Primality.Composite
            case Primality.Prime:
                return Primality.Prime
            case Primality.ProbablyPrime:
                continue
    return Primality.ProbablyPrime

def one_round_miller_rabin(n: int) -> Primality:
    a = random.randint(2, n - 1)
    g = gcd(a, n)
    if g > 1:
        return Primality.Composite
    k = 0
    q = n - 1
    while (q % 2 == 0):
        q //= 2
        k += 1
    a = pow_mod(a, q, n)
    if a == 1:
        return Primality.ProbablyPrime
    for _ in range(k):
        if a == n-1:
            return Primality.ProbablyPrime
        a = (a*a) % n
    return Primality.Composite
