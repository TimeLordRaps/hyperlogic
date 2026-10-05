"""Tests for the PROPOSED status layer (outside L0). See `hyperlogic.status`."""

from __future__ import annotations

import types
from pathlib import Path

import pytest

import hyperlogic.status as st

SRC = Path(st.__file__).read_text(encoding="utf-8")


def _load_mutant(old: str, new: str) -> types.ModuleType:
    assert SRC.count(old) == 1, "mutation target must occur exactly once"
    mod = types.ModuleType("status_mutant")
    exec(compile(SRC.replace(old, new), "status_mutant", "exec"), mod.__dict__)
    return mod


def test_all_six_findings_run_and_print():
    lines = st.check()
    for tag in ("0. ", "1. ", "2. ", "3. ", "4. ", "5. "):
        assert any(ln.startswith(tag) for ln in lines), tag


def test_the_frame_has_one_theory_atom_and_two_observation_atoms():
    assert st.OBS == ("Test", "Null")
    assert set(st.ATOMS) - set(st.OBS) == {"Psi"}
    assert len(list(st.assignments())) == 8


def test_psi_alone_is_independent_and_unfalsifiable_and_so_is_its_negation():
    for pred in (st.Psi, lambda m: not m["Psi"]):
        s = st.status(st.T0, pred)
        assert s["independent"] and s["unfalsifiable"] and not s["falsifiable"]
        assert not s["provable"] and not s["refutable"]


def test_provable_refutable_independent_partition():
    cases = [
        (st.T0, lambda m: True),
        (st.T0, lambda m: False),
        (st.T0, st.Psi),
        (lambda m: m["Psi"], st.Psi),
    ]
    for t, p in cases:
        s = st.status(t, p)
        assert [s["provable"], s["refutable"], s["independent"]].count(True) == 1


def test_r1_is_falsifiable_and_a_null_has_likelihood_ratio_one():
    s = st.status(st.T0, st.READINGS["R1 tests always return null"])
    assert s["falsifiable"] and (True, False) not in s["observable_with_P"]
    lr = st.likelihood_ratio_of_null(1, 1)
    assert lr == 1
    assert st.posterior(st.Fraction(1, 10), lr) == st.Fraction(1, 10)


def test_r2_is_psi_and_no_test_is_ever_run():
    r2 = st.READINGS["R2 testing falsifies the postulate"]
    for m in st.assignments():
        assert r2(m) == (m["Psi"] and not m["Test"])


def test_r3_is_unfalsifiable_and_unprovable():
    s = st.status(st.T0, st.READINGS["R3 tests are uninterpretable"])
    assert s["unfalsifiable"] and s["independent"]


def test_independence_is_not_unfalsifiability():
    def bridge(m):
        return (not m["Psi"]) or (not m["Test"]) or m["Null"]

    s = st.status(bridge, st.Psi)
    assert s["independent"] and s["falsifiable"] and not s["unfalsifiable"]


def test_dropping_the_null_prediction_makes_r1_unfalsifiable_and_the_check_notices():
    mutant = _load_mutant(
        'lambda m: m["Psi"] and ((not m["Test"]) or m["Null"])', 'lambda m: m["Psi"]'
    )
    with pytest.raises(AssertionError):
        mutant.check()


def test_a_wrong_likelihood_ratio_is_noticed():
    mutant = _load_mutant(
        "lr = likelihood_ratio_of_null(1, 1)", "lr = likelihood_ratio_of_null(1, Fraction(1, 2))"
    )
    with pytest.raises(AssertionError):
        mutant.check()


def test_the_module_states_it_is_outside_l0():
    doc = (st.__doc__ or "").lower()
    assert "not part of the l0 triangle" in doc
    assert "propositional only" in doc


def test_l0_modules_do_not_import_the_proposed_layer():
    root = Path(st.__file__).parent
    for name in ("__init__.py", "triangle.py", "models.py", "relations.py", "report.py"):
        text = (root / name).read_text(encoding="utf-8")
        for layer in ("status", "provability"):
            assert f"from .{layer}" not in text and f"import {layer}" not in text, (name, layer)
