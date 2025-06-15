import numpy as np
import random

def FindCoPrime(N: int) -> int:
    """
    We search a random a, such that 1 < a < N and GCD(a, N) = 1
    :param N: The upper bound of a, and the size of the first qubit register
    :return: The integer a
    """
    if (not(N & 1)):
        # If by error N is even, we know we have a working a
        return 2
    while True:
        # We check that a is not even, since it is not a factor of an odd N
        a = random.randrange(3, N, 2)
        g = np.gcd(a, N)
        if (g != 1):
            return (int) (g)
        else:
            return (int) (a)

def BitSize(n: int) -> int:
    """
    Find the number of qubits needed to represent an integer
    :param n: Integer we are trying to represent
    :return: Number of qubits needed to represent n
    """
    return (int) (np.ceil(np.log2(n)))

def PrecomputePowers(a: int, N: int, q: int) -> list[int]:
    """
    Precomputes the table of [a^(2^q) mod N]
    :param a: Integer prime with N
    :param N: Modulo
    :param q: Upper bound of the power
    :return: The table with pre-processed values
    """
    table = [a % N]
    for _ in range(1, q):
        table.append((table[-1] * table[-1]) % N)
    return table
