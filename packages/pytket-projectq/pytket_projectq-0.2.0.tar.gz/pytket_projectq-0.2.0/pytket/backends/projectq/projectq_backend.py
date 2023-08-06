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

"""Methods to allow t|ket> circuits to be ran on ProjectQ simulator
"""
from openfermion import QubitOperator
import projectq
from projectq import MainEngine
from projectq.backends import Simulator
from projectq.cengines import ForwarderEngine
from projectq.ops import All, Measure
from typing import Dict, Iterable, List, Optional, Tuple
import numpy as np

from pytket import Circuit, OpType
from pytket.backends import Backend
from pytket.projectq import tk_to_projectq
from pytket.utils.results import counts_from_shot_table
from pytket.passes import BasePass, RebaseProjectQ
from pytket.predicates import (
    Predicate, GateSetPredicate, NoClassicalControlPredicate,
    NoFastFeedforwardPredicate)

class ProjectQBackend(Backend) :

    def __init__(self) :
        """Backend for running simulations on the ProjectQ simulator.
        """
        super().__init__(shots=True, counts=True, state=True, expectation=True)
        self._backend = Simulator()
        self._cache = {}

    @property
    def required_predicates(self) -> List[Predicate] :
        return [
            NoClassicalControlPredicate(),
            NoFastFeedforwardPredicate(),
            GateSetPredicate({
                OpType.SWAP, OpType.CRz, OpType.CX, OpType.CZ, OpType.H,
                OpType.X, OpType.Y, OpType.Z, OpType.S, OpType.T, OpType.V,
                OpType.Rx, OpType.Ry, OpType.Rz, OpType.Measure})
        ]

    @property
    def default_compilation_pass(self) -> BasePass :
        return RebaseProjectQ()

    def process_circuits(self, circuits:Iterable[Circuit], n_shots:Optional[int]=None, seed:Optional[int]=None, valid_check:bool=True) :
        for circuit in circuits :
            if valid_check and not self.valid_circuit(circuit) :
                raise ValueError("Circuits do not satisfy all required predicates for this backend")
            measures = [-1]*len(circuit.bits)
            for com in circuit:
                if com.op.get_type() == OpType.Measure:
                    measures[com.bits[0].index[0]] = com.qubits[0].index[0]
            print(measures)
            fwd = ForwarderEngine(self._backend)
            eng = MainEngine(backend=self._backend,engine_list=[fwd])
            qureg = eng.allocate_qureg(circuit.n_qubits)
            tk_to_projectq(eng,qureg,circuit,True)
            eng.flush()
            state = eng.backend.cheat()[1] #`cheat()` returns tuple:(a dictionary of qubit indices, statevector)
            results = []
            if n_shots :
                for _ in range(n_shots) :
                    readout = []
                    eng.backend.set_wavefunction(state, qureg)
                    for qb in [q for q in measures if q != -1] :
                        Measure | qureg[qb]
                        readout.append(int(qureg[qb]))
                    results.append(readout)
            All(Measure) | qureg
            eng.flush()
            self._cache.update({circuit : (state, np.asarray(results))})

    def empty_cache(self) :
        self._cache = {}

    def get_shots(self, circuit:Circuit, n_shots:Optional[int]=None, seed:Optional[int]=None, valid_check:bool=True, remove_from_cache:bool=True) -> np.ndarray :
        if circuit not in self._cache :
            if not n_shots :
                raise ValueError("Circuit has not been processed; please specify a number of shots")
            self.process_circuits([circuit], n_shots, seed, valid_check)
        _, shots = self._cache[circuit]
        if remove_from_cache :
            del self._cache[circuit]
        return shots

    def get_counts(self, circuit:Circuit, n_shots:Optional[int]=None, seed:Optional[int]=None, valid_check:bool=True, remove_from_cache:bool=True) -> Dict[Tuple[int, ...], int] :
        return counts_from_shot_table(self.get_shots(circuit, n_shots, seed, valid_check, remove_from_cache))

    def get_state(self, circuit:Circuit, valid_check:bool=True, remove_from_cache:bool=True) -> np.ndarray :
        if circuit not in self._cache :
            self.process_circuits([circuit], valid_check=valid_check)
        state, _ = self._cache[circuit]
        if remove_from_cache :
            del self._cache[circuit]
        return state
    
    def _expectation_value(self, circuit:Circuit, hamiltonian:projectq.ops.QubitOperator) -> complex :
        fwd = ForwarderEngine(self._backend)
        eng = MainEngine(backend=self._backend,engine_list=[fwd])
        qureg = eng.allocate_qureg(circuit.n_qubits)
        tk_to_projectq(eng,qureg,circuit)
        eng.flush()
        energy = eng.backend.get_expectation_value(hamiltonian,qureg)
        All(Measure) | qureg
        return energy
    

    def get_pauli_expectation_value(self, state_circuit:Circuit, pauli:Iterable[Tuple[int,str]]) -> complex :
        """Calculates the expectation value of the given circuit using the built-in ProjectQ functionality
        
        :param state_circuit: Circuit that generates the desired state :math:`\\left|\\psi\\right>`.
        :type state_circuit: Circuit
        :param pauli: Sparse Pauli operator :math:`P` [p1, p2, p3, ...] where each pi = (q, s) with qubit index q and Pauli s ("I", "X", "Y", "Z").
        :type pauli: Iterable[Tuple[int,str]]
        :return: :math:`\\left<\\psi | P | \\psi \\right>`
        :rtype: complex
        """
        return self._expectation_value(state_circuit, projectq.ops.QubitOperator(tuple(pauli)))
    
    def get_operator_expectation_value(self, state_circuit:Circuit, operator:QubitOperator) -> complex :
        """Calculates the expectation value of the given circuit with respect to the operator using the built-in ProjectQ functionality
        
        :param state_circuit: Circuit that generates the desired state :math:`\\left|\\psi\\right>`.
        :type state_circuit: Circuit
        :param operator: Operator :math:`H`.
        :type operator: QubitOperator
        :return: :math:`\\left<\\psi | P | \\psi \\right>`
        :rtype: complex
        """
        ham = projectq.ops.QubitOperator()
        for term, coeff in operator.terms.items() :
            ham += projectq.ops.QubitOperator(tuple(term), coeff)
        return self._expectation_value(state_circuit, ham)
