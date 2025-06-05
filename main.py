from mpqp import QCircuit, Barrier
from mpqp.gates import *
from mpqp.measures import BasisMeasure
from mpqp.execution import run, AWSDevice

from quantum.qft import AddQFTToCircuit
from quantum.quantumSubroutine import ComputePeriod

def basicCircuit():
    circ = QCircuit(5)

    AddQFTToCircuit(circ, 3)
    circ.pretty_print()

    circ.add(BasisMeasure(shots=100))
    print(f"Period is {ComputePeriod(circ)}")

if __name__ == "__main__":
    basicCircuit()