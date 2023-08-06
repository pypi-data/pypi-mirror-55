# Copyright 2019 Cambridge Quantum Computing
#
# Licensed under a Non-Commercial Use Software Licence (the "Licence");
# you may not use this file except in compliance with the Licence.
# You may obtain a copy of the Licence in the LICENCE file accompanying
# these documents or at:
#
#     https://cqcl.github.io/pytket/build/html/licence.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the Licence is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the Licence for the specific language governing permissions and
# limitations under the Licence, but note it is strictly for non-commercial use.

from pytket.pyzx import tk_to_pyzx, pyzx_to_tk
from pytket.circuit import Circuit
from pytket.backends.ibm import IBMQBackend, AerBackend, AerStateBackend
from qiskit import IBMQ
import math
import numpy as np
import pytest

@pytest.mark.filterwarnings("ignore:strict=False")
def test_statevector():
    b = AerStateBackend()
    circ = Circuit(3)
    circ.H(2)
    circ.X(0)
    circ.H(0)
    circ.CX(0,1)
    circ.CZ(1,2)
    circ.Z(1)
    circ.T(2)
    circ.Rx(0.3333,1)
    circ.Rz(0.3333,1)
    # for command in circ:
    #     print(command)
    zxcirc = tk_to_pyzx(circ)
    state = b.get_state(b.compile_circuit(circ))
    circ2 = pyzx_to_tk(zxcirc)
    # for command in circ2:
    #     print(command)
    state2 = b.get_state(b.compile_circuit(circ2))
    assert np.allclose(state, state2, atol=1e-10)

if __name__ =='__main__':
    test_statevector()