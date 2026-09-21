"""Tests that the executable report reports honestly.

These are not cosmetic. The report is the artifact most readers will run, and a
report that quietly upgraded an open obligation, called a checked claim proved,
or let the package's name imply a logic would misrepresent the whole layer.
"""

from __future__ import annotations

from hyperlogic.report import OPEN_OBLIGATIONS, build_report, main


def test_the_report_runs_clean():
    assert main() == 0


def test_the_report_never_claims_universal_validity_for_a_checked_claim():
    """Catch affirmative overclaims only.

    A bare keyword scan is wrong here: the report legitimately contains the word
    "theorem" inside "no proof-assistant theorem", which is a disclaimer. What
    must never appear is an assertion that something was proved or is valid.
    """
    text = "\n".join(build_report()).lower()
    overclaims = (
        "is proved", "is proven", "we prove", "proves that", "is a theorem",
        "is valid", "hereby established", "has been established",
        "establishes that", "demonstrates that this is true",
    )
    for overclaim in overclaims:
        assert overclaim not in text, overclaim
    assert "no proof-assistant theorem" in text


def test_the_report_states_the_confirm_refute_asymmetry():
    text = "\n".join(build_report()).lower()
    assert "confirms nothing universally" in text
    assert "single countermodel settles" in text


def test_every_open_obligation_appears_unresolved():
    text = "\n".join(build_report())
    for title, status, _ in OPEN_OBLIGATIONS:
        assert title in text
        assert status in ("OPEN", "NOT_ESTABLISHED", "NOT_ATTEMPTED")
    assert "OPEN OBLIGATIONS" in text


def test_the_report_never_claims_this_layer_is_a_logic():
    """The name invites the assumption. The report must refuse it in writing."""
    text = "\n".join(build_report())
    assert "That this layer is a logic" in text
    assert "no connective, no quantifier, no inference rule" in text


def test_the_report_states_gc2_as_the_bet_the_package_rests_on():
    text = "\n".join(build_report())
    assert "GC-2 independence from hypermath L0" in text
    assert "OPEN" in text
    assert "no argument for it is offered" in text


def test_the_report_states_the_one_of_five_count():
    """One graduation criterion discharged out of five. Never rounded up."""
    text = "\n".join(build_report())
    assert "One of five graduation criteria is discharged" in text


def test_the_report_states_the_gate():
    text = "\n".join(build_report())
    assert "NOTHING MOVES OUT OF HYPERMATH" in text
    assert "GC-4 is not" in text


def test_the_report_states_the_period_difference_from_hypermath():
    text = "\n".join(build_report())
    assert "hypermath's ax-box closes at two" in text
    assert "three edges" in text


def test_the_report_carries_all_three_conclusive_refutations():
    text = "\n".join(build_report())
    assert text.count("REFUTED:") == 3


def test_the_report_records_that_d_two_signs_needs_the_close():
    """A reader must not take the third refutation as contradicting the derive."""
    text = "\n".join(build_report())
    assert "not the axioms alone" in text
    assert "nd-two-signs-from-axioms-alone" in text
