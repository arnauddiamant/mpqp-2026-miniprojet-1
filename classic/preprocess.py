import numpy as np

def FindCoPrime(N: int) -> int:
    """
    We search a random a, such that 1 < a < N and GCD(a, N) = 1
    :param N: The upper bound of a, and the size of the first qubit register
    :return: The integer a
    """
    if (N%2 == 0):
        return 2
    while True:
        a = np.random.randint(2, N)
        g = np.gcd(a, N)
        if (g != 1):
            return g
        else:
            return a

def FindPhaseRegisterSize(N: int) -> int:
    """
    Find the size of the phase register
    :param N: Size of the first register
    :return: Size of the phase register
    """
    return np.ceil(2 * np.log2(N))

def FindModularRegisterSize(N: int) -> int:
    """
    Find the size of the modular register
    :param N: Size of the first register
    :return: Size of the modular register
    """
    return np.ceil(np.log2(N))

def PrecomputePowers(a: int, N: int, q: int) -> [int]:
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
