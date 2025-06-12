import numpy as np

"""
This function post process what the quantum circuit returned: the period r.
It needs the number we want to factorize N, and the random number we chose a.

Returns: a tuple with the result (int, int), or (None, "error message") if not found
"""
def PostProcessPeriod(N : int, a : int, r : int, DEBUG_MODE: bool = False) -> tuple[int, int | str]:
    # If r is odd, stop
    if r % 2 != 0:
        if DEBUG_MODE:
            print(f"{r} is odd, try another.")
        return None, "Period is odd; try a different a"
    
    # Compute x = a^(r/2) mod N
    x = pow(a, r // 2, N)
    if DEBUG_MODE:
        print(f"Computing x = a^(r/2) mod N: x = {x}")
    
    
    # If x + 1 == 0 mod N, stop
    if x + 1 == N:
        if DEBUG_MODE:
            print("x + 1 ≡ 0 mod N; try a different a")
        return None, "x + 1 ≡ 0 mod N; try a different a"
    
    # Compute a^(r/2) ± 1 mod N
    factor1 = np.gcd(x - 1, N)
    factor2 = np.gcd(x + 1, N)
    if DEBUG_MODE:
        print(f"Computing factors: x+1 = {factor1}, x-1 = {factor2}")

    # Avoid getting 1 or N
    if factor1 == 1 or factor1 == N:
        if factor2 == 1 or factor2 == N:
            return None, "Period gives 1 or N only"
        return factor2, N // factor2
    
    if factor2 == 1 or factor2 == N:
        return factor1, N // factor1
    
    # Both factors are different from 1 and N
    return factor1, factor2
