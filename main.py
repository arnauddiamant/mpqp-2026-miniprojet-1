import argparse

from classic.preprocess import FindCoPrime
from classic.postprocess import PostProcessPeriod

from quantum.quantumSubroutine import ComputePeriods, QuantumSubroutine

def Shor(N: int, maxIterations: int = -1, display_circ: bool = False, DEBUG_MODE: bool = False) -> tuple[int, int | str]:
    maxIterations = N if maxIterations != -1 else N // 2
    f1 = None # Answer, loop until founded
    tested_a = []
    a = None
    if DEBUG_MODE:
        print(f"\n=== Starting Shor's algorithm for N = {N} ===")
    while f1 == None:
        # Finding an a not already tested
        a = FindCoPrime(N)
        while a in tested_a:
            a = FindCoPrime(N)
        if DEBUG_MODE:
            print(f"\nTesting a = {a} (already tested: {tested_a})")
        tested_a.append(a)

        # Create the circuit
        circ = QuantumSubroutine(N, a, DEBUG_MODE=DEBUG_MODE)
        if display_circ:
            circ.pretty_print()

        # Compute periods
        periods = ComputePeriods(circ)

        if DEBUG_MODE:
            print(f"Potential periods founded: {periods}")

        # Test all periods
        for r in periods:
            if DEBUG_MODE:
                print(f"\nTesting period r = {r}")
            
            # Compute primes
            f1, f2 = PostProcessPeriod(N, a, r, DEBUG_MODE=DEBUG_MODE)
            
            if f1 != None: # Primes are founded
                return f1, f2
        
        # If every a has been tested, end the loop
        # a is odd and include in [3, N[, which is N-3 elements
        if len(tested_a) >= maxIterations:
            if DEBUG_MODE:
                print(f"Number of tries to high, stopping.")
            return None, "Not found"


if __name__ == "__main__":
    # Parsing arguments
    # Create a parser object
    parser = argparse.ArgumentParser()

    # Add argument(s)
    parser.add_argument('--debug', action='store_true', help="Enable debug mode")
    parser.add_argument('--circuit', action='store_true', help="Print quantum circuit")

    # Parse arguments
    args = parser.parse_args()

    DEBUG_MODE = False
    if args.debug:
        DEBUG_MODE = True

    # Select a number
    N = int(input("Choose a number to factorize: "))

    # If number is even, exit
    if not (N & 1):
        if DEBUG_MODE:
            print("N is even. Computing solution.")
        print(f"{N} = 2 * {N >> 1}")
        exit()

    if DEBUG_MODE:
        print("N is odd. Computing solution.")

    # Use the shor's algorithm to factorize N
    f1, f2 = Shor(N, display_circ=args.circuit, DEBUG_MODE=DEBUG_MODE)
    if f1 == None:
        print("No factorization founded.")
    else:
        print(f"\nResult: {N} = {f1} * {f2}")