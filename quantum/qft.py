from mpqp import QCircuit
from mpqp.gates import *


"""
This function add a QFT at the end of the circuit on the Nth first qubits (default: all qubits)
"""
def AddQFTToCircuit(circ: QCircuit, N: int = None) -> None:
    nbQubits : int = N if N != None else circ.nb_qubits

    for i in range(nbQubits):
        idx = nbQubits - i - 1
        circ.add(H(idx))

        for j in range(idx - 1, -1, -1):
            circ.add(CRk(nbQubits - j, j, idx))
