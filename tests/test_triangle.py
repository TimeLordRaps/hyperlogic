"""Tests for the L0 axioms, derives and non-derives.

The tests that matter most here are the ones that check a claim FAILS. A layer
whose test suite only confirms is a layer whose limits are unrecorded.
"""

from __future__ import annotations

import pytest

from hyperlogic.models import (
    CLOSURE,
    MATTER,
    READING,
    collapsed_model,
    minimal_model,
)
from hyperlogic.triangle import (
    AXIOM_NAMES,
    AXIOMS,
    DERIVES,
    NotAModel,
    SignModel,
    Status,
    Verdict,
    advances_is_irreflexive,
    check_axioms,
    check_derives,
    circuit,
    d_two_signs,
    failed_axioms,
    is_model,
    refuted_by,
    two_turn_return,
    universal_one_turn_return,
)


def test_the_minimal_structure_models_every_axiom():
    assert is_model(minimal_model())
    assert failed_axioms(minimal_model()) == ()


def test_every_derive_holds_in_the_minimal_model():
    for verdict in check_derives(minimal_model()):
        assert verdict.status is Status.HOLDS_IN_MODEL, verdict.claim


def test_the_axiom_names_match_the_checkers_in_order():
    model = minimal_model()
    assert len(AXIOMS) == len(AXIOM_NAMES) == 4
    assert tuple(v.claim for v in check_axioms(model)) == AXIOM_NAMES


def test_turn_is_the_three_cycle():
    model = minimal_model()
    assert model.turn(CLOSURE) == MATTER
    assert model.turn(MATTER) == READING
    assert model.turn(READING) == CLOSURE
    for sign in model.signs:
        assert model.turn_n(sign, 3) == sign


def test_the_period_is_three_and_not_two():
    """The one structural place this layer differs from hypermath's ax-box."""
    model = minimal_model()
    for sign in model.signs:
        assert model.turn_n(sign, 2) != sign


def test_a_verdict_has_no_truth_value():
    verdict = Verdict("some-claim", Status.HOLDS_IN_MODEL)
    with pytest.raises(TypeError, match="no truth value"):
        bool(verdict)


def test_a_holding_verdict_may_not_name_a_witness():
    with pytest.raises(ValueError, match="no distinguished witness"):
        Verdict("some-claim", Status.HOLDS_IN_MODEL, (CLOSURE,))


def test_a_failing_verdict_must_name_a_witness():
    with pytest.raises(ValueError, match="must name its counterexample"):
        Verdict("some-claim", Status.FAILS_IN_MODEL)


def test_universal_one_turn_return_is_refuted():
    """ax-closure-self grants a one-turn return to the closure and to nothing else."""
    model = minimal_model()
    verdict = universal_one_turn_return(model)
    assert verdict.status is Status.FAILS_IN_MODEL
    assert verdict.witness == (MATTER,)
    assert "REFUTED" in refuted_by("every sign returns after one turn", verdict, model)


def test_the_two_step_return_is_refuted():
    model = minimal_model()
    verdict = two_turn_return(model)
    assert verdict.status is Status.FAILS_IN_MODEL
    assert "REFUTED" in refuted_by("two turns suffice for a circuit", verdict, model)


def test_d_two_signs_is_refuted_from_the_axioms_alone():
    """nd-two-signs-from-axioms-alone, executed.

    The collapsed structure satisfies all four axioms and has one sign. The
    derive is not thereby wrong: it uses the Section VI close, which this
    structure violates. What is refuted is the stronger reading in which
    plurality follows from Section III alone.
    """
    collapsed = collapsed_model()
    assert is_model(collapsed)
    verdict = d_two_signs(collapsed)
    assert verdict.status is Status.FAILS_IN_MODEL
    report = refuted_by(
        "the carrier has at least two members, from the axioms alone", verdict, collapsed
    )
    assert "REFUTED" in report
    assert "collapsed" in report


def test_a_non_model_refutes_nothing():
    """A failure inside a structure that is not a model says nothing about the theory."""
    broken = SignModel(
        "broken", (CLOSURE,), CLOSURE, ((CLOSURE, CLOSURE),),
        frozenset(), frozenset(), frozenset(),
    )
    assert not is_model(broken)
    verdict = d_two_signs(broken)
    assert verdict.status is Status.FAILS_IN_MODEL
    with pytest.raises(NotAModel, match="refutes nothing"):
        refuted_by("anything at all", verdict, broken)


def test_a_refutation_needs_a_failure_to_point_at():
    model = minimal_model()
    with pytest.raises(ValueError, match="requires a failure"):
        refuted_by("something", d_two_signs(model), model)


def test_advances_is_not_forced_to_be_irreflexive_at_construction():
    """Reading advances as non-identity is the Section VI close, not an L0 fact."""
    assert advances_is_irreflexive(minimal_model()).status is Status.HOLDS_IN_MODEL
    assert advances_is_irreflexive(collapsed_model()).status is Status.FAILS_IN_MODEL


def test_the_circuit_of_every_sign_is_the_whole_carrier():
    model = minimal_model()
    for sign in model.signs:
        assert set(circuit(model, sign)) == set(model.signs)
        assert len(circuit(model, sign)) == 3


def test_the_circuit_of_the_collapsed_closure_is_itself_alone():
    assert circuit(collapsed_model(), CLOSURE) == (CLOSURE,)


def test_turn_must_be_a_total_function():
    with pytest.raises(ValueError, match="total function"):
        SignModel(
            "partial", (CLOSURE, MATTER), CLOSURE, ((CLOSURE, MATTER),),
            frozenset(), frozenset(), frozenset(),
        )


def test_turn_must_land_inside_the_carrier():
    with pytest.raises(ValueError, match="land inside the carrier"):
        SignModel(
            "escaping", (CLOSURE,), CLOSURE, ((CLOSURE, "elsewhere"),),
            frozenset(), frozenset(), frozenset(),
        )


def test_the_closure_must_be_a_sign():
    with pytest.raises(ValueError, match="must be a sign"):
        SignModel(
            "no-closure", (MATTER,), CLOSURE, ((MATTER, MATTER),),
            frozenset(), frozenset(), frozenset(),
        )


def test_a_relation_may_not_mention_an_unknown_sign():
    with pytest.raises(ValueError, match="unknown sign"):
        SignModel(
            "stranger", (CLOSURE,), CLOSURE, ((CLOSURE, CLOSURE),),
            frozenset({(CLOSURE, "stranger")}), frozenset(), frozenset(),
        )


def test_turn_n_rejects_a_negative_count():
    with pytest.raises(ValueError, match="nonnegative"):
        minimal_model().turn_n(CLOSURE, -1)


def test_the_derive_list_is_the_five_of_section_four():
    assert len(DERIVES) == 5
    assert tuple(v.claim for v in check_derives(minimal_model())) == (
        "d-turn-advances", "d-turn-stays", "d-triple-turn-returns",
        "d-two-signs", "d-return-exists",
    )
