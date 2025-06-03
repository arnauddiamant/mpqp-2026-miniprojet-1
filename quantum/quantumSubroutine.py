# choose t number of qubits in the phase register
from mpqp import QCircuit, QBit, ApplyControlledUnitary
from scipy import log2
from classic.preprocess import FindCoPrime, PrecomputePowers, FindPhaseRegisterSize, FindModularRegisterSize

def QuantumModularExponentiation(x: int, y: int,a: int, n: int, N: int) -> None:
    t = len(x)
    C = PrecomputePowers(a, N, t)
    for i in range(t-1):
        if x[i] == 1:
            C = ApplyControlledUnitary(C, i, a, N)

def QuantumSubroutine(N: int) -> None:

    t = FindPhaseRegisterSize(N)
    n = FindModularRegisterSize(N)
    
    # prepare two register: |0> \tensor t \tensor |0> \tensor n
    Register1 = QCircuit(t)
    Register2 = QCircuit(n)
    
    # Apply Hadamard on each qubit of register 1
    for i in range(t):
        Register1.H(QBit(i))
    

