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

"""Methods for integration of cirq and :math:`\\mathrm{t|ket}\\rangle` devices
"""
from typing import List, Iterator

import cirq
from cirq import GridQubit
from cirq.google import XmonDevice

from pytket import UnitID, OpType
from pytket.device import Device, GateError, GateErrorContainer
from pytket.routing import Architecture

def _sort_row_col(qubits: Iterator[GridQubit]) -> List[GridQubit]:
    """Sort grid qubits first by row then by column"""

    return sorted(qubits, key=lambda x: (x.row, x.col))

def xmon_to_device(xmon: XmonDevice) -> Device:
    """Generates a :math:`\\mathrm{t|ket}\\rangle` :py:class:`Device` object for a Cirq :py:class:`XmonDevice` .
    
    :param xmon: The device to convert

    :return: The corresponding :math:`\\mathrm{t|ket}\\rangle` :py:class:`Device`
    """

    qb_map = {q : UnitID('q', q.row, q.col) for q in xmon.qubits}

    indexed_qubits = _sort_row_col(xmon.qubits)
    coupling_map = []
    for qb in indexed_qubits:
        neighbours = xmon.neighbors_of(qb)
        #filter only higher index neighbours to avoid double counting edges
        forward_neighbours = filter(lambda x: indexed_qubits.index(x)>indexed_qubits.index(qb), neighbours)
        for x in forward_neighbours:
            coupling_map.append((qb_map[qb], qb_map[x]))
    arc = Architecture(coupling_map)

    node_ers_dict = {}
    link_ers_dict = {}

    px_duration = xmon.duration_of(cirq.X(GridQubit(0,0))).total_nanos()
    cz_duration = xmon.duration_of(cirq.CZ(GridQubit(0,0), GridQubit(0,1))).total_nanos()
    for qb in xmon.qubits :
        error_cont = GateErrorContainer()
        error_cont.add_error((OpType.PhasedX, GateError(0., px_duration)))
        error_cont.add_error((OpType.Rz, GateError(0., 0.)))
        node_ers_dict[qb_map[qb]] = error_cont
    
    for a, b in coupling_map :
        error_cont = GateErrorContainer()
        error_cont.add_error((OpType.CZ, GateError(0., cz_duration)))
        link_ers_dict[(a,b)] = error_cont
        link_ers_dict[(b,a)] = error_cont
    
    return Device(node_ers_dict, link_ers_dict, arc)
