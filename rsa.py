from math import gcd
from typing import Self
from primes import *
from modular import *

class RCADecryptor:
    __slots__ = ['_n', '_pub', '_priv']
    # Private
    def _generate_keys(self: Self, bits: int):
        assert bits > 0, "Bits must be a positive integer."
        lower = 1 << bits
        upper = lower << 1
        pg = PrimeGenerator(5, 30)
        p = pg.random_prime(lower, upper)
        while (q := pg.random_prime(lower, upper)) == p:
            pass
        self._n = p*q
        g = gcd(p - 1, q - 1)
        phi = ((p - 1)*(q - 1)) // g

        while True:
            self._priv = random.randint(2,phi - 1)
            if (pub := inverse_mod(self._priv, phi)) is not None:
                break
        self._pub = pub

    # Public
    def __init__(self: Self, bits: int):
        assert bits > 0, "Bits must be a positive integer."
        self._generate_keys(bits)

    def decrypt(self: Self, cipher_text: int):
        return pow_mod(cipher_text, self._priv, self._n)

    def get_pub(self: Self) -> int:
        return self._pub

    def get_mod(self: Self) -> int:
        return self._n

class RCAEncryptor:
    __slots__ = ['_n', '_pub']
    # Public
    def __init__(self: Self, pub: int, n: int):
        self._n = n
        self._pub = pub

    def encrypt(self: Self, message: int):
        return pow_mod(message, self._pub, self._n)



def main():
    alice = RCADecryptor(1024)
    n = alice.get_mod()
    pub = alice.get_pub()
    bob = RCAEncryptor(pub, n)
    message = random.randint(2, n - 1)
    cipher_text = bob.encrypt(message)
    deciphered = alice.decrypt(cipher_text)
    print(f'message=\n\t{message}')
    print(f'deciphered=\n\t{deciphered}')

if __name__ == '__main__':
    main()
