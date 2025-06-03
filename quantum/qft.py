from mpqp import QCircuit
from mpqp.gates import *


"""
This function add a QFT at the end of the circuit
"""
def AddQFTToCircuit(circ: QCircuit) -> None:
    nbQubits : int = circ.nb_qubits
    
    for i in range(nbQubits):
        circ.add(H(i))

        for j in range(i + 1, nbQubits):
            circ.add(CRk(j-i+1, j, i))
    
    for i in range((nbQubits // 2)):
        SWAP(i, nbQubits - i - 1)
