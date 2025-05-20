# Authors
- DIAMANT Arnaud
- FLORION Thomas
- KIFFER Mathéo
- SEFRIN Quentin

# Dependencies:
- Python3.12
- [MPQP](https://mpqpdoc.colibri-quantum.com/getting-started) python library

# Subject: Implement Shor's algorithm with MPQP
**Difficulty:** 4.5/5

Shor's algorithm is probably the most famous quantum algorithm. It allows you to
factor out products of prime numbers. It has an exponential speedup compared to
its classical counterpoint ($O(log(N))$ compared to 
$O(e^{1.9log(N)^\frac13log(log(N))^\frac23})$)

Shor's algorithm, if ever implemented would easily break cryptographic scemes
based on big prime number's product being hard to factor, such as RSA,
Diffie-Hellman, etc...

## Explaination

Shor's algorithm starts with a preprocessing step, followed by a quantum
subroutine consisting in finding the order of a periodic function.

The order finding subroutine relies on the QPE, itself based on the inverse QFT.

These are the steps you'll need to follow to implement Shor's algorithm.

## Goal

Your implementation should take as input an integer and return its factors.

Good luck !