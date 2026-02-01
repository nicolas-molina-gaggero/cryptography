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
    '''
    Return a list of primes until `limit`. It implements a simple Eratosthenes sieve
    we mainly use it here for testing divisibility for small primes
    '''
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
    '''
    Class for generating random prime numbers and random safe prime (TODO: implement this) numbers in a given range
    '''
    __slots__ = ['prefilter', 'offsets', 'small_primes_prod', 'rounds']

    def __init__(self: Self, max_prefilter: int = 7, max_small_prime: int = 100, rounds: int = 40):
        primes = sieve(max_small_prime)
        index = bisect.bisect_right(primes, max_prefilter)
        self.prefilter = reduce(mul, primes[:index])
        self.small_primes_prod = reduce(mul, primes[index:])
        self.offsets = [b for b in range(3, self.prefilter) if gcd(self.prefilter, b) == 1]
        self.rounds =rounds

    '''
    Generates a random prime p between lower and upper. (p - 1)/2 might have small divisors
    so its not appropiate for many ciphers.
    Args:
        lower: lower limit to generate the prime
        upper: upper limit to gtenerate the prime
    Returns:
        A likely prime
    '''
    def random_prime(self: Self, lower: int, upper: int) -> int:
        while True:
            c = self.prefilter*random.randint(lower//self.prefilter, upper//self.prefilter) + random.choice(self.offsets)
            if gcd(self.small_primes_prod, c) > 1:
                continue
            if miller_rabin(c, self.rounds) != Primality.Composite:
                return c
    # def random_safe_prime(self: Self, lower: int, upper: int) -> int:
    #     pass

def miller_rabin(n: int, rounds: int) -> Primality:
    '''
    Miller-Rabin primality test
    if it returns ProbablyPrime the probability
    of actualy being a primes is at least 75%
    Args:
        n: the number to be tested
        rounds: how many rounds of the test are performed
    Returns:
        a Primality enum class.
            Composite: The number is sure to be composite
            Prime: The number is sure to be prime (only returned when n = 2)
            ProbablyPrime: The number is at least (1 - 1/4**rounds) likely to be prime
    '''
    if (n == 2):
        return Primality.Prime
    if (n % 2 == 0):
        return Primality.Composite
    for _ in range(rounds):
        match one_round_miller_rabin(n):
            case Primality.Composite:
                return Primality.Composite
            case Primality.Prime:
                return Primality.Prime
            case Primality.ProbablyPrime:
                continue
    return Primality.ProbablyPrime

def one_round_miller_rabin(n: int) -> Primality:
    '''
    One round of Miller-Rabin primality testing
    if it returns ProbablyPrime the probability
    of actualy being a primes is at least 75%
    Args:
        n: the number to be tested
    Returns:
        a Primality enum class.
            Composite: The number is sure to be composite
            ProbablyPrime: The number is at least 75% likely to be prime
    '''
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
