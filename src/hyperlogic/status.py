"""PROPOSED, OUTSIDE L0: provable / refutable / independent, falsifiable / unfalsifiable.

THIS MODULE IS NOT PART OF THE L0 TRIANGLE AND IS NOT COVERED BY ITS CLAIMS. The
L0 layer (`L0_triangle.hm`, `triangle.py`, `models.py`, `relations.py`) has no
connective, no quantifier, no inference rule and no proof object, and that
statement stays exactly true of those files. This module DOES have connectives
(it evaluates propositional predicates) and an entailment relation (`entails`,
by enumeration). It is a separately proposed layer, written beside L0, imported
by nothing in L0, and it discharges none of GC-1 .. GC-5.

WHAT IS COMPUTED. A finite propositional frame. Atoms split into OBSERVATION
atoms (what a test can read: `Test`, `Null`) and one THEORY atom (`Psi`, which a
test cannot read). A model is a truth assignment to all three atoms. For a
background theory T (a predicate on assignments) and a postulate P:

    provable       T entails P
    refutable      T entails not P
    independent    neither: unprovable and unrefutable
    falsifiable    observable(T and P) is a proper subset of observable(T):
                   P forbids an observation T allows
    unfalsifiable  observable(T and P) == observable(T): P is observationally
                   conservative over T

Independence is not unfalsifiability, and `check()` exhibits a postulate that is
independent and falsifiable.

THREE READINGS of the owner's remark "trying to prove it disproves it always"
(USER-STATED, 2026-10-05; recorded verbatim in DESIGN.md) are computed
separately: R1 tests always return null, R2 testing falsifies the postulate
(equivalent to `Psi and no test is ever run`), R3 tests are uninterpretable.

LIMITS, stated here because the name invites more. Propositional only: no
first-order structure. Exactly one theory atom and two observation atoms. No
probability enters except one exact-rational likelihood ratio for a null result
under R1. Godel-level independence (undecidability in an arithmetic theory) is
NOT modelled; "independent" here means only that both the postulate and its
negation have models of T in a three-atom frame. Everything is checked by
exhaustive enumeration of eight assignments, so each result holds for this frame
and says nothing beyond it.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from fractions import Fraction
from itertools import product
from typing import Any

ATOMS = ("Test", "Null", "Psi")
OBS = ("Test", "Null")

Assignment = dict[str, bool]
Predicate = Callable[[Assignment], bool]


def assignments() -> Iterator[Assignment]:
    for vals in product([False, True], repeat=len(ATOMS)):
        yield dict(zip(ATOMS, vals))


def models(pred: Predicate) -> list[Assignment]:
    return [m for m in assignments() if pred(m)]


def observable(pred: Predicate) -> set[tuple[bool, ...]]:
    """Observation patterns realisable by models of `pred` (projection onto OBS)."""
    return {tuple(m[a] for a in OBS) for m in models(pred)}


def entails(t: Predicate, p: Predicate) -> bool:
    return all(p(m) for m in models(t))


def status(t: Predicate, p: Predicate) -> dict[str, Any]:
    prov = entails(t, p)
    ref = entails(t, lambda m: not p(m))
    # A consistent theory cannot both prove and refute.
    assert not (prov and ref) or not models(t)

    def both(m: Assignment) -> bool:
        return t(m) and p(m)

    obs_t, obs_tp = observable(t), observable(both)
    return {
        "provable": prov,
        "refutable": ref,
        "independent": not prov and not ref,
        "falsifiable": obs_tp < obs_t,
        "unfalsifiable": obs_tp == obs_t,
        "observable_with_P": sorted(obs_tp),
    }


def T0(m: Assignment) -> bool:
    """Background theory with no link between tests and the postulate."""
    return True


def Psi(m: Assignment) -> bool:
    return m["Psi"]


READINGS: dict[str, Predicate] = {
    "R1 tests always return null": lambda m: m["Psi"] and ((not m["Test"]) or m["Null"]),
    "R2 testing falsifies the postulate": lambda m: m["Psi"]
    and ((not m["Test"]) or (not m["Psi"])),
    "R3 tests are uninterpretable": lambda m: m["Psi"],
}


def likelihood_ratio_of_null(p_null_given_h: Any, p_null_given_not_h: Any) -> Fraction:
    return Fraction(p_null_given_h) / Fraction(p_null_given_not_h)


def posterior(prior: Any, lr: Fraction) -> Fraction:
    odds = Fraction(prior) / (1 - Fraction(prior)) * lr
    return odds / (1 + odds)


def check() -> list[str]:
    """Run the six findings. Raises AssertionError if any fails; returns the lines."""
    out: list[str] = []

    base = status(T0, Psi)
    assert base["independent"] and base["unfalsifiable"] and not base["falsifiable"]
    out.append("0. Psi alone: unprovable and unrefutable (independent) and unfalsifiable: "
               "no observation pattern is excluded")

    neg = status(T0, lambda m: not m["Psi"])
    assert neg["independent"] and neg["unfalsifiable"]
    out.append("1. not Psi has the same status, so no observation distinguishes Psi from "
               "not Psi on T0 (observational underdetermination)")

    r1 = status(T0, READINGS["R1 tests always return null"])
    assert r1["falsifiable"] and (True, False) not in r1["observable_with_P"]
    out.append("2. R1 (tests always return null) is falsifiable: one Test with a non-null "
               "result refutes it")
    lr = likelihood_ratio_of_null(1, 1)
    assert lr == 1 and posterior(Fraction(1, 10), lr) == Fraction(1, 10)
    out.append("   and a null result, predicted by Psi and by not-Psi alike, has likelihood "
               "ratio 1: posterior = prior (no disproof, no support)")

    r2 = status(T0, READINGS["R2 testing falsifies the postulate"])
    assert r2["falsifiable"] and all(not test for (test, _null) in r2["observable_with_P"])
    assert not entails(T0, lambda m: not m["Test"])
    out.append("3. R2 (testing falsifies it) is equivalent to 'Psi and no test is ever run': "
               "it survives only untested, so any run test refutes it by definition")

    r3 = status(T0, READINGS["R3 tests are uninterpretable"])
    assert r3["unfalsifiable"] and r3["independent"]
    out.append("4. R3 (tests uninterpretable) adds no observational constraint: unfalsifiable "
               "and unprovable; evidence cannot touch it")

    # Independence is not unfalsifiability: a bridge law links Psi to a prediction.
    def t1(m: Assignment) -> bool:  # Psi and Test imply Null
        return (not m["Psi"]) or (not m["Test"]) or m["Null"]

    s1 = status(t1, Psi)
    assert s1["independent"] and s1["falsifiable"] and not s1["unfalsifiable"]
    s2 = status(t1, lambda m: m["Psi"] and m["Test"] and not m["Null"])
    assert s2["refutable"]
    out.append("5. independence is not unfalsifiability: with a bridge law (Psi and Test "
               "imply Null) Psi is independent of T1 yet falsifiable (it forbids Test with a "
               "non-null result); its 'positive-result' strengthening is refuted outright")
    return out


def main() -> int:
    print("\n".join(check()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
