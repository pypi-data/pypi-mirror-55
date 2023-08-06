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

"""Methods to allow conversion between pyQuil and t|ket> data types
"""

from pyquil import Program
from pyquil.quilbase import Gate, Measurement, Declare, Pragma, Halt
from pyquil.quilatom import Qubit
from pyquil.device import AbstractDevice, ISA, isa_to_graph, specs_from_graph
from collections import namedtuple

from pytket.circuit import Circuit, Op, OpType, UnitID

from sympy import pi

from typing import Union

_known_quil_gate = {
    "X" : OpType.X,
    "Y" : OpType.Y,
    "Z" : OpType.Z,
    "H" : OpType.H,
    "S" : OpType.S,
    "T" : OpType.T,
    "RX" : OpType.Rx,
    "RY" : OpType.Ry,
    "RZ" : OpType.Rz,
    "CZ" : OpType.CZ,
    "CNOT" : OpType.CX,
    "CCNOT" : OpType.CCX,
    "CPHASE" : OpType.CU1,
    "PHASE" : OpType.U1,
    "SWAP" : OpType.SWAP
}

_known_quil_gate_rev = {v : k for k, v in _known_quil_gate.items() }

def pyquil_to_tk(prog: Program) -> Circuit:
    """
    Convert a :py:class:`pyquil.Program` to a :math:`\\mathrm{t|ket}\\rangle` :py:class:`Circuit` .
    Note that not all pyQuil operations are currently supported by pytket.

    :param prog: A circuit to be converted

    :return: The converted circuit
    """
    qubits = prog.get_qubits()
    tkc = Circuit()
    qmap = {}
    for q in qubits :
        id = UnitID('q', q)
        tkc.add_qubit(id)
        qmap.update({q : id})
    cregmap = {}
    for i in prog.instructions:
        if isinstance(i, Gate):
            try:
                optype = _known_quil_gate[i.name]
            except KeyError as error:
                raise NotImplementedError("Operation not supported by tket: " + str(i)) from error
            qubits = [qmap[q.index] for q in i.qubits]
            params = [p/pi for p in i.params]
            tkc.add_gate(optype, params, qubits, [])
        elif isinstance(i, Measurement):
            qubit = qmap[i.qubit.index]
            reg = cregmap[i.classical_reg.name]
            bit = reg[i.classical_reg.offset]
            tkc.Measure(qubit, bit)
        elif isinstance(i, Declare):
            if i.memory_type != 'BIT' :
                raise NotImplementedError("Cannot handle memory of type " + i.memory_type)
            new_reg = tkc.add_c_register(i.name, i.memory_size)
            cregmap.update({i.name : new_reg})
        elif isinstance(i, Pragma):
            continue
        elif isinstance(i, Halt):
            return tkc
        else:
            raise NotImplementedError("PyQuil instruction is not a gate: " + str(i))
    return tkc

def tk_to_pyquil(tkcirc: Circuit, active_reset:bool=False) -> Program:
    """
       Convert a :math:`\\mathrm{t|ket}\\rangle` :py:class:`Circuit` to a :py:class:`pyquil.Program` .

    :param tkcirc: A circuit to be converted

    :return: The converted circuit
    """
    p = Program()
    qregs = set()
    for qb in tkcirc.qubits :
        if len(qb.index) != 1 :
            raise NotImplementedError("PyQuil registers must use a single index")
        qregs.add(qb.reg_name)
    if len(qregs) > 1 :
        raise NotImplementedError("Cannot convert circuit with multiple quantum registers to pyQuil")
    creg_sizes = {}
    for b in tkcirc.bits :
        if len(b.index) != 1 :
            raise NotImplementedError("PyQuil registers must use a single index")
        if (b.reg_name not in creg_sizes) or (b.index[0] >= creg_sizes[b.reg_name]) :
            creg_sizes.update({b.reg_name : b.index[0] + 1})
    cregmap = {}
    for reg_name, size in creg_sizes.items() :
        name = reg_name
        if name == 'c' :
            name = 'ro'
        quil_reg = p.declare(name, 'BIT', size)
        cregmap.update({reg_name : quil_reg})
    if active_reset :
        p.reset()
    measures = []
    measured_qubits = []
    for command in tkcirc:
        op = command.op
        qubits = [Qubit(qb.index[0]) for qb in command.qubits]
        for qb in qubits :
            if qb in measured_qubits :
                raise NotImplementedError("Cannot apply gate on qubit " + qb.__repr__() + " after measurement")
        optype = op.get_type()
        if optype == OpType.Measure :
            bits = [cregmap[b.reg_name][b.index[0]] for b in command.bits]
            measures.append(Measurement(*qubits, *bits))
            measured_qubits.extend(qubits)
            continue
        try:
            gatetype = _known_quil_gate_rev[optype]
        except KeyError as error:
            raise NotImplementedError("Cannot convert tket Op to pyQuil gate: " + op.get_name()) from error
        if len(command.conditions) != 0 :
            raise NotImplementedError("Cannot convert conditional gates from tket to pyQuil")
        params = [float((p * pi).evalf()) for p in op.get_params()]
        g = Gate(gatetype, params, qubits)
        p += g
    for m in measures :
        p += m
    return p
