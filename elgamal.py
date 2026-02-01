from math import gcd
from typing import Self, Tuple
from primes import PrimeGenerator, naive_factor
from modular import inverse_mod, pow_mod
import random

class ElGamalDecryptor:
    '''
    Class that implements an RSA decryptor with a public and private keys
    '''
    __slots__ = ['_p', '_g', '_pub', '_priv']
    # Private
    def _generate_keys(self: Self):
        self._priv = random.randint(2, self._p - 1)
        self._pub = pow_mod(self._g, self._priv, self._p)

    # Public
    def __init__(self: Self, p: int, g: int):
        self._p = p
        self._g = g
        self._generate_keys()

    def decrypt(self: Self, c: Tuple[int, int]) -> int:
        '''
        Given a message m is encrypted as
        c1 = g^x (mod p)
        c2 = m*(k_pub)^x (mod p)
        we can decrypt it as 
        m = c1*(c2)^{-k_priv} (mod p)
        Args:
            c (int,int): Tuple with the encrypted messages
        Result:
            the decrypted message
        '''
        c1, c2 = c
        temp = inverse_mod(pow_mod(c1, self._priv, self._p), self._p)
        if temp is None:
            raise RuntimeError("")
        return (c2 * temp) % self._p

    def get_pub(self: Self) -> int:
        """
        Returns the public key.
        """
        return self._pub

class ElGamalEncryptor:
    __slots__ = ['_p', '_g', '_pub']
    # Public
    def __init__(self: Self, pub: int, p: int, g: int):
        self._pub = pub
        self._p = p
        self._g = g

    def encrypt(self: Self, message: int):
        x = random.randint(2, self._p - 1)
        c1 = pow_mod(self._g, x, self._p)
        c2 = (message * pow_mod(self._pub, x, self._p)) % self._p
        return (c1, c2)

def main():
    pg = PrimeGenerator(11, 2000)
    p = pg.random_prime(2**127, 2**128)
    q = (p - 1) // 2
    fact = naive_factor(q)

    if fact is not None:
        print(fact)
    else:
        print("Couldn't factor it")

    g = 2
    alice = ElGamalDecryptor(p, g)
    pub = alice.get_pub()
    bob = ElGamalEncryptor(pub, p, g)

    message = random.randint(2, p - 1)
    cipher_text = bob.encrypt(message)
    deciphered = alice.decrypt(cipher_text)
    print(f'message=\n\t{message}')
    print(f'deciphered=\n\t{deciphered}')

if __name__ == '__main__':
    main()
