import numpy as np

"""
This function post process what the quantum circuit returned: the period r.
It needs the number we want to factorize N, and the random number we chose a.

Returns: a tuple with the result (int, int), or (None, "error message") if not found
"""
def PostProcessPeriod(N : int, a : int, r : int) -> tuple[int, int | str]:
    # If r is odd, stop
    if r % 2 != 0:
        return None, "Period is odd; try a different a"
    
    # Compute x = a^(r/2) mod N
    x = pow(a, r // 2, N)
    
    # If x + 1 == 0 mod N, stop
    if x + 1 == N:
        return None, "x + 1 ≡ 0 mod N; try a different a"
    
    # Compute a^(r/2) ± 1 mod N
    factor1 = np.gcd(x - 1, N)
    factor2 = np.gcd(x + 1, N)
    
    return factor1, factor2
