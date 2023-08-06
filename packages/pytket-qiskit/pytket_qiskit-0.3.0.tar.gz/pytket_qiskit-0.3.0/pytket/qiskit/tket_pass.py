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

import qiskit
from qiskit.dagcircuit import DAGCircuit
from qiskit.providers import BaseBackend
from qiskit.transpiler.basepasses import TransformationPass, BasePass as qBasePass
from qiskit.converters import circuit_to_dag, dag_to_circuit
from typing import Optional

from pytket.passes import (
    BasePass, gen_directed_cx_routing_pass, SynthesiseIBM,
    OptimisePhaseGadgets, SequencePass)
from pytket.predicates import CompilationUnit
from .qiskit_convert import qiskit_to_tk, tk_to_qiskit, _process_device

class TketPass(TransformationPass):
    """The :math:`\\mathrm{t|ket}\\rangle` compiler to be plugged in to the Qiskit compilation sequence"""
    filecount = 0

    def __init__(self, backend:BaseBackend, tket_pass:Optional[BasePass]=None, name:str="T|KET>") :
        """Wraps a pytket compiler pass as a :py:class:`qiskit.transpiler.TransformationPass`.
        A :py:class:`qiskit.dagcircuit.DAGCircuit` is converted to a pytket :py:class:`Circuit`.
        If specified, `tket_pass` will be run, otherwise a default pass is used. The circuit is
        then routed and rebased for the `backend`, and converted back.
        
        :param backend: The Qiskit backend to target
        :type backend: BaseBackend
        :param tket_pass: The pytket compiler pass to run. Defaults to None
        :type tket_pass: Optional[BasePass], optional
        :param name: Readable name for the :py:class:`qiskit.transpiler.TransformationPass`. Defaults to "T|KET>"
        :type name: str, optional
        """
        qBasePass.__init__(self)
        self.name = name
        if not isinstance(backend, BaseBackend) :
            raise ValueError("Requires BaseBackend instance")
        if not backend.configuration().coupling_map :
            self._pass = SynthesiseIBM()
            return
        self._device = _process_device(backend)
        if tket_pass :
            passlist = [tket_pass]
        else :
            passlist = [OptimisePhaseGadgets()]
        passlist.append(gen_directed_cx_routing_pass(self._device))
        passlist.append(SynthesiseIBM())
        self._pass = SequencePass(passlist)

    def run(self, dag:DAGCircuit) -> DAGCircuit :
        """Run a preconfigured optimisation pass on the circuit and route for the given backend.

        :param dag: The circuit to optimise and route

        :return: The modified circuit
        """
        qc = dag_to_circuit(dag)
        circ = qiskit_to_tk(qc)
        cu = CompilationUnit(circ)
        self._pass.apply(cu)
        circ = cu.circuit
        qc = tk_to_qiskit(circ)
        newdag = circuit_to_dag(qc)
        newdag.name = dag.name
        return newdag
