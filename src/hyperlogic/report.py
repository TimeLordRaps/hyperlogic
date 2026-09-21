"""The executable L0 status report.

The report states what was checked, what was refuted, and what remains open. It
never reports an open obligation as satisfied, and it never upgrades
HOLDS_IN_MODEL into validity. A reader who only runs this and reads nothing else
should still come away with an accurate picture of what is and is not
established — including the fact that four of this layer's five graduation
criteria are not discharged, and that the layer is not a logic.
"""

from __future__ import annotations

from .models import (
    ECHO,
    INDEPENDENCE_MODELS,
    MATTER,
    MODELS,
    collapsed_model,
    minimal_model,
    separating_model,
)
from .relations import (
    CLOSE_NAMES,
    Relation,
    check_closes,
    closes_hold,
    holds,
    interderivable,
    same_conclusion,
    strength_order_holds,
)
from .triangle import (
    AXIOM_NAMES,
    Status,
    advances_is_irreflexive,
    check_axioms,
    check_derives,
    d_two_signs,
    failed_axioms,
    is_model,
    refuted_by,
    two_turn_return,
    universal_one_turn_return,
)

THE_GATE = (
    "NOTHING MOVES OUT OF HYPERMATH UNTIL GC-1 AND GC-4 ARE BOTH DISCHARGED. "
    "GC-1 is discharged and GC-4 is not, so hypermath Section VIII stays "
    "exactly where it is and this package is written beside it."
)

OPEN_OBLIGATIONS = (
    (
        "GC-2 independence from hypermath L0",
        "OPEN",
        "That Sign and Claim are not Form and Prop respelled. This is the bet "
        "the repository rests on and no argument for it is offered anywhere. If "
        "the triangle needs a Form-like carrier to be stated at all, this is "
        "hypermath Section VIII with new spelling and should be archived as "
        "that result.",
    ),
    (
        "GC-3 three registers rather than four",
        "NOT_ESTABLISHED",
        "Declared in Section I and used by ax-triangle. A fourth register would "
        "change the period without disturbing anything else here, which is "
        "itself a sign the number does no derivational work yet.",
    ),
    (
        "GC-4 closing hypermath's seven executive opaques",
        "NOT_ATTEMPTED",
        "Syntax, substance, semantics, derives, discharge, definition, "
        "form-closure. This is the eventual purpose of the field and it is "
        "deliberately not claimed at L0.",
    ),
    (
        "GC-5 the declare-from / close-as fixed point",
        "OPEN",
        "Sections V and VI declare each relation from an opaque predicate and "
        "close that predicate as the relation. Inherited as a shared open "
        "problem with hypermath, which uses the same construction.",
    ),
    (
        "That this layer is a logic",
        "NOT_ESTABLISHED",
        "There is no connective, no quantifier, no inference rule and no proof "
        "object in this package. What is established is a cycle of three "
        "registers with a distinguished fixed point.",
    ),
)


def _line(label: str, value: object) -> str:
    return f"  {label:<44} {value}"


def _axioms_section() -> list[str]:
    out: list[str] = []
    out.append("AXIOMS AND DERIVES, checked against each model of the axioms")
    out.append("-" * 72)
    for factory in MODELS:
        model = factory()
        out.append(f"model {model.name!r} ({len(model.signs)} signs)")
        for verdict in check_axioms(model):
            out.append(_line(verdict.claim, verdict.status.value))
        for verdict in check_derives(model):
            out.append(_line(verdict.claim, verdict.status.value))
        out.append(_line("(reading) advances-is-irreflexive",
                         advances_is_irreflexive(model).status.value))
        out.append("")
    return out


def _independence_section() -> list[str]:
    out: list[str] = []
    out.append("AXIOM INDEPENDENCE -- each countermodel fails exactly one axiom")
    out.append("-" * 72)
    for name, factory in INDEPENDENCE_MODELS:
        model = factory()
        failed = failed_axioms(model)
        ok = failed == (name,)
        out.append(_line(
            model.name,
            f"fails {', '.join(failed) or '(nothing)'}"
            + ("" if ok else "  <-- UNEXPECTED: should fail exactly " + name),
        ))
    out.append("")
    out.append("  Each of the four axioms fails in a structure where the other three")
    out.append("  hold. No L0 axiom is a consequence of the others.")
    out.append("")
    return out


def _refutations_section() -> list[str]:
    out: list[str] = []
    out.append("CONCLUSIVE REFUTATIONS -- one countermodel settles a universal claim")
    out.append("-" * 72)
    minimal = minimal_model()
    out.append("  " + refuted_by(
        "every sign returns after one turn",
        universal_one_turn_return(minimal), minimal,
    ))
    out.append("  " + refuted_by(
        "two turns suffice for a circuit",
        two_turn_return(minimal), minimal,
    ))
    collapsed = collapsed_model()
    out.append("  " + refuted_by(
        "the carrier has at least two members, from the axioms alone",
        d_two_signs(collapsed), collapsed,
    ))
    out.append("")
    out.append("  The second is the period. hypermath's ax-box closes an orbit at two")
    out.append("  steps; this layer closes at three, and a structure satisfying all")
    out.append("  four axioms here fails the two-step return. That failure is the")
    out.append("  executable content of the claim that the triangle has three edges.")
    out.append("")
    out.append("  The third is load-bearing in a different way. d-two-signs is a FORM")
    out.append("  derive of Section IV, and the refutation above does not contradict it.")
    out.append("  The derive rests on the Section VI close of log-advances and")
    out.append("  not the axioms alone; the countermodel satisfies every axiom and")
    out.append("  violates that close. nd-two-signs-from-axioms-alone records this.")
    out.append("")
    return out


def _relations_section() -> list[str]:
    out: list[str] = []
    out.append("SECTION V RELATIONS in the minimal model, weakest first")
    out.append("-" * 72)
    minimal = minimal_model()
    for relation in Relation:
        pairs = [
            f"({left},{right})"
            for left in minimal.signs
            for right in minimal.signs
            if holds(minimal, relation, left, right)
        ]
        out.append(_line(relation.value, ", ".join(pairs) or "(empty)"))
    out.append(_line("strength order holds", strength_order_holds(minimal).status.value))
    out.append("")
    out.append("  The relations narrow as they strengthen, as Section V declares. The")
    out.append("  gap between shares-context and interderivable is where every")
    out.append("  nontrivial derivation lives: turn(closure) shares a context with the")
    out.append("  closure and is not interderivable with it.")
    out.append("")
    out.append("  In THIS structure same-conclusion and interderivable have the same")
    out.append("  extension, so the minimal circuit does not witness the strictness")
    out.append("  Section V declares between them. The separating structure does:")
    separating = separating_model()
    out.append(_line(
        "  matter / echo",
        f"same-conclusion {same_conclusion(separating, MATTER, ECHO)}, "
        f"interderivable {interderivable(separating, MATTER, ECHO)}",
    ))
    out.append(_line("  strength order holds", strength_order_holds(separating).status.value))
    out.append("")

    out.append("SECTION VI CLOSES -- GC-1, the criterion that decides the field")
    out.append("-" * 72)
    for factory in MODELS:
        model = factory()
        out.append(f"model {model.name!r}")
        for verdict in check_closes(model):
            out.append(_line(verdict.claim, verdict.status.value))
        out.append("")
    out.append("  All three opaque predicates of Section II are closed in Section VI of")
    out.append("  the same file. That is the bar hypermath L0 meets and hyperethics L0")
    out.append("  does not, and it is the one graduation criterion discharged here.")
    out.append("")
    out.append("  The collapsed structure is a model of the axioms that violates a")
    out.append("  close. The closes say more than the axioms do, and that gap is where")
    out.append("  d-two-signs lives.")
    out.append("")
    return out


def build_report() -> list[str]:
    """Produce the report as lines, so tests can assert on it without capture."""
    out: list[str] = []
    out.append("hyperlogic L0 triangle -- shape, matter, reading")
    out.append("=" * 72)
    out.append("")
    out.append("IRREDUCIBLE      closure: the sign whose shape, matter and reading coincide")
    out.append("SOLE OPERATION   turn: advance one edge around the triangle")
    out.append("PERIOD           three. hypermath's ax-box closes at two.")
    out.append("")
    out.extend(_axioms_section())
    out.extend(_independence_section())
    out.extend(_refutations_section())
    out.extend(_relations_section())

    out.append("THE GATE")
    out.append("-" * 72)
    for chunk in THE_GATE.split(". "):
        out.append(f"  {chunk.strip().rstrip('.')}.")
    out.append("")

    out.append("OPEN OBLIGATIONS -- not discharged by anything above")
    out.append("-" * 72)
    for title, status, note in OPEN_OBLIGATIONS:
        out.append(_line(title, status))
        out.append(f"      {note}")
    out.append("")
    out.append("  One of five graduation criteria is discharged. Four are not, and GC-2")
    out.append("  is the one on which the existence of this package depends.")
    out.append("")

    out.append("WHAT THIS REPORT DOES NOT ESTABLISH")
    out.append("-" * 72)
    out.append("  Model checking confirms nothing universally. A claim shown here as")
    out.append("  HOLDS_IN_MODEL was checked against finite structures and is not")
    out.append("  thereby valid. Only the refutations above are conclusive, because a")
    out.append("  single countermodel settles a universal claim and no number of")
    out.append("  confirming models settles one. No proof-assistant theorem, no")
    out.append("  adequacy proof, and no independence result against hypermath exists")
    out.append("  for this layer.")
    return out


def main() -> int:
    """Print the report. Returns nonzero if a structural expectation broke."""
    lines = build_report()
    print("\n".join(lines))
    if any("UNEXPECTED" in line for line in lines):
        return 1

    minimal = minimal_model()
    separating = separating_model()
    collapsed = collapsed_model()
    for model in (minimal, separating, collapsed):
        if not is_model(model):
            print(f"\nUNEXPECTED: {model.name!r} is not a model of the axioms")
            return 1
    for model in (minimal, separating):
        if any(v.status is not Status.HOLDS_IN_MODEL for v in check_derives(model)):
            print(f"\nUNEXPECTED: a derive failed in {model.name!r}")
            return 1
        if not closes_hold(model):
            print(f"\nUNEXPECTED: a close failed in {model.name!r}")
            return 1
        if strength_order_holds(model).status is not Status.HOLDS_IN_MODEL:
            print(f"\nUNEXPECTED: the strength order failed in {model.name!r}")
            return 1
    if not same_conclusion(separating, MATTER, ECHO) or interderivable(
        separating, MATTER, ECHO
    ):
        print("\nUNEXPECTED: the separating structure no longer separates")
        return 1

    # The collapsed structure must fail exactly d-two-signs and exactly the
    # advances close. If it ever failed more or fewer, the refutation above
    # would be pointing at something other than what the text says it is.
    failed_derives = tuple(
        v.claim for v in check_derives(collapsed) if v.status is Status.FAILS_IN_MODEL
    )
    if failed_derives != ("d-two-signs",):
        print(f"\nUNEXPECTED: collapsed model fails {failed_derives}")
        return 1
    failed_closes = tuple(
        v.claim for v in check_closes(collapsed) if v.status is Status.FAILS_IN_MODEL
    )
    if failed_closes != ("close-advances-as-not-interderivable",):
        print(f"\nUNEXPECTED: collapsed model fails closes {failed_closes}")
        return 1

    for name, factory in INDEPENDENCE_MODELS:
        if failed_axioms(factory()) != (name,):
            return 1

    assert AXIOM_NAMES and CLOSE_NAMES  # the report is keyed to the declared order
    return 0
