import argparse

import time
import sys
import os

# Temporary add parent folder to path in order to import main
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import Shor


def IsValidFactorization(N, f1, f2):
    return f1 is not None and f2 is not None and f1 * f2 == N


def IsValidFactorizationPrimes(N, f1, f2):
    return f1 is None and f2 == "Not found"


def TestShorBasic(test_cases: list[int], TIMER: bool = False, cases: int = 0):
    if cases == 0:
        cases = len(test_cases)

    for i in range(cases):
        N = test_cases[i]
        print(f"\nTesting N = {N}")

        start_time = time.time()
        f1, f2 = Shor(N, DEBUG_MODE=False)
        elapsed = time.time() - start_time

        print(f"Found factors: {f1}, {f2}")
        if TIMER:
            print(f"    Time to completion: {elapsed:.2f} seconds")
        assert IsValidFactorization(N, f1, f2), f"Incorrect factors for N = {N}"


def TestShorPrime(test_cases: list[int], TIMER: bool = False):
    for N in test_cases:
        print(f"\nTesting N = {N}")

        start_time = time.time()
        f1, f2 = Shor(N, DEBUG_MODE=False)
        elapsed = time.time() - start_time

        print(f"Found factors: {f1}, {f2}")
        if TIMER:
            print(f"    Time to completion: {elapsed:.2f} seconds")
        assert IsValidFactorizationPrimes(N, f1, f2), f"Factors found for prime N = {N}"


def RestrictedInt(min_val, max_val):
    def Validator(val):
        if val is None:
            return None
        try:
            ivalue = int(val)
        except ValueError:
            raise argparse.ArgumentTypeError(f"Invalid int value: {val}")
        if ivalue < min_val or ivalue > max_val:
            raise argparse.ArgumentTypeError(f"Value must be between {min_val} and {max_val}")
        return ivalue
    return Validator


if __name__ == "__main__":
    # Test cases
    basic_cases = [
        187, # 11 * 17
        527, # 17 * 31
        1131, # 29 * 39
        3995, # 85 * 47
    ]

    hard_cases = [
        6693, # 97 * 69
        16837, # 113 * 149
        18536, # 118 * 157
    ]

    prime_cases = [
        47, # No answer
        113, # No answer
    ]

    # Parsing arguments for selecting tests
    # Create a parser object
    parser = argparse.ArgumentParser()

    # Add argument(s)
    parser.add_argument('-t', '--timer', action='store_true', help="Enable timer for computing")
    parser.add_argument('-a', '--all', action='store_true', help="Launch every tests")
    parser.add_argument('-b', '--basic', action='store_true', help="Launch test for basic cases")
    parser.add_argument('-p', '--primes', action='store_true', help="Launch test for prime cases")
    parser.add_argument('-H', '--hard', nargs='?', const=3, type=RestrictedInt(1, len(hard_cases)), metavar='CASES',
                        help=f"Launch test for hard cases (up to several minutes). Optionally specify number of cases (1 to {len(hard_cases)})")

    # Parse arguments
    args = parser.parse_args()

    TIMER = args.timer

    if args.all:
        TestShorBasic(test_cases=basic_cases, TIMER=TIMER)
        TestShorPrime(test_cases=prime_cases, TIMER=TIMER)
        TestShorBasic(test_cases=hard_cases, TIMER=TIMER)

    else:
        if args.basic:
            TestShorBasic(test_cases=basic_cases, TIMER=TIMER)

        if args.primes:
            TestShorPrime(test_cases=prime_cases, TIMER=TIMER)

        if args.hard is not None:
            TestShorBasic(test_cases=hard_cases, TIMER=TIMER, cases=args.hard)

    print("\nAll tests passed.")