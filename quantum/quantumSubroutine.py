# choose t number of qubits in the phase register
from mpqp import QCircuit
from mpqp.gates import *
from mpqp.measure import BasisMeasure
from classic.preprocess import FindCoPrime, PrecomputePowers, FindPhaseRegisterSize, FindModularRegisterSize

def QuantumModularExponentiation(Circ, a: int, n: int, N: int) -> None:
    t = len(Circ)
    C = PrecomputePowers(a, N, t)
    for i in range(t + n - 1):
        if Circ[i] == 1:
            Circ.add(C[i % t], i + t)

def InverseQFT(Circ, start: int, end: int) -> None:
    for i in range(end - 1, start - 1, -1):
        Circ.add(H(i))
        for j in range(i - 1, start - 1, -1):
            Circ.add(CRk(-2 ** (i - j), j, i))

    for i in range((end - start) // 2):
        Circ.add(SWAP(start + i, end - i - 1))


def QuantumSubroutine(a: int, N: int) -> QCircuit:

    t = FindPhaseRegisterSize(N)
    n = FindModularRegisterSize(N)
    # prepare two register: |0> \tensor t \tensor |0> \tensor n
    Circ = QCircuit(t + n)

    # Apply Hadamard on each qubit of register 1
    for i in range(t):
        Circ.add(H(i))

    QuantumModularExponentiation(Circ, a, n, N)

        # Apply inverse QFT to phase register
    InverseQFT(Circ, 0, t)

    # Measure the phase register
    Circ.add(BasisMeasure(targets=list(range(t)), shots=1024))

    return Circ
