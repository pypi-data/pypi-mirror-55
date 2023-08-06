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

# This test is stolen primarily from https://github.com/ProjectQ-Framework/ProjectQ/blob/develop/examples/variational_quantum_eigensolver.ipynb

import os
on_travis = os.environ.get('TRAVIS')=='true'

import warnings
warnings.filterwarnings("ignore", category=PendingDeprecationWarning)

if not on_travis:
    import projectq
    from pytket.backends.projectq import ProjectQBackend

from openfermion import QubitOperator
from pytket.circuit import Circuit
from pytket.predicates import CompilationUnit
from pytket.utils.expectations import _get_pauli_expectation_value, _get_operator_expectation_value
import pytest
import math
import numpy as np

#TODO add tests for `get_operator_expectation_value`

def circuit_gen(measure=False):
    c = Circuit(2)
    c.H(0)
    c.CX(0,1)
    return c

@pytest.mark.filterwarnings("ignore::PendingDeprecationWarning")
@pytest.mark.skipif(on_travis, reason="this is not tested on travis")
def test_statevector():
    c = circuit_gen()
    b = ProjectQBackend()
    state = b.get_state(c)
    assert np.allclose(state, [math.sqrt(0.5), 0, 0, math.sqrt(0.5)], atol=1e-10)
    
@pytest.mark.filterwarnings("ignore::PendingDeprecationWarning")
@pytest.mark.filterwarnings("ignore:Casting complex values")
@pytest.mark.skipif(on_travis, reason="this is not tested on travis")
def test_pauli_statevector():
    c = Circuit(2)
    c.Rz(0.5,0)
    b = ProjectQBackend()
    zi = [(0,'Z')]
    assert math.isclose(_get_pauli_expectation_value(c, zi, b),1)
    c.X(0)
    assert math.isclose(_get_pauli_expectation_value(c, zi, b),-1)
    
@pytest.mark.filterwarnings("ignore::PendingDeprecationWarning")
@pytest.mark.filterwarnings("ignore:Casting complex values to real discards the imaginary part")
@pytest.mark.skipif(on_travis, reason="this is not tested on travis")
def test_operator_statevector():
    c = circuit_gen()
    b = ProjectQBackend()
    zz = QubitOperator('Z0 Z1', 1.)
    assert math.isclose(_get_operator_expectation_value(c, zz, b),1.)
    c.X(0)
    assert math.isclose(_get_operator_expectation_value(c, zz, b),-1.)
    
@pytest.mark.filterwarnings("ignore::PendingDeprecationWarning")
@pytest.mark.skipif(on_travis, reason="this is not tested on travis")
def test_measures():
    n_qbs = 12
    c = Circuit(n_qbs, n_qbs)
    x_qbs = [2, 5, 7, 10]
    for i in x_qbs:
        c.X(i)
    for i in range(n_qbs-1):
        c.Measure(i, i)
    b = ProjectQBackend()
    shots = b.get_shots(c,10)
    print(shots)
    all_ones = True
    all_zeros = True
    for i in x_qbs:
        all_ones = all_ones and np.all(shots[:,i])
    for i in range(n_qbs-1):
        if i not in x_qbs:
            all_zeros = all_zeros and (not np.any(shots[:,i]))
    assert all_ones
    assert all_zeros

@pytest.mark.filterwarnings("ignore::PendingDeprecationWarning")
@pytest.mark.skipif(on_travis, reason="this is not tested on travis")
def test_default_pass():
    b = ProjectQBackend()
    comp_pass = b.default_compilation_pass
    circ = circuit_gen(False)
    cu = CompilationUnit(circ)
    comp_pass.apply(cu)
    c = cu.circuit
    for pred in b.required_predicates :
        assert pred.verify(c)
    assert b.valid_circuit(c)

if __name__ =='__main__':
    test_statevector()
    test_pauli_statevector()
    test_operator_statevector()
    test_measures()