from mpqp import QCircuit, Barrier
from mpqp.gates import *
from mpqp.measures import BasisMeasure
from mpqp.execution import run, AWSDevice

from quantum.qft import AddQFTToCircuit

def basicCircuit():
    circ = QCircuit(3)

    AddQFTToCircuit(circ)

    circ.pretty_print()
    #print(run(circ, [AWSDevice.BRAKET_LOCAL_SIMULATOR]))

if __name__ == "__main__":
    basicCircuit()