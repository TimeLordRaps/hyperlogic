"""Tests for the PROPOSED provability layer (outside L0). See `hyperlogic.provability`."""

from __future__ import annotations

import types
from pathlib import Path

import hyperlogic.provability as gl

SRC = Path(gl.__file__).read_text(encoding="utf-8")
p, q = gl.var("p"), gl.var("q")


def _load_mutant(old: str, new: str) -> types.ModuleType:
    assert SRC.count(old) == 1, "mutation target must occur exactly once"
    mod = types.ModuleType("provability_mutant")
    exec(compile(SRC.replace(old, new), "provability_mutant", "exec"), mod.__dict__)
    return mod


def test_gl_checks_run_and_match_the_literature():
    lines = gl.check()
    text = "\n".join(lines)
    assert "FairBot      vs FairBot     : C C" in text
    assert "agree on 300/300" in text


def test_known_cases_match_expected_values():
    for name, (f, expected) in gl.known_cases().items():
        assert gl.prove(f) == expected, name


def test_loeb_and_4_are_provable_and_reflection_is_not():
    assert gl.prove(gl.imp(gl.box(gl.imp(gl.box(p), p)), gl.box(p)))
    assert gl.prove(gl.imp(gl.box(p), gl.box(gl.box(p))))
    assert not gl.prove(gl.imp(gl.box(p), p))
    assert gl.countermodel(gl.imp(gl.box(p), p)) is not None


def test_every_unprovable_known_case_has_an_independent_countermodel():
    for name, (f, expected) in gl.known_cases().items():
        if not expected:
            assert gl.countermodel(f) is not None, name


def test_a_provable_formula_has_no_countermodel():
    assert gl.countermodel(gl.imp(gl.box(p), gl.box(gl.box(p)))) is None


def test_differential_agreement_is_total_on_the_default_sample():
    assert gl.differential() == 300
    assert gl.differential(samples=40, seed=1) == 40


def test_weakening_the_gl_rule_to_k_loses_loeb_and_4():
    mutant = _load_mutant("frozenset(boxed_left | unboxed | {f})", "frozenset(unboxed)")
    loeb = mutant.imp(mutant.box(mutant.imp(mutant.box(mutant.var("p")), mutant.var("p"))),
                      mutant.box(mutant.var("p")))
    four = mutant.imp(mutant.box(mutant.var("p")), mutant.box(mutant.box(mutant.var("p"))))
    # plain K: Loeb and 4 are both lost
    assert (mutant.prove(loeb), mutant.prove(four)) == (False, False)
    # and the unmutated procedure still has both
    assert gl.prove(gl.imp(gl.box(gl.imp(gl.box(p), p)), gl.box(p)))
    assert gl.prove(gl.imp(gl.box(p), gl.box(gl.box(p))))


def test_the_mutated_prover_disagrees_with_the_oracle_so_the_differential_notices():
    mutant = _load_mutant("frozenset(boxed_left | unboxed | {f})", "frozenset(unboxed)")
    try:
        mutant.differential()
    except AssertionError:
        return
    raise AssertionError("the differential check did not notice the weakened rule")


def test_letterless_truth_and_agents():
    assert gl.true_in_arithmetic(gl.CON) and not gl.true_in_arithmetic(gl.box(gl.BOT))
    assert gl.play(gl.FairBot, gl.DefectBot) == (False, False)
    assert gl.play(gl.FairBot, gl.FairBot) == (True, True)
    assert gl.play(gl.CooperateBot, gl.DefectBot) == (True, False)


def test_the_module_states_it_is_outside_l0_and_names_its_limits():
    doc = (gl.__doc__ or "").lower()
    assert "not part of the l0 triangle" in doc
    assert "propositional modal only" in doc
    assert "solovay" in doc
