from mpqp import QCircuit

from classic.preprocess import FindCoPrime
from classic.postprocess import PostProcessPeriod

from quantum.quantumSubroutine import ComputePeriods, QuantumSubroutine

def Shor(N: int, maxIterations: int = -1) -> tuple[int, int | str]:
    maxIterations = N if maxIterations != -1 else N // 2
    f1 = None # Answer, loop until founded
    tested_a = []
    a = None
    while f1 == None:
        # Finding an a not already tested
        a = FindCoPrime(N)
        while a in tested_a:
            a = FindCoPrime(N)
        tested_a.append(a)

        # Create the circuit
        circ = QuantumSubroutine(N, a)

        # Compute periods
        periods = ComputePeriods(circ)

        # Test all periods
        for r in periods: 
            # Compute primes
            f1, f2 = PostProcessPeriod(N, a, r)
            
            if f1 != None: # Primes are founded
                return f1, f2
        
        # If every a has been tested, end the loop
        # a is odd and include in [3, N[, which is N-3 elements
        if len(tested_a) >= maxIterations:
            return None, "Not found"


if __name__ == "__main__":
    print(Shor(15))