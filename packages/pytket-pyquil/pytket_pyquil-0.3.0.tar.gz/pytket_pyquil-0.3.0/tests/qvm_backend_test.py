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
import numpy as np
from pytket.circuit import Circuit
from pytket.predicates import CompilationUnit
from pytket.routing import Architecture, route
from pytket.backends.forest import ForestBackend, ForestStateBackend
from pytket.utils.expectations import _get_pauli_expectation_value

import pytest
import math
import docker
from shutil import which

@pytest.fixture(scope="module")
def qvm(request) :
    print("running qvm container")
    dock = docker.from_env()
    container = dock.containers.run(image="rigetti/qvm", command="-S", detach=True, ports={5000:5000}, remove=True)
    # container = dock.containers.run(image="rigetti/qvm", command="-S", detach=True, publish_all_ports=True, remove=True)
    request.addfinalizer(container.stop)
    return None

@pytest.fixture(scope="module")
def quilc(request) :
    dock = docker.from_env()
    container = dock.containers.run(image="rigetti/quilc", command="-S", detach=True, ports={5555:5555}, remove=True)
    request.addfinalizer(container.stop)
    return None

def circuit_gen(measure=False):
    c = Circuit(2,2)
    c.H(0)
    c.CX(0,1)
    if measure :
        c.measure_all()
    return c

@pytest.mark.skipif(which('docker') is None, reason="Can only run Rigetti QVM if docker is installed")
def test_statevector(qvm, quilc):
    c = circuit_gen()
    b = ForestStateBackend()
    state = b.get_state(c)
    state /= state[0]
    correct = np.asarray([math.sqrt(0.5), 0, 0, math.sqrt(0.5)])
    correct /= correct[0]
    assert np.allclose(state, correct, atol=1e-10)

@pytest.mark.skipif(which('docker') is None, reason="Can only run Rigetti QVM if docker is installed")
@pytest.mark.filterwarnings("ignore:strict=False")
def test_sim(qvm, quilc):
    c = circuit_gen(True)
    b = ForestBackend("9q-square")
    c = b.compile_circuit(c)
    shots = b.get_shots(c,1024)
    print(shots)

@pytest.mark.skipif(which('docker') is None, reason="Can only run Rigetti QVM if docker is installed")
def test_measures(qvm, quilc):
    n_qbs = 9
    c = Circuit(n_qbs,n_qbs)
    x_qbs = [2, 5, 7, 8]
    for i in x_qbs:
        c.X(i)
    c.measure_all()
    b = ForestBackend("9q-square")
    c = b.compile_circuit(c)
    shots = b.get_shots(c,10)
    print(shots)
    all_ones = True
    all_zeros = True
    for i in x_qbs:
        all_ones = all_ones and np.all(shots[:,i])
    for i in range(n_qbs):
        if i not in x_qbs:
            all_zeros = all_zeros and (not np.any(shots[:,i]))
    assert all_ones
    assert all_zeros

@pytest.mark.skipif(which('docker') is None, reason="Can only run Rigetti QVM if docker is installed")
def test_pauli_statevector(qvm, quilc):
    c = Circuit(2,2)
    c.Rz(0.5,0)
    b = ForestStateBackend()
    zi = [(0,'Z')]
    assert _get_pauli_expectation_value(c, zi, b) == 1
    c.X(0)
    assert _get_pauli_expectation_value(c, zi, b) == -1

@pytest.mark.skipif(which('docker') is None, reason="Can only run Rigetti QVM if docker is installed")
def test_pauli_sim(qvm, quilc):
    c = Circuit(2,2)
    c.Rz(0.5,0)
    b = ForestBackend("9q-square")
    zi = [(0,'Z')]
    energy = _get_pauli_expectation_value(c, zi, b, 10)
    assert abs(energy-1) < 0.001
    c.X(0)
    energy = _get_pauli_expectation_value(c, zi, b, 10)
    assert abs(energy+1) < 0.001

@pytest.mark.skipif(which('docker') is None, reason="Can only run Rigetti QVM if docker is installed")
def test_counts(qvm, quilc) :
    c = circuit_gen(True)
    b = ForestBackend("9q-square")
    c = b.compile_circuit(c)
    counts = b.get_counts(c, 10)
    assert list(counts.keys()) == [(0,0), (1,1)]

def test_default_pass():
    b = ForestBackend("9q-square")
    comp_pass = b.default_compilation_pass
    circ = circuit_gen(False)
    cu = CompilationUnit(circ)
    comp_pass.apply(cu)
    c = cu.circuit
    for pred in b.required_predicates :
        assert pred.verify(c)

if __name__ == '__main__' :
    test_statevector(None, None)
    test_sim(None, None)
    test_measures(None, None)
    # test_device()
    test_pauli_statevector(None, None)
    test_pauli_sim(None, None)
    test_counts(None, None)