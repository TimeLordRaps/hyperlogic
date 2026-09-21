"""Hyperlogic: a self-grounded triangle of shape, matter and reading.

The irreducible is `closure`, the sign whose shape, matter and reading coincide.
The sole operation is `turn`, which advances a sign one edge around the circuit
shape -> matter -> reading -> shape. Three turns are a circuit, and the
self-grounding axiom is that the circuit closes: a cycle needs no exterior.

This package implements `L0_triangle.hm` and nothing above it. It has no
dependencies outside the standard library, on purpose and by placement. It does
NOT import hypermath, and it cannot: hypermath needs a metalanguage in order to
state hypermath, so a grounded-hyperlogic would make the dependency run
hyperlogic -> hypermath -> hyperlogic. `nd-import-hypermath` sets that argument
out in full. Under the acyclic dependency constraint the family already follows,
either this is a foundation with its own ground or the material stays inside
hypermath. This package takes the first option, and GC-2 is the bet that it
works.

WHAT IS NOT HERE, STATED FIRST BECAUSE THE NAME INVITES THE ASSUMPTION. There is
no connective, no quantifier, no inference rule and no proof object in this
package. It is not a logic and no claim of one is made. One of five graduation
criteria is discharged: this layer closes its own three opaque predicates in the
same file that declares them. The other four are open, and `report.py` prints
them every run.

Nothing has yet moved out of hypermath. `nd-the-gate` holds that nothing will
until GC-4 is discharged, so hypermath Section VIII stays exactly where it is
and this package is written beside it rather than carved out of it.
"""

from __future__ import annotations

from .models import (
    CLOSURE,
    ECHO,
    INDEPENDENCE_MODELS,
    MATTER,
    MODELS,
    READING,
    collapsed_model,
    minimal_model,
    separating_model,
    without_advance,
    without_closure_self,
    without_stay,
    without_triangle,
)
from .relations import (
    CLOSE_NAMES,
    CLOSES,
    STRENGTH,
    Relation,
    check_closes,
    close_advances_as_not_interderivable,
    close_derives_as_shares_context,
    close_returns_as_circuit_in_context,
    closes_hold,
    holds,
    interderivable,
    same_conclusion,
    shares_context,
    strength_order_holds,
    stronger_than,
)
from .triangle import (
    AXIOM_NAMES,
    AXIOMS,
    DERIVES,
    NotAModel,
    SignModel,
    Status,
    Verdict,
    advances_is_irreflexive,
    ax_advance,
    ax_closure_self,
    ax_stay,
    ax_triangle,
    check_axioms,
    check_derives,
    circuit,
    d_return_exists,
    d_triple_turn_returns,
    d_turn_advances,
    d_turn_stays,
    d_two_signs,
    failed_axioms,
    is_model,
    refuted_by,
    two_turn_return,
    universal_one_turn_return,
)

__version__ = "0.1.0.dev0"

__all__ = [
    "AXIOMS", "AXIOM_NAMES", "CLOSES", "CLOSE_NAMES", "CLOSURE", "DERIVES",
    "ECHO",
    "INDEPENDENCE_MODELS", "MATTER", "MODELS", "NotAModel", "READING",
    "Relation", "STRENGTH", "SignModel", "Status", "Verdict",
    "advances_is_irreflexive", "ax_advance", "ax_closure_self", "ax_stay",
    "ax_triangle", "check_axioms", "check_closes", "check_derives", "circuit",
    "close_advances_as_not_interderivable", "close_derives_as_shares_context",
    "close_returns_as_circuit_in_context", "closes_hold", "collapsed_model",
    "d_return_exists", "d_triple_turn_returns", "d_turn_advances",
    "d_turn_stays", "d_two_signs", "failed_axioms", "holds", "interderivable",
    "is_model", "minimal_model", "refuted_by", "same_conclusion",
    "separating_model",
    "shares_context", "strength_order_holds", "stronger_than",
    "two_turn_return", "universal_one_turn_return", "without_advance",
    "without_closure_self", "without_stay", "without_triangle",
]
