# choose t number of qubits in the phase register
from mpqp import QCircuit
from mpqp.gates import *
from mpqp.execution import run, AWSDevice
from classic.preprocess import FindCoPrime, PrecomputePowers, FindPhaseRegisterSize, FindModularRegisterSize

def QuantumModularExponentiation(Circ, a: int, n: int, N: int) -> None:
    t = len(Circ)
    C = PrecomputePowers(a, N, t)
    for i in range(t + n - 1):
        if Circ[i] == 1:
            Circ.add(C[i % t], i + t)


def QuantumSubroutine(a: int, N: int) -> QCircuit:

    t = FindPhaseRegisterSize(N)
    n = FindModularRegisterSize(N)
    # prepare two register: |0> \tensor t \tensor |0> \tensor n
    Circ = QCircuit(t + n)

    # Apply Hadamard on each qubit of register 1
    for i in range(t):
        Circ.add(H(i))

    QuantumModularExponentiation(Circ, a, n, N)



"""
This function takes a quantum circuit (generated from QuantumSubroutine),
emulates it and return the result (most probable period r).
"""
def ComputePeriod(circ: QCircuit) -> int:
    result = run(circ, AWSDevice.BRAKET_LOCAL_SIMULATOR)

    r = 0
    for i in range(1, len(result.counts)):
        r = i if result.counts[i] > result.counts[r] else r
    
    return r