# choose t number of qubits in the phase register
import numpy as np

from mpqp import QCircuit
from mpqp.gates import *
from mpqp.execution import run, IBMDevice
from mpqp.measures import BasisMeasure
from quantum.CustomControlledGate import *

from classic.preprocess import FindPhaseRegisterSize, FindModularRegisterSize
from quantum.qft import AddQFTToCircuit

def QuantumModularExponentiation(circ: QCircuit, N: int, a: int,  t: int, n: int) -> None:
    for i in range(t):
        # Uk =
        # 1     0
        # 0 e^(2πi*a/N)^k
        # avec k = 2^i
        mat = np.array([[1, 0], [0, np.exp(2*np.pi*1j*a*(1 << i)/N)]], dtype=complex)
        for j in range(n):
            circ.add(CustomControlledGate([i], CustomGate(UnitaryMatrix(mat), [j+t])))


def QuantumSubroutine(N: int, a: int, DEBUG_MODE: bool = False) -> QCircuit:
    t = FindPhaseRegisterSize(N)
    n = FindModularRegisterSize(N)

    if DEBUG_MODE:
        print(f"Creating circuit with {t+n} qubits ({t} + {n} ancillas)")

    # prepare two register: |0> \tensor t \tensor |0> \tensor n
    circ = QCircuit(t + n)

    # Apply Hadamard on each qubit of register 1
    for i in range(t):
        circ.add(H(i))
    
    # Set to |1> every ancilla qubits
    for i in range(n):
        circ.add(X(t + i))

    QuantumModularExponentiation(circ, N, a, t, n)

    AddQFTToCircuit(circ, t)

    circ.add(BasisMeasure(list(range(t)), shots=100))
    return circ



"""
This function takes a quantum circuit (generated from QuantumSubroutine),
emulates it and return the result (most probable periods (above a threshold)).
"""
def ComputePeriods(circ: QCircuit, DEBUG_MODE: bool = False) -> int:
    if DEBUG_MODE:
        print(f"Emulating circuit.")
    # print(repr(circ))
    result = run(circ, IBMDevice.AER_SIMULATOR)

    # Getting only non-0 results
    results = [(i, result.probabilities[i]) for i in range(len(result.probabilities)) if result.probabilities[i] != 0]
    if DEBUG_MODE:
        print(f"Simulation results non-zero: {results}")

    # Compute threshold
    threshold = np.percentile([results[i][1] for i in range(len(results))], 90)

    # Return only 10% of most probable answers
    return [results[i][0] for i in range(len(results)) if results[i][1] >= threshold]