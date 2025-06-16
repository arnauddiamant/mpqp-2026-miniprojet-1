# choose t number of qubits in the phase register
import numpy as np

from mpqp import QCircuit
from mpqp.gates import *
from mpqp.execution import run, IBMDevice
from mpqp.measures import BasisMeasure
from quantum.CustomControlledGate import *

from classic.preprocess import BitSize
from quantum.qft import AddQFTToCircuit


def QuantumModularExponentiation(circ: QCircuit, N: int, a: int,  t: int, n: int) -> None:
    """
    Apply the modular exponentiation on the circuit,
    using the first register as controls and the second register as targets
    :param circ: Qauntum circuit on which the exponentiation is applied
    :param N: Integer we need to factorize
    :param a: A coprime of N
    :param t: Size of the first register
    :param n: Size of the second register
    :return: None
    """
    for i in range(t):
        """
        Uk =
            | 1       0        |
            | 0  e^(2πi*a/N)^k |
        with k = 2^i
        """
        mat = np.array([[1, 0], [0, np.exp(2*np.pi*1j*a*(1 << i)/N)]], dtype=complex)
        for j in range(n):
            circ.add(CustomControlledGate([i], CustomGate(UnitaryMatrix(mat), [j+t])))


def QuantumSubroutine(N: int, a: int, DEBUG_MODE: bool = False) -> QCircuit:
    """
    Construct a quantum circuit for solving Shor's
    algorithm with the given parameters
    :param N: Integer we need to factorize
    :param a: A coprime of N
    :param DEBUG_MODE: A boolean for managing debug output
    :return: A QCircuit that can be run to solve Shor
    """
    t = n = BitSize(N)

    if DEBUG_MODE:
        print(f"Creating circuit with {t+n} qubits ({t} + {n} ancillas)")

    # prepare two register: |0⟩^(⊗t) ⊗ |0⟩^(⊗n)
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


def ComputePeriods(circ: QCircuit, DEBUG_MODE: bool = False) -> list[int]:
    """
    This function takes a quantum circuit (generated from QuantumSubroutine),
    emulates it and return the result (most probable periods (above a threshold)).
    :param circ: Qauntum circuit to run
    :param DEBUG_MODE: A boolean for managing debug output
    :return: A list containing the most probable periods found
    """
    if DEBUG_MODE:
        print(f"Emulating circuit.")
    result = run(circ, IBMDevice.AER_SIMULATOR)

    # Getting only non-0 results
    results = [(i, result.probabilities[i]) for i in range(len(result.probabilities)) if result.probabilities[i] != 0]
    if DEBUG_MODE:
        print(f"Simulation results non-zero: {results}")

    # Compute threshold
    threshold = np.percentile([results[i][1] for i in range(len(results))], 90)

    # Return only 10% of most probable answers
    return [results[i][0] for i in range(len(results)) if results[i][1] >= threshold]