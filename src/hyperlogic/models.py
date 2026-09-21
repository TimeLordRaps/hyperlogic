"""Canonical finite structures for `L0_triangle.hm`.

Three kinds of structure live here, and the distinction between them is the
whole point:

- `minimal_model` satisfies all four axioms. Claims that fail in it are REFUTED,
  because one countermodel settles a universal claim.
- The four independence structures each drop exactly one axiom. They show that
  no axiom is implied by the other three, and they refute nothing, because a
  structure that is not a model of the theory says nothing about the theory.
- `collapsed_model` satisfies all four axioms and still fails `d-two-signs`.
  That is not a defect in the derive; it is the executable proof that the derive
  needs the Section VI close as well as the axioms.
- `separating_model` witnesses a Section V property that `minimal_model` cannot:
  that `same-conclusion` does NOT imply `interderivable`. In the minimal circuit
  the two relations happen to coincide, so a declared strictness would have gone
  unwitnessed there. A declared property with no structure exhibiting it is a
  claim, not a check.
"""

from __future__ import annotations

from .triangle import SignModel

CLOSURE = "closure"
MATTER = "matter"
READING = "reading"
ECHO = "echo"

_SIGNS = (CLOSURE, MATTER, READING)
_TURNS = ((CLOSURE, MATTER), (MATTER, READING), (READING, CLOSURE))

#: turn(x) advances past x, for each of the three signs.
_ADVANCES = frozenset({(MATTER, CLOSURE), (READING, MATTER), (CLOSURE, READING)})

#: turn(x) is derivable from the closure, for each of the three signs, and each
#: reachable sign derives itself. The first group is what ax-stay forces. The
#: second is not forced by any axiom; it is what makes `shares-context` reflexive
#: on reachable signs, as Section V declares it to be. A model may satisfy more
#: than the axioms demand, and this one does.
_DERIVES = frozenset(
    {
        (MATTER, CLOSURE), (READING, CLOSURE), (CLOSURE, CLOSURE),
        (MATTER, MATTER), (READING, READING),
    }
)

#: the three-step circuit returns for every sign, and the closure returns after
#: one turn as well. Note what is ABSENT: no two-step return, and no one-turn
#: return for `matter` or `reading`. Both absences are load-bearing.
_RETURNS = frozenset(
    {(CLOSURE, CLOSURE), (MATTER, MATTER), (READING, READING), (MATTER, CLOSURE)}
)


def minimal_model() -> SignModel:
    """The three-register circuit: shape, matter, reading, and back.

    This is the intended reading of the layer. `turn` is the 3-cycle, so the
    three-step circuit is the identity and `ax-triangle` holds everywhere, while
    the two-step orbit lands on the wrong register and does not return.
    """
    return SignModel(
        "minimal", _SIGNS, CLOSURE, _TURNS, _ADVANCES, _DERIVES, _RETURNS,
    )


def without_advance() -> SignModel:
    """Drops ax-advance only: the closure's turn no longer advances past it."""
    return SignModel(
        "without-advance", _SIGNS, CLOSURE, _TURNS,
        _ADVANCES - {(MATTER, CLOSURE)}, _DERIVES, _RETURNS,
    )


def without_stay() -> SignModel:
    """Drops ax-stay only: one turn lands outside what the closure derives."""
    return SignModel(
        "without-stay", _SIGNS, CLOSURE, _TURNS,
        _ADVANCES, _DERIVES - {(CLOSURE, CLOSURE)}, _RETURNS,
    )


def without_triangle() -> SignModel:
    """Drops ax-triangle only: one sign's three-step circuit does not return."""
    return SignModel(
        "without-triangle", _SIGNS, CLOSURE, _TURNS,
        _ADVANCES, _DERIVES, _RETURNS - {(MATTER, MATTER)},
    )


def without_closure_self() -> SignModel:
    """Drops ax-closure-self only: the closure no longer returns after one turn.

    The three-step circuit still closes for every sign, which is exactly why
    ax-closure-self is not redundant: the other three axioms are universally
    quantified and say nothing that singles out the irreducible.
    """
    return SignModel(
        "without-closure-self", _SIGNS, CLOSURE, _TURNS,
        _ADVANCES, _DERIVES, _RETURNS - {(MATTER, CLOSURE)},
    )


def collapsed_model() -> SignModel:
    """One sign that is its own turn. Satisfies all four axioms.

    This structure reads `advances` reflexively, which the Section VI close
    forbids but the axioms do not. It is a model of the axioms and it fails
    `d-two-signs`, so it establishes that plurality does not follow from the
    four axioms alone.
    """
    only = frozenset({(CLOSURE, CLOSURE)})
    return SignModel(
        "collapsed", (CLOSURE,), CLOSURE, ((CLOSURE, CLOSURE),), only, only, only,
    )


def separating_model() -> SignModel:
    """Four signs, two of which land on one conclusion by different routes.

    `echo` turns to `reading`, as `matter` does, so the two share a conclusion.
    They are NOT interderivable: `returns` relates matter to echo and not the
    other way. This is the structure that makes Section V's "same-conclusion
    does not imply interderivable" a checked property rather than a declared one,
    and the minimal circuit cannot do it, because there the two relations have
    the same extension.

    `echo` is deliberately unreachable from the closure. The Section VI close of
    `log-derives` is stated on reachable signs, and a structure that puts a sign
    outside the circuit is how that restriction gets exercised.
    """
    signs = (CLOSURE, MATTER, READING, ECHO)
    turns = ((CLOSURE, MATTER), (MATTER, READING), (READING, CLOSURE), (ECHO, READING))
    advances = frozenset(
        {(MATTER, CLOSURE), (READING, MATTER), (CLOSURE, READING), (READING, ECHO)}
    )
    derives = frozenset(
        {
            (MATTER, CLOSURE), (READING, CLOSURE), (CLOSURE, CLOSURE),
            (MATTER, MATTER), (READING, READING), (ECHO, ECHO), (MATTER, ECHO),
        }
    )
    returns = frozenset(
        {
            (CLOSURE, CLOSURE), (MATTER, MATTER), (READING, READING),
            (MATTER, ECHO), (MATTER, CLOSURE),
        }
    )
    return SignModel("separating", signs, CLOSURE, turns, advances, derives, returns)


#: Every canonical structure, in the order the report walks them.
MODELS = (minimal_model, separating_model, collapsed_model)

#: One structure per axiom, each failing that axiom and no other.
INDEPENDENCE_MODELS = (
    ("ax-advance", without_advance),
    ("ax-stay", without_stay),
    ("ax-triangle", without_triangle),
    ("ax-closure-self", without_closure_self),
)
