"""Tests for the Section V relations and the Section VI closes.

GC-1 is the one graduation criterion this layer discharges, and it is a claim
about these three closes: they are in the same file that declares the opaque
predicates, and they are checkable. These tests are what "checkable" means.
"""

from __future__ import annotations

import pytest

from hyperlogic.models import (
    CLOSURE,
    ECHO,
    MATTER,
    READING,
    collapsed_model,
    minimal_model,
    separating_model,
)
from hyperlogic.relations import (
    CLOSE_NAMES,
    CLOSES,
    Relation,
    check_closes,
    close_advances_as_not_interderivable,
    closes_hold,
    holds,
    interderivable,
    same_conclusion,
    shares_context,
    strength_order_holds,
    stronger_than,
)
from hyperlogic.triangle import Status, is_model


def test_all_three_closes_hold_in_the_minimal_model():
    assert closes_hold(minimal_model())


def test_the_close_names_match_the_checkers_in_order():
    assert len(CLOSES) == len(CLOSE_NAMES) == 3
    assert tuple(v.claim for v in check_closes(minimal_model())) == CLOSE_NAMES


def test_the_gap_between_the_weakest_and_strongest_relation():
    """Where every nontrivial derivation lives.

    turn(closure) shares a context with the closure and is not interderivable
    with it. A field in which the two coincided would have derivations that
    never got anywhere.
    """
    model = minimal_model()
    turned = model.turn(CLOSURE)
    assert shares_context(model, turned, CLOSURE)
    assert not interderivable(model, turned, CLOSURE)
    assert (turned, CLOSURE) in model.advances


def test_the_relations_are_declared_weakest_first():
    assert stronger_than(Relation.INTERDERIVABLE, Relation.SAME_CONCLUSION)
    assert stronger_than(Relation.SAME_CONCLUSION, Relation.SHARES_CONTEXT)
    assert not stronger_than(Relation.SHARES_CONTEXT, Relation.INTERDERIVABLE)


def test_the_strength_order_is_checked_and_not_merely_declared():
    assert strength_order_holds(minimal_model()).status is Status.HOLDS_IN_MODEL
    assert strength_order_holds(collapsed_model()).status is Status.HOLDS_IN_MODEL


def test_same_conclusion_discards_the_route():
    """Two signs land on the same claim when one turn takes them to the same place."""
    model = minimal_model()
    for sign in model.signs:
        assert same_conclusion(model, sign, sign)
    assert not same_conclusion(model, CLOSURE, MATTER)
    assert not same_conclusion(model, MATTER, READING)


def test_shares_context_is_symmetric_by_construction():
    model = minimal_model()
    for left in model.signs:
        for right in model.signs:
            assert shares_context(model, left, right) == shares_context(model, right, left)


def test_shares_context_is_reflexive_on_reachable_signs():
    model = minimal_model()
    for sign in model.signs:
        assert shares_context(model, sign, sign)


def test_shares_context_is_not_transitive_in_general():
    """Section V declares it weakest and widest, and explicitly not transitive.

    matter shares a context with the closure and the closure with reading, while
    matter and reading share none.
    """
    model = minimal_model()
    assert shares_context(model, MATTER, CLOSURE)
    assert shares_context(model, CLOSURE, READING)
    assert not shares_context(model, MATTER, READING)


def test_the_collapsed_model_satisfies_the_axioms_and_violates_a_close():
    """The gap where d-two-signs lives, made executable.

    The closes say more than the axioms do. A structure can model every axiom
    and still fail a close, and this is the one that does.
    """
    collapsed = collapsed_model()
    assert is_model(collapsed)
    assert not closes_hold(collapsed)
    failed = tuple(
        v.claim for v in check_closes(collapsed) if v.status is Status.FAILS_IN_MODEL
    )
    assert failed == ("close-advances-as-not-interderivable",)


def test_the_violated_close_names_its_witness():
    verdict = close_advances_as_not_interderivable(collapsed_model())
    assert verdict.status is Status.FAILS_IN_MODEL
    assert verdict.witness == (CLOSURE, CLOSURE)


def test_holds_dispatches_to_each_relation():
    model = minimal_model()
    assert holds(model, Relation.SHARES_CONTEXT, MATTER, CLOSURE)
    assert holds(model, Relation.SAME_CONCLUSION, READING, READING)
    assert not holds(model, Relation.INTERDERIVABLE, MATTER, CLOSURE)


def test_holds_rejects_a_string_in_place_of_a_relation():
    """Relation subclasses str, so a bare string must not slip through as one."""
    with pytest.raises(TypeError, match="must be a Relation member"):
        holds(minimal_model(), "shares-context", MATTER, CLOSURE)


def test_stronger_than_rejects_a_string_in_place_of_a_relation():
    with pytest.raises(TypeError, match="must be Relation"):
        stronger_than("interderivable", Relation.SHARES_CONTEXT)


def test_an_unknown_sign_is_rejected_rather_than_reported_false():
    model = minimal_model()
    with pytest.raises(KeyError):
        shares_context(model, "elsewhere", CLOSURE)
    with pytest.raises(KeyError):
        interderivable(model, CLOSURE, "elsewhere")


def test_same_conclusion_does_not_imply_interderivable():
    """Section V declares the implication strict. This is the witness.

    The minimal circuit cannot witness it: there the two relations have the same
    extension, so a declared strictness would go unchecked. `matter` and `echo`
    land on the same conclusion by different routes and are not interderivable.
    """
    model = separating_model()
    assert is_model(model)
    assert same_conclusion(model, MATTER, ECHO)
    assert not interderivable(model, MATTER, ECHO)


def test_the_minimal_circuit_cannot_witness_that_strictness():
    """Recorded so the limitation is visible rather than implicit."""
    model = minimal_model()
    for left in model.signs:
        for right in model.signs:
            assert same_conclusion(model, left, right) == interderivable(model, left, right)


def test_all_three_closes_hold_in_the_separating_structure():
    assert closes_hold(separating_model())


def test_the_strength_order_holds_in_the_separating_structure():
    assert strength_order_holds(separating_model()).status is Status.HOLDS_IN_MODEL
