"""The L0 triangle: finite sign models and checkable derivation claims.

This module implements `L0_triangle.hm` and nothing above it. It has no
dependencies outside the standard library, on purpose: a foundation that needs a
proof assistant, an ordinal notation or another package in order to state its
ground is not a foundation.

The irreducible is `closure`, the sign whose shape, matter and reading coincide.
The sole operation is `turn`, which advances a sign one edge around the triangle
shape -> matter -> reading -> shape. Three turns are a circuit, and that period
of three is the one structural place this layer differs from hypermath, whose
`ax-box` closes an orbit at two steps.

Nothing here is a logic. There is no connective, no quantifier, no inference
rule, and no proof object in this module, and `L0_triangle.hm` GC-1 through GC-5
record exactly what is and is not established.

Epistemic contract, enforced by the return types below:

- A claim that HOLDS_IN_MODEL has been checked against one finite structure.
  That is not a proof of validity and must never be reported as one.
- A claim that FAILS_IN_MODEL, where the structure satisfies all four axioms,
  is REFUTED outright. One countermodel settles a universal claim.

`Verdict` deliberately has no truth value. `if verdict:` raises, because the
interesting distinction is between "checked here" and "established", and a
boolean erases exactly that distinction.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

Pair = tuple[str, str]


class Status(str, Enum):
    """Whether a claim was observed to hold in one finite structure."""

    HOLDS_IN_MODEL = "HOLDS_IN_MODEL"
    FAILS_IN_MODEL = "FAILS_IN_MODEL"


class NotAModel(ValueError):
    """The structure fails at least one L0 axiom, so it refutes nothing."""


def _name(value: object, label: str) -> None:
    if type(value) is not str or not value.strip():
        raise ValueError(f"{label} must be a nonempty string")


def _relation(value: object, signs: tuple[str, ...], label: str) -> None:
    if type(value) is not frozenset:
        raise TypeError(f"{label} must be a frozenset of sign pairs")
    for item in value:
        if type(item) is not tuple or len(item) != 2:
            raise TypeError(f"{label} must contain two-element tuples")
        for part in item:
            if part not in signs:
                raise ValueError(f"{label} mentions the unknown sign {part!r}")


@dataclass(frozen=True, slots=True)
class Verdict:
    """The outcome of checking one claim against one finite structure.

    `witness` names the signs that produced the outcome. For a failure it is the
    counterexample; for a success it is empty, because a success has no
    distinguished witness and inventing one would overstate what was checked.
    """

    claim: str
    status: Status
    witness: tuple[str, ...] = ()
    note: str = ""

    def __post_init__(self) -> None:
        _name(self.claim, "claim")
        if type(self.status) is not Status:
            raise TypeError("status must be a Status")
        if type(self.witness) is not tuple or any(type(w) is not str for w in self.witness):
            raise TypeError("witness must be a tuple of sign names")
        if self.status is Status.HOLDS_IN_MODEL and self.witness:
            raise ValueError("a claim holding in a model has no distinguished witness")
        if self.status is Status.FAILS_IN_MODEL and not self.witness:
            raise ValueError("a failure must name its counterexample")

    def __bool__(self) -> bool:
        raise TypeError(
            "Verdict has no truth value: compare .status explicitly. "
            "HOLDS_IN_MODEL is not validity, and treating it as True erases that."
        )


@dataclass(frozen=True, slots=True)
class SignModel:
    """A finite structure interpreting the L0 primitives and opaque predicates.

    `turns` is a total function on the carrier, given as ordered pairs so the
    structure stays hashable and its checking order stays deterministic.

    The three relations interpret the OPAQUE predicates of Section II. They are
    deliberately unconstrained beyond being relations on the carrier. In
    particular `advances` is not required to be irreflexive: reading it as
    non-identity is the Section VI close talking, not an L0 fact, and forcing it
    at construction would smuggle that close into the structure. Ask the
    question explicitly with `advances_is_irreflexive`.
    """

    name: str
    signs: tuple[str, ...]
    closure: str
    turns: tuple[Pair, ...]
    advances: frozenset[Pair]
    derives: frozenset[Pair]
    returns: frozenset[Pair]

    def __post_init__(self) -> None:
        _name(self.name, "model name")
        if type(self.signs) is not tuple or not self.signs:
            raise ValueError("signs must be a nonempty tuple")
        for sign in self.signs:
            _name(sign, "sign")
        if len(set(self.signs)) != len(self.signs):
            raise ValueError("sign names must be unique")
        if self.closure not in self.signs:
            raise ValueError("the closure must be a sign; it is never of another kind")
        if type(self.turns) is not tuple:
            raise TypeError("turns must be a tuple of pairs")
        sources = [pair[0] for pair in self.turns]
        if sorted(sources) != sorted(self.signs):
            raise ValueError("turn must be a total function: exactly one image per sign")
        for _, target in self.turns:
            if target not in self.signs:
                raise ValueError("turn must land inside the carrier")
        _relation(self.advances, self.signs, "advances")
        _relation(self.derives, self.signs, "derives")
        _relation(self.returns, self.signs, "returns")

    def turn(self, sign: str) -> str:
        """Apply the sole primitive operation once."""
        for source, target in self.turns:
            if source == sign:
                return target
        raise KeyError(f"{sign!r} is not a sign of this model")

    def turn_n(self, sign: str, times: int) -> str:
        """Apply `turn` a given number of times."""
        if type(times) is not int or times < 0:
            raise ValueError("times must be a nonnegative integer")
        current = sign
        for _ in range(times):
            current = self.turn(current)
        return current


# ---------------------------------------------------------------------------
# Section III axioms. Each returns a Verdict; none returns a bool.
# ---------------------------------------------------------------------------


def ax_advance(model: SignModel) -> Verdict:
    """Turning moves a sign past where it was."""
    for sign in model.signs:
        if (model.turn(sign), sign) not in model.advances:
            return Verdict(
                "ax-advance", Status.FAILS_IN_MODEL, (sign,),
                "turn(x) does not advance past this x",
            )
    return Verdict("ax-advance", Status.HOLDS_IN_MODEL)


def ax_stay(model: SignModel) -> Verdict:
    """Turning stays inside what is derivable from the closure."""
    for sign in model.signs:
        if (model.turn(sign), model.closure) not in model.derives:
            return Verdict(
                "ax-stay", Status.FAILS_IN_MODEL, (sign,),
                "turn(x) is not derivable from the closure for this x",
            )
    return Verdict("ax-stay", Status.HOLDS_IN_MODEL)


def ax_triangle(model: SignModel) -> Verdict:
    """THE self-grounding axiom: three turns are a circuit. A cycle needs no exterior."""
    for sign in model.signs:
        if (model.turn_n(sign, 3), sign) not in model.returns:
            return Verdict(
                "ax-triangle", Status.FAILS_IN_MODEL, (sign,),
                "the three-step circuit does not return to this x",
            )
    return Verdict("ax-triangle", Status.HOLDS_IN_MODEL)


def ax_closure_self(model: SignModel) -> Verdict:
    """The closure already returns after one turn. Not a claim that it made itself."""
    if (model.turn(model.closure), model.closure) not in model.returns:
        return Verdict(
            "ax-closure-self", Status.FAILS_IN_MODEL, (model.closure,),
            "one turn of the closure does not return to it",
        )
    return Verdict("ax-closure-self", Status.HOLDS_IN_MODEL)


AXIOMS = (ax_advance, ax_stay, ax_triangle, ax_closure_self)
AXIOM_NAMES = ("ax-advance", "ax-stay", "ax-triangle", "ax-closure-self")


def check_axioms(model: SignModel) -> tuple[Verdict, ...]:
    """Check all four Section III axioms in declaration order."""
    return tuple(axiom(model) for axiom in AXIOMS)


def is_model(model: SignModel) -> bool:
    """Whether the structure satisfies every L0 axiom.

    This is a plain bool because it is a question about one finite structure,
    not a claim about the theory. It is the precondition for a refutation.
    """
    return all(v.status is Status.HOLDS_IN_MODEL for v in check_axioms(model))


def failed_axioms(model: SignModel) -> tuple[str, ...]:
    """The names of the axioms this structure does not satisfy."""
    return tuple(v.claim for v in check_axioms(model) if v.status is Status.FAILS_IN_MODEL)


# ---------------------------------------------------------------------------
# Section IV derives.
# ---------------------------------------------------------------------------


def circuit(model: SignModel, sign: str) -> tuple[str, ...]:
    """Every sign reachable from `sign` under turn, reflexively.

    The carrier is finite and turn is total, so this terminates: the walk
    revisits a sign within at most len(signs) steps.
    """
    if sign not in model.signs:
        raise KeyError(f"{sign!r} is not a sign of this model")
    orbit: list[str] = [sign]
    current = sign
    while True:
        current = model.turn(current)
        if current in orbit:
            return tuple(orbit)
        orbit.append(current)


def d_turn_advances(model: SignModel) -> Verdict:
    """The closure's own turn is not the closure."""
    if (model.turn(model.closure), model.closure) not in model.advances:
        return Verdict(
            "d-turn-advances", Status.FAILS_IN_MODEL, (model.closure,),
            "the closure's turn does not advance past the closure",
        )
    return Verdict("d-turn-advances", Status.HOLDS_IN_MODEL)


def d_turn_stays(model: SignModel) -> Verdict:
    """What the closure turns into is still derivable from it."""
    if (model.turn(model.closure), model.closure) not in model.derives:
        return Verdict(
            "d-turn-stays", Status.FAILS_IN_MODEL, (model.closure,),
            "the closure's turn is not derivable from the closure",
        )
    return Verdict("d-turn-stays", Status.HOLDS_IN_MODEL)


def d_triple_turn_returns(model: SignModel) -> Verdict:
    """The full circuit of the closure comes back to the closure."""
    if (model.turn_n(model.closure, 3), model.closure) not in model.returns:
        return Verdict(
            "d-triple-turn-returns", Status.FAILS_IN_MODEL, (model.closure,),
            "the closure's three-step circuit does not return",
        )
    return Verdict("d-triple-turn-returns", Status.HOLDS_IN_MODEL)


def d_two_signs(model: SignModel) -> Verdict:
    """Plurality, derived rather than assumed.

    Section I posits one sign. This obtains a second from ax-advance, exactly as
    hypermath obtains `two-members-in-class` and hyperethics obtains
    `d-two-bearers`, rather than declaring a carrier of size two.
    """
    if model.turn(model.closure) == model.closure:
        return Verdict(
            "d-two-signs", Status.FAILS_IN_MODEL, (model.closure,),
            "the closure is its own turn, so no second sign is obtained",
        )
    return Verdict("d-two-signs", Status.HOLDS_IN_MODEL)


def d_return_exists(model: SignModel) -> Verdict:
    """Every sign has a return point. This is what makes it a cycle, not a sequence."""
    for sign in model.signs:
        if (model.turn_n(sign, 3), sign) not in model.returns:
            return Verdict(
                "d-return-exists", Status.FAILS_IN_MODEL, (sign,),
                "this sign has no return point",
            )
    return Verdict("d-return-exists", Status.HOLDS_IN_MODEL)


DERIVES = (d_turn_advances, d_turn_stays, d_triple_turn_returns, d_two_signs, d_return_exists)


def check_derives(model: SignModel) -> tuple[Verdict, ...]:
    """Check every Section IV derive."""
    return tuple(derive(model) for derive in DERIVES)


# ---------------------------------------------------------------------------
# Section VIII non-derives, stated so a later layer cannot quietly assume them.
# ---------------------------------------------------------------------------


def universal_one_turn_return(model: SignModel) -> Verdict:
    """Every sign returns after ONE turn. NOT an L0 theorem.

    ax-closure-self grants this to the closure alone. Generalising it would
    erase the only thing that distinguishes the irreducible from its own output.
    """
    for sign in model.signs:
        if (model.turn(sign), sign) not in model.returns:
            return Verdict(
                "nd-universal-one-turn-return", Status.FAILS_IN_MODEL, (sign,),
                "one turn of this sign does not return to it",
            )
    return Verdict("nd-universal-one-turn-return", Status.HOLDS_IN_MODEL)


def two_turn_return(model: SignModel) -> Verdict:
    """Two turns suffice for a circuit. NOT an L0 theorem, and the period matters.

    hypermath's `ax-box` closes its orbit at two steps. This layer closes at
    three, and the difference is not cosmetic: a structure satisfying all four
    axioms here can fail a two-step return. That failure is the executable
    content of the claim that the triangle has three edges.
    """
    for sign in model.signs:
        if (model.turn_n(sign, 2), sign) not in model.returns:
            return Verdict(
                "nd-two-turn-return", Status.FAILS_IN_MODEL, (sign,),
                "the two-step orbit does not return to this x",
            )
    return Verdict("nd-two-turn-return", Status.HOLDS_IN_MODEL)


def advances_is_irreflexive(model: SignModel) -> Verdict:
    """Whether this model reads `advances` as non-identity.

    A FAILS_IN_MODEL outcome is not a defect. `advances` is opaque until Section
    VI, and a structure may interpret it in a way the close would later reject.
    """
    for left, right in sorted(model.advances):
        if left == right:
            return Verdict(
                "advances-is-irreflexive", Status.FAILS_IN_MODEL, (left,),
                "this model lets a sign advance past itself",
            )
    return Verdict("advances-is-irreflexive", Status.HOLDS_IN_MODEL)


def refuted_by(claim: str, verdict: Verdict, model: SignModel) -> str:
    """Report a conclusive refutation, or raise if the structure cannot refute.

    A structure only refutes a universal claim when it satisfies every axiom. A
    failure inside a non-model shows nothing about the theory, so this raises
    rather than returning a softer result.
    """
    _name(claim, "claim")
    if not is_model(model):
        raise NotAModel(
            f"{model.name!r} fails {', '.join(failed_axioms(model))} and so refutes nothing"
        )
    if verdict.status is not Status.FAILS_IN_MODEL:
        raise ValueError("a refutation requires a failure to point at")
    return (
        f"REFUTED: {claim} is not a consequence of the L0 axioms. "
        f"Countermodel {model.name!r} satisfies all four axioms and fails at "
        f"{', '.join(verdict.witness)} ({verdict.note})."
    )
