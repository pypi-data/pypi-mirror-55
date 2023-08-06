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
"""Python Interface to CQC t|ket>
"""

from pytket.circuit import (Circuit, OpType, Pauli, CircBox, Unitary2qBox,
    ExpBox, PauliExpBox, UnitID)
from pytket.routing import route, Architecture
from pytket.transform import Transform
from pytket.device import Device
from pytket.predicates import (GateSetPredicate, NoClassicalControlPredicate,
                                NoFastFeedforwardPredicate, NoClassicalBitsPredicate, NoWireSwapsPredicate,
                                MaxTwoQubitGatesPredicate, ConnectivityPredicate, DirectednessPredicate,
                                CliffordCircuitPredicate,
                                UserDefinedPredicate, CompilationUnit)
from pytket.passes import (SequencePass, RepeatPass, RepeatWithMetricPass, RepeatUntilSatisfiedPass,
                                SynthesiseIBM, SynthesiseHQS, SynthesiseOQC, SynthesiseUMD,
                                RebaseCirq, RebaseTket, RebaseIBM, RebaseQuil, RebasePyZX, RebaseProjectQ,
                                RebaseHQS, RebaseUMD, PauliSimp, DecomposeSingleQubitsIBM, DecomposeBoxes,
                                OptimisePhaseGadgets, RemoveRedundancies, CliffordSimp,
                                CommuteThroughMultis, OptimiseCliffordsZX, DecomposeArbitrarilyControlledGates,
                                DecomposeMultiQubitsIBM, USquashIBM,
                                gen_rebase_pass, gen_routing_pass, gen_directed_cx_routing_pass,
                                gen_decompose_routing_gates_to_cxs_pass, gen_user_defined_swap_decomp_pass)
from pytket.qasm import circuit_from_qasm, circuit_to_qasm
from pytket.quipper import circuit_from_quipper
__path__ = __import__('pkgutil').extend_path(__path__, __name__)
