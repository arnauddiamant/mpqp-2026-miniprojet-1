from mpqp import QCircuit, Barrier
from mpqp.gates import *
from mpqp.measures import BasisMeasure
from mpqp.execution import run, AWSDevice

def basicCircuit():
    circ = QCircuit(2)
    circ.add([H(0), CNOT(0, 1), Barrier(), BasisMeasure(shots=1000)])
    circ.pretty_print()

    print(run(circ, [AWSDevice.BRAKET_LOCAL_SIMULATOR]))

if __name__ == "__main__":
    basicCircuit()