"""Section V relations and the Section VI closes.

Section V declares three relations in strictly increasing strength, and Section
VI closes each of the three opaque predicates into them. This module makes both
halves checkable against a finite structure rather than leaving them as prose.

The relations are read off a `SignModel` exactly as Section V says they are
closed from:

- `shares_context` from `log-derives`, symmetrised. The weakest, widest relation.
- `same_conclusion` from `log-derives` with the route discarded: two signs land
  on the same claim when one turn takes them to the same place, however they got
  there.
- `interderivable` from full `log-returns` coincidence in both directions. The
  strongest, and earned rather than presupposed.

KNOWN SOFT SPOT, carried as GC-5 in `L0_triangle.hm` and not resolved here: each
relation is declared from an opaque predicate and each opaque predicate is then
closed as that relation. Read as a reduction this is circular. It is intended as
a fixed point. hypermath Sections V and VI use the same construction and do not
settle it either.
"""

from __future__ import annotations

from enum import Enum

from .triangle import SignModel, Status, Verdict, circuit


class Relation(str, Enum):
    """The three Section V relations, weakest first."""

    SHARES_CONTEXT = "shares-context"
    SAME_CONCLUSION = "same-conclusion"
    INTERDERIVABLE = "interderivable"


#: Declared strength. Higher is stronger, narrower, and harder to earn.
STRENGTH: dict[Relation, int] = {
    Relation.SHARES_CONTEXT: 0,
    Relation.SAME_CONCLUSION: 1,
    Relation.INTERDERIVABLE: 2,
}


def stronger_than(left: Relation, right: Relation) -> bool:
    """Whether `left` is the stronger of two relations."""
    if type(left) is not Relation or type(right) is not Relation:
        raise TypeError("both arguments must be Relation members")
    return STRENGTH[left] > STRENGTH[right]


def _known(model: SignModel, *signs: str) -> None:
    for sign in signs:
        if sign not in model.signs:
            raise KeyError(f"{sign!r} is not a sign of this model")


def shares_context(model: SignModel, left: str, right: str) -> bool:
    """The founding relation: the two signs stand in some one derivation context."""
    _known(model, left, right)
    return (left, right) in model.derives or (right, left) in model.derives


def same_conclusion(model: SignModel, left: str, right: str) -> bool:
    """The middle relation: one turn takes both signs to the same place.

    The route is discarded and only the landing counts, which is the
    proof-theoretic reading of two different derivations of one conclusion.
    """
    _known(model, left, right)
    return model.turn(left) == model.turn(right)


def interderivable(model: SignModel, left: str, right: str) -> bool:
    """The strongest relation: each sign returns to the other, both ways."""
    _known(model, left, right)
    return (left, right) in model.returns and (right, left) in model.returns


def holds(model: SignModel, relation: Relation, left: str, right: str) -> bool:
    """Evaluate any of the three relations by name."""
    if type(relation) is not Relation:
        raise TypeError("relation must be a Relation member")
    if relation is Relation.SHARES_CONTEXT:
        return shares_context(model, left, right)
    if relation is Relation.SAME_CONCLUSION:
        return same_conclusion(model, left, right)
    return interderivable(model, left, right)


def _pairs(model: SignModel) -> tuple[tuple[str, str], ...]:
    return tuple((left, right) for left in model.signs for right in model.signs)


# ---------------------------------------------------------------------------
# Section VI closes, each stated as a claim about a finite structure.
# ---------------------------------------------------------------------------


def close_advances_as_not_interderivable(model: SignModel) -> Verdict:
    """`log-advances` closes at the STRONGEST relation, not the weakest.

    The checkable content is disjointness: no pair may both advance and be
    interderivable. A structure where they overlap has derivations that never
    get anywhere, and `collapsed_model` is exactly that structure.
    """
    for left, right in _pairs(model):
        if (left, right) in model.advances and interderivable(model, left, right):
            return Verdict(
                "close-advances-as-not-interderivable", Status.FAILS_IN_MODEL, (left, right),
                "this pair both advances and is interderivable",
            )
    return Verdict("close-advances-as-not-interderivable", Status.HOLDS_IN_MODEL)


def close_derives_as_shares_context(model: SignModel) -> Verdict:
    """`log-derives` closes at the founding relation.

    Section V declares `shares-context` reflexive on signs reachable from the
    closure. Symmetry is free by construction; reflexivity is not, and it is what
    this checks.
    """
    reachable = circuit(model, model.closure)
    for sign in reachable:
        if not shares_context(model, sign, sign):
            return Verdict(
                "close-derives-as-shares-context", Status.FAILS_IN_MODEL, (sign,),
                "this reachable sign does not share a context with itself",
            )
    return Verdict("close-derives-as-shares-context", Status.HOLDS_IN_MODEL)


def close_returns_as_circuit_in_context(model: SignModel) -> Verdict:
    """`log-returns` closes so that a full circuit lands back in the same context."""
    for sign in model.signs:
        if not shares_context(model, model.turn_n(sign, 3), sign):
            return Verdict(
                "close-returns-as-circuit-in-context", Status.FAILS_IN_MODEL, (sign,),
                "the three-step circuit of this sign leaves its context",
            )
    return Verdict("close-returns-as-circuit-in-context", Status.HOLDS_IN_MODEL)


CLOSES = (
    close_derives_as_shares_context,
    close_advances_as_not_interderivable,
    close_returns_as_circuit_in_context,
)

CLOSE_NAMES = (
    "close-derives-as-shares-context",
    "close-advances-as-not-interderivable",
    "close-returns-as-circuit-in-context",
)


def check_closes(model: SignModel) -> tuple[Verdict, ...]:
    """Check all three Section VI closes in declaration order."""
    return tuple(close(model) for close in CLOSES)


def closes_hold(model: SignModel) -> bool:
    """Whether the structure satisfies every Section VI close.

    A structure may model the axioms and still fail a close, because the closes
    say more than the axioms do. That gap is not an accident; `d-two-signs`
    lives in it.
    """
    return all(v.status is Status.HOLDS_IN_MODEL for v in check_closes(model))


def strength_order_holds(model: SignModel) -> Verdict:
    """Each relation implies the weaker one below it, as Section V declares.

    Declared properties are checked rather than asserted: `interderivable`
    implies `same-conclusion`, and `same-conclusion` implies `shares-context`.
    """
    for left, right in _pairs(model):
        if interderivable(model, left, right) and not same_conclusion(model, left, right):
            return Verdict(
                "strength-order", Status.FAILS_IN_MODEL, (left, right),
                "interderivable without the same conclusion",
            )
        if same_conclusion(model, left, right) and not shares_context(model, left, right):
            return Verdict(
                "strength-order", Status.FAILS_IN_MODEL, (left, right),
                "same conclusion without a shared context",
            )
    return Verdict("strength-order", Status.HOLDS_IN_MODEL)
