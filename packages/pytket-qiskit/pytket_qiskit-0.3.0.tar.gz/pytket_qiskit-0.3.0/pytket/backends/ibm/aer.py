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

from typing import Dict, Iterable, List, Optional, Tuple
import numpy as np
from qiskit import Aer
from qiskit.compiler import assemble
from qiskit.providers import BaseBackend
from qiskit.providers.aer.noise import NoiseModel

from pytket import Architecture, Circuit, OpType
from pytket.backends import Backend
from pytket.qiskit import tk_to_qiskit
from pytket.predicates import (
    Predicate, GateSetPredicate, NoClassicalControlPredicate,
    NoFastFeedforwardPredicate)
from pytket.passes import BasePass, gen_routing_pass, SynthesiseIBM
from .ibm import _convert_bin_str, _shots_from_result

class AerBackend(Backend) :

    def __init__(self, noise_model:Optional[NoiseModel]=None) :
        """Backend for running simulations on the Qiskit Aer QASM simulator.

        :param noise_model: Noise model to apply during simulation. Defaults to None.
        :type noise_model: Optional[NoiseModel], optional
        """
        super().__init__(shots=True, counts=True)
        self._backend = Aer.get_backend('qasm_simulator')
        self._noise_model = noise_model
        if noise_model :
            self._device = _process_model(noise_model)
        self._cache = {}

    @property
    def required_predicates(self) -> List[Predicate] :
        return [
            NoClassicalControlPredicate(),
            NoFastFeedforwardPredicate(),
            GateSetPredicate(_aer_ops.union({OpType.Measure}))
        ]

    @property
    def default_compilation_pass(self) -> BasePass :
        return SynthesiseIBM()

    def process_circuits(self, circuits:Iterable[Circuit], n_shots:Optional[int]=None, seed:Optional[int]=None, valid_check:bool=True) :
        cs = list(circuits)
        if valid_check :
            for c in cs :
                for p in self.required_predicates :
                    if not p.verify(c) :
                        raise ValueError("Circuits do not satisfy all required predicates for this backend")
        qcs = list(map(tk_to_qiskit, cs))
        qobj = assemble(qcs, shots=n_shots, memory=True, seed_simulator=seed)
        job = self._backend.run(qobj)
        for i, c in enumerate(cs) :
            self._cache[c] = (job, i)

    def empty_cache(self) :
        self._cache = {}

    def get_shots(self, circuit:Circuit, n_shots:Optional[int]=None, seed:Optional[int]=None, valid_check:bool=True, remove_from_cache:bool=True) -> np.ndarray :
        if circuit not in self._cache :
            if not n_shots :
                raise ValueError("Circuit has not been processed; please specify a number of shots")
            self.process_circuits([circuit], n_shots, seed, valid_check)
        job, i = self._cache[circuit]
        if remove_from_cache :
            del self._cache[circuit]
        return _shots_from_result(i, job.result(), True)

    def get_counts(self, circuit:Circuit, n_shots:Optional[int]=None, seed:Optional[int]=None, valid_check:bool=True, remove_from_cache:bool=True) -> Dict[Tuple[int, ...], int] :
        if circuit not in self._cache :
            if not n_shots :
                raise ValueError("Circuit has not been processed; please specify a number of shots")
            self.process_circuits([circuit], n_shots, seed, valid_check)
        job, i = self._cache[circuit]
        counts = job.result().get_counts(i)
        if remove_from_cache :
            del self._cache[circuit]
        return {tuple(_convert_bin_str(b)) : c for b, c in counts.items()}

class AerStateBackend(Backend) :

    def __init__(self) :
        """Backend for running simulations on the Qiskit Aer Statevector simulator.
        """
        super().__init__(state=True)
        self._backend = Aer.get_backend('statevector_simulator')
        self._cache = {}

    @property
    def required_predicates(self) -> List[Predicate] :
        return _pure_aer_predicates

    @property
    def default_compilation_pass(self) -> BasePass :
        return SynthesiseIBM()

    def process_circuits(self, circuits:Iterable[Circuit], n_shots:Optional[int]=None, seed:Optional[int]=None, valid_check:bool=True) :
        cs = list(circuits)
        if valid_check :
            for c in cs :
                for p in self.required_predicates :
                    if not p.verify(c) :
                        raise ValueError("Circuits do not satisfy all required predicates for this backend")
        qcs = list(map(lambda c : tk_to_qiskit(c), cs))
        qobj = assemble(qcs)
        job = self._backend.run(qobj)
        for i, c in enumerate(cs) :
            self._cache[c] = (job, i)

    def empty_cache(self) :
        self._cache = {}

    def get_state(self, circuit:Circuit, valid_check:bool=True, remove_from_cache:bool=True) -> np.ndarray :
        if circuit not in self._cache :
            self.process_circuits([circuit], valid_check=valid_check)
        job, i = self._cache[circuit]
        if remove_from_cache :
            del self._cache[circuit]
        return np.asarray(job.result().get_statevector(i, decimals=16))

class AerUnitaryBackend(Backend) :

    def __init__(self) :
        """Backend for running simulations on the Qiskit Aer Unitary simulator.
        """
        super().__init__(unitary=True)
        self._backend = Aer.get_backend('unitary_simulator')
        self._cache = {}

    @property
    def required_predicates(self) -> List[Predicate] :
        return _pure_aer_predicates

    @property
    def default_compilation_pass(self) -> BasePass :
        return SynthesiseIBM()

    def process_circuits(self, circuits:Iterable[Circuit], n_shots:Optional[int]=None, seed:Optional[int]=None, valid_check:bool=True) :
        cs = list(circuits)
        if valid_check :
            for c in cs :
                for p in self.required_predicates :
                    if not p.verify(c) :
                        raise ValueError("Circuits do not satisfy all required predicates for this backend")
        qcs = list(map(lambda c : tk_to_qiskit(c), cs))
        qobj = assemble(qcs)
        job = self._backend.run(qobj)
        for i, c in enumerate(cs) :
            self._cache[c] = (job, i)

    def empty_cache(self) :
        self._cache = {}

    def get_unitary(self, circuit:Circuit, valid_check:bool=True, remove_from_cache:bool=True) -> np.ndarray :
        if circuit not in self._cache :
            self.process_circuits([circuit], valid_check=valid_check)
        job, i = self._cache[circuit]
        if remove_from_cache :
            del self._cache[circuit]
        return np.asarray(job.result().get_unitary(i, decimals=16))

_aer_ops = {
    OpType.U1,  OpType.U2,  OpType.U3,  OpType.CX,
    OpType.CZ,  OpType.CU1, OpType.noop,OpType.X,
    OpType.Y,   OpType.Z,   OpType.H,   OpType.S,
    OpType.Sdg, OpType.T,   OpType.Tdg, OpType.CCX,
    OpType.SWAP,OpType.Unitary1qBox,    OpType.Unitary2qBox
}

_pure_aer_predicates = [
    NoClassicalControlPredicate(),
    NoFastFeedforwardPredicate(),
    GateSetPredicate(_aer_ops)
]

def _process_model(noise_model:NoiseModel) -> dict:
    # obtain approximations for gate errors from noise model by using probability of "identity" error
    _gate_str_2_optype = {
        'u1': OpType.U1,
        'u2': OpType.U2,
        'u3': OpType.U3,
        'cx': OpType.CX
    }
    errors = [e for e in noise_model.to_dict()['errors'] if e['type'] == 'qerror']
    link_ers = []
    node_ers = []
    coupling_map = []
    for error in errors:
        name = error['operations']
        if len(name) > 1:
            raise RuntimeWarning("Error applies to multiple gates.")
        name = name[0]
        qubits = error['gate_qubits'][0]
        gate_fid = error['probabilities'][-1]
        if len(qubits) == 1:
            node_ers.append((qubits[0], _gate_str_2_optype[name], gate_fid))
        elif len(qubits) == 2:
            link_ers.append((qubits, _gate_str_2_optype[name], gate_fid))
            # to simulate a worse reverse direction square the fidelity
            link_ers.append((qubits[::-1], _gate_str_2_optype[name], (gate_fid)**2))
            coupling_map.append(qubits)

    arc = Architecture(coupling_map)
    return {'coupling': coupling_map, 'architecture': arc, 'single_qubit_errors': node_ers, 'two_qubit_errors':link_ers}
