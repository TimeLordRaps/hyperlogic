"""Tests for the canonical structures, and for axiom independence.

Independence is the one result in this package that is conclusive rather than
checked: four structures, each satisfying exactly three axioms and failing the
fourth. One countermodel settles the independence of one axiom, so the result
does not depend on how many confirming models exist.
"""

from __future__ import annotations

from hyperlogic.models import (
    CLOSURE,
    ECHO,
    INDEPENDENCE_MODELS,
    MATTER,
    MODELS,
    READING,
    collapsed_model,
    minimal_model,
    separating_model,
    without_closure_self,
    without_triangle,
)
from hyperlogic.triangle import (
    AXIOM_NAMES,
    Status,
    ax_closure_self,
    ax_triangle,
    check_derives,
    circuit,
    failed_axioms,
    is_model,
)


def test_every_canonical_structure_is_a_model_of_the_axioms():
    """Including the collapsed one. That is what makes its derive failure a refutation."""
    for factory in MODELS:
        assert is_model(factory()), factory().name


def test_each_independence_structure_fails_exactly_its_own_axiom():
    for name, factory in INDEPENDENCE_MODELS:
        assert failed_axioms(factory()) == (name,), factory().name


def test_the_independence_structures_cover_every_axiom_once():
    assert tuple(name for name, _ in INDEPENDENCE_MODELS) == AXIOM_NAMES


def test_ax_closure_self_is_not_implied_by_the_universal_axioms():
    """The three-step circuit still closes for every sign when the closure does not.

    This is why ax-closure-self is not redundant: the other three axioms are
    universally quantified and say nothing that singles out the irreducible.
    """
    model = without_closure_self()
    assert ax_triangle(model).status is Status.HOLDS_IN_MODEL
    assert ax_closure_self(model).status is Status.FAILS_IN_MODEL


def test_ax_triangle_can_fail_while_the_closure_still_returns():
    model = without_triangle()
    assert ax_closure_self(model).status is Status.HOLDS_IN_MODEL
    assert ax_triangle(model).status is Status.FAILS_IN_MODEL
    assert ax_triangle(model).witness == (MATTER,)


def test_the_minimal_model_has_the_three_registers():
    model = minimal_model()
    assert model.signs == (CLOSURE, MATTER, READING)
    assert model.closure == CLOSURE


def test_the_collapsed_model_has_one_sign_and_fails_only_d_two_signs():
    collapsed = collapsed_model()
    assert collapsed.signs == (CLOSURE,)
    failed = tuple(
        v.claim for v in check_derives(collapsed) if v.status is Status.FAILS_IN_MODEL
    )
    assert failed == ("d-two-signs",)


def test_the_structures_are_immutable_and_hashable():
    """Frozen with slots, so a structure cannot drift between two checks of it."""
    model = minimal_model()
    assert hash(model) == hash(minimal_model())
    assert model == minimal_model()


def test_the_minimal_model_reads_shares_context_reflexively_where_declared():
    """Section V declares shares-context reflexive on signs reachable from the closure.

    A model may satisfy more than the axioms demand, and this one does: the
    reflexive derives pairs are not forced by any axiom.
    """
    model = minimal_model()
    for sign in model.signs:
        assert (sign, sign) in model.derives


def test_the_separating_structure_models_the_axioms():
    assert is_model(separating_model())


def test_the_separating_structure_has_a_sign_outside_the_circuit():
    """`echo` is unreachable from the closure, which is how the Section VI close
    of log-derives gets exercised on its stated restriction to reachable signs.
    """
    model = separating_model()
    assert ECHO in model.signs
    assert ECHO not in circuit(model, CLOSURE)
    assert circuit(model, CLOSURE) == (CLOSURE, MATTER, READING)


def test_every_derive_holds_in_the_separating_structure():
    for verdict in check_derives(separating_model()):
        assert verdict.status is Status.HOLDS_IN_MODEL, verdict.claim
