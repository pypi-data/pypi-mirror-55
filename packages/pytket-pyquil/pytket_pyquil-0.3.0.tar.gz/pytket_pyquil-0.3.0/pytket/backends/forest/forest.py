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

from openfermion import QubitOperator
import numpy as np
from typing import Dict, Iterable, List, Optional, Tuple
from pyquil import get_qc
from pyquil.api import WavefunctionSimulator, QuantumComputer
from pyquil.paulis import PauliTerm, ID, PauliSum

from pytket import Architecture, Circuit, OpType
from pytket.backends import Backend
from pytket.pyquil import tk_to_pyquil
from pytket.utils.results import counts_from_shot_table
from pytket.device import Device, GateError, GateErrorContainer
from pytket.passes import (
    BasePass, gen_routing_pass, gen_decompose_routing_gates_to_cxs_pass,
    SequencePass, SynthesiseIBM, RebaseQuil)
from pytket.predicates import (
    Predicate, GateSetPredicate, NoClassicalControlPredicate,
    NoFastFeedforwardPredicate, ConnectivityPredicate)

class ForestBackend(Backend) :

    def __init__(self, qc_name:str, simulator:bool=True) :
        """Backend for running circuits on a Rigetti QCS device or simulating with the QVM.
        
        :param qc_name: The name of the particular QuantumComputer to use. See the pyQuil docs for more details.
        :type qc_name: str
        :param simulator: Simulate the device with the QVM (True), or run on the QCS (False). Defaults to True.
        :type simulator: bool, optional
        """
        super().__init__(shots=True, counts=True)
        self._qc = get_qc(qc_name, as_qvm=simulator)
        self._device, self._architecture = _process_device(self._qc)
        self._cache = {}
    
    @property
    def required_predicates(self) -> List[Predicate] :
        return [
            NoClassicalControlPredicate(),
            NoFastFeedforwardPredicate(),
            GateSetPredicate({OpType.CZ, OpType.Rx, OpType.Rz, OpType.Measure}),
            ConnectivityPredicate(self._architecture)
        ]

    @property
    def default_compilation_pass(self) -> BasePass :
        passlist = [
            gen_routing_pass(self._device),
            gen_decompose_routing_gates_to_cxs_pass(self._device),
            SynthesiseIBM(),
            RebaseQuil()
        ]
        return SequencePass(passlist)

    def process_circuits(self, circuits:Iterable[Circuit], n_shots:Optional[int]=None, seed:Optional[int]=None, valid_check:bool=True) :
        if not n_shots :
            raise ValueError("Parameter n_shots is required for ForestBackend")
        for circuit in circuits :
            if not self.valid_circuit(circuit) :
                raise ValueError("Circuits do not satisfy all required predicates for this backend")
            p = tk_to_pyquil(circuit)
            p.wrap_in_numshots_loop(n_shots)
            ex = self._qc.compiler.native_quil_to_executable(p)
            self._cache.update({circuit : np.asarray(self._qc.run(ex))})

    def empty_cache(self) :
        self._cache = {}

    def get_shots(self, circuit:Circuit, n_shots:Optional[int]=None, seed:Optional[int]=None, valid_check:bool=True, remove_from_cache:bool=True) -> np.ndarray :
        if circuit not in self._cache :
            if not n_shots :
                raise ValueError("Circuit has not been processed; please specify a number of shots")
            self.process_circuits([circuit], n_shots, seed, valid_check)
        shots = self._cache[circuit]
        if remove_from_cache :
            del self._cache[circuit]
        return shots

    def get_counts(self, circuit:Circuit, n_shots:Optional[int]=None, seed:Optional[int]=None, valid_check:bool=True, remove_from_cache:bool=True) -> Dict[Tuple[int, ...], int] :
        return counts_from_shot_table(self.get_shots(circuit, n_shots, seed, valid_check, remove_from_cache))

class ForestStateBackend(Backend) :

    def __init__(self) :
        """Backend for running simulations on the Rigetti QVM Wavefunction Simulator.
        """
        super().__init__(state=True, expectation=True)
        self._sim = WavefunctionSimulator()
        self._cache = {}
    
    @property
    def required_predicates(self) -> List[Predicate] :
        return [
            NoClassicalControlPredicate(),
            NoFastFeedforwardPredicate(),
            GateSetPredicate({
                OpType.X, OpType.Y, OpType.Z, OpType.H, OpType.S, OpType.T,
                OpType.Rx, OpType.Ry, OpType.Rz, OpType.CZ, OpType.CX,
                OpType.CCX, OpType.CU1, OpType.U1, OpType.SWAP})
        ]

    @property
    def default_compilation_pass(self) -> BasePass :
        return RebaseQuilPass

    def process_circuits(self, circuits:Iterable[Circuit], n_shots:Optional[int]=None, seed:Optional[int]=None, valid_check:bool=True) :
        for circuit in circuits :
            if not self.valid_circuit(circuit) :
                raise ValueError("Circuits do not satisfy all required predicates for this backend")
            p = tk_to_pyquil(circuit)
            self._cache.update({circuit : np.asarray(self._sim.wavefunction(p).amplitudes)})

    def empty_cache(self) :
        self._cache = {}

    def get_state(self, circuit:Circuit, valid_check:bool=True, remove_from_cache:bool=True) -> np.ndarray :
        if circuit not in self._cache :
            self.process_circuits([circuit], valid_check=valid_check)
        state = self._cache[circuit]
        if remove_from_cache :
            del self._cache[circuit]
        return state

    def _gen_PauliTerm(self, term:Iterable[Tuple[int,str]], coeff:complex=1.) -> PauliTerm :
        pauli_term = ID() * coeff
        for idx, p in term :
            pauli_term *= PauliTerm(p, idx)
        return pauli_term
    
    def get_pauli_expectation_value(self, state_circuit:Circuit, pauli:Iterable[Tuple[int,str]]) -> complex :
        """Calculates the expectation value of the given circuit using the built-in QVM functionality
        
        :param state_circuit: Circuit that generates the desired state :math:`\\left|\\psi\\right>`.
        :type state_circuit: Circuit
        :param pauli: Sparse Pauli operator :math:`P` [p1, p2, p3, ...] where each pi = (q, s) with qubit index q and Pauli s ("I", "X", "Y", "Z").
        :type pauli: Iterable[Tuple[int,str]]
        :return: :math:`\\left<\\psi | P | \\psi \\right>`
        :rtype: complex
        """
        prog = tk_to_pyquil(state_circuit)
        pauli_term = self._gen_PauliTerm(pauli)
        return self._sim.expectation(prog, [pauli_term])

    def get_operator_expectation_value(self, state_circuit:Circuit, operator:QubitOperator) -> complex :
        """Calculates the expectation value of the given circuit with respect to the operator using the built-in QVM functionality
        
        :param state_circuit: Circuit that generates the desired state :math:`\\left|\\psi\\right>`.
        :type state_circuit: Circuit
        :param operator: Operator :math:`H`.
        :type operator: QubitOperator
        :return: :math:`\\left<\\psi | P | \\psi \\right>`
        :rtype: complex
        """
        prog = tk_to_pyquil(state_circuit)
        pauli_sum = PauliSum([self._gen_PauliTerm(term, coeff)] for term, coeff in operator.terms.items())
        return self._sim.expectation(prog, [pauli_sum])

def _process_device(qc : QuantumComputer) -> Tuple[Device, Architecture] :
    specs = qc.device.get_specs()

    coupling_map = [[n, ni] for n, neigh_dict in qc.qubit_topology().adjacency() for ni, _ in neigh_dict.items()]

    node_ers_dict = {}
    link_ers_dict = {}

    device_node_ers = specs.f1QRB_std_errs()
    device_link_ers = specs.fCZ_std_errs()
    device_ROs = specs.fROs()
    device_t1s = specs.T1s()
    device_t2s = specs.T2s()

    for index in qc.qubits() :
        error_cont = GateErrorContainer()
        error_cont.add_readout(device_ROs[index])
        error_cont.add_t1_time(device_t1s[index])
        error_cont.add_t2_time(device_t2s[index])
        error_cont.add_error((OpType.Rx, GateError(device_node_ers[index], 1.)))
        error_cont.add_error((OpType.Rz, GateError(device_node_ers[index], 1.)))
        node_ers_dict[index] = error_cont
    
    for (a, b), err in device_link_ers.items() :
        error_cont = GateErrorContainer()
        error_cont.add_error((OpType.CZ, GateError(err, 1.)))
        link_ers_dict[(a,b)] = error_cont
        link_ers_dict[(b,a)] = error_cont

    arc = Architecture(coupling_map)
    # convert qubits to architecture Nodes
    node_ers_dict = {arc.map_vertex(
        q_index): ers for q_index, ers in node_ers_dict.items()}
    link_ers_dict = {(arc.map_vertex(q_indices[0]), arc.map_vertex(
        q_indices[1])): ers for q_indices, ers in link_ers_dict.items()}

    device = Device(node_ers_dict, link_ers_dict, arc)
    return device, arc
