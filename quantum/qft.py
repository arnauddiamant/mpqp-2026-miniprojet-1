from mpqp import QCircuit
from mpqp.gates import *


"""
This function add a QFT at the end of the circuit on the Nth first qubits (default: all qubits)
"""
def AddQFTToCircuit(circ: QCircuit, N: int = None) -> None:
    nbQubits : int = N if N != None else circ.nb_qubits
    
    for i in range(nbQubits):
        circ.add(H(i))

        for j in range(i + 1, nbQubits):
            circ.add(CRk(j-i+1, j, i))
    
    for i in range((nbQubits // 2)):
        SWAP(i, nbQubits - i - 1)
