"""PROPOSED, OUTSIDE L0: GL (Goedel-Loeb provability logic) as a decision procedure.

THIS MODULE IS NOT PART OF THE L0 TRIANGLE AND IS NOT COVERED BY ITS CLAIMS. L0
has no connective, no quantifier, no inference rule and no proof object, and that
stays exactly true of L0. This module has all of: connectives (not, and, or,
imp), a modality (box, read as "provable in a fixed theory"), and an inference
system (the sequent calculus GLS, with proof search). It is a separately
proposed layer, imported by nothing in L0, and it discharges none of GC-1 ..
GC-5. It is the unprovability half of the derivation-status work, next to
`status.py`.

Formulas are tuples:
    ("var", p) | ("bot",) | ("not", A) | ("imp", A, B) | ("and", A, B)
    | ("or", A, B) | ("box", A)

`prove(A)` is backward proof search in GLS: the propositional rules plus the GL
rule, from  B1..Bn, box B1..box Bn, box A => A  infer  box B1..box Bn => box A.
Each modal step adds box A to the left, and box A can be principal only while it
is absent there, so search terminates.

`countermodel(A)` searches finite irreflexive transitive trees. It is an
independent semantic oracle: GL is sound and complete for them. `prove` and
`countermodel` share no code beyond the formula syntax, so their agreement on
random formulas (`differential`) is a real cross-check and not a tautology.

LIMITS. This decides GL. It is the logic of provability in a theory like PA by
Solovay's theorem, which is a result cited here and not proved or checked here.
Propositional modal only: no first-order quantifier. `true_in_arithmetic` is
exact for letterless sentences and for nothing else. The countermodel oracle is
bounded (`max_nodes`, default 4), so "no countermodel found" is evidence about
small trees and the differential test shows only agreement on its sample.
Modal agents are evaluated on a linear frame, not by running programs.
"""

from __future__ import annotations

import random
from functools import lru_cache
from itertools import product
from typing import Any

Formula = tuple[Any, ...]

BOT: Formula = ("bot",)


def var(p: str) -> Formula:
    return ("var", p)


def neg(a: Formula) -> Formula:
    return ("not", a)


def imp(a: Formula, b: Formula) -> Formula:
    return ("imp", a, b)


def conj(a: Formula, b: Formula) -> Formula:
    return ("and", a, b)


def disj(a: Formula, b: Formula) -> Formula:
    return ("or", a, b)


def box(a: Formula) -> Formula:
    return ("box", a)


def iff(a: Formula, b: Formula) -> Formula:
    return conj(imp(a, b), imp(b, a))


def diamond(a: Formula) -> Formula:
    return neg(box(neg(a)))


TOP = neg(BOT)
CON = neg(box(BOT))  # "the theory is consistent"


@lru_cache(maxsize=None)
def _prove(left: frozenset, right: frozenset) -> bool:
    if BOT in left or left & right:
        return True
    for f in left:
        k, rest = f[0], left - {f}
        if k == "not":
            return _prove(rest, right | {f[1]})
        if k == "and":
            return _prove(rest | {f[1], f[2]}, right)
        if k == "or":
            return _prove(rest | {f[1]}, right) and _prove(rest | {f[2]}, right)
        if k == "imp":
            return _prove(rest, right | {f[1]}) and _prove(rest | {f[2]}, right)
    for f in right:
        k, rest = f[0], right - {f}
        if k == "not":
            return _prove(left | {f[1]}, rest)
        if k == "and":
            return _prove(left, rest | {f[1]}) and _prove(left, rest | {f[2]})
        if k == "or":
            return _prove(left, rest | {f[1], f[2]})
        if k == "imp":
            return _prove(left | {f[1]}, rest | {f[2]})
    boxed_left = {f for f in left if f[0] == "box"}
    unboxed = {f[1] for f in boxed_left}
    for f in right:
        if f[0] == "box" and f not in left:
            if _prove(frozenset(boxed_left | unboxed | {f}), frozenset({f[1]})):
                return True
    return False


def prove(a: Formula) -> bool:
    """True iff `a` is a theorem of GL."""
    return _prove(frozenset(), frozenset({a}))


def atoms(a: Formula, acc: set[str] | None = None) -> set[str]:
    acc = set() if acc is None else acc
    if a[0] == "var":
        acc.add(a[1])
    for sub in a[1:]:
        if isinstance(sub, tuple):
            atoms(sub, acc)
    return acc


def holds(a: Formula, w: int, R: dict, V: dict) -> bool:
    k = a[0]
    if k == "var":
        return V[(w, a[1])]
    if k == "bot":
        return False
    if k == "not":
        return not holds(a[1], w, R, V)
    if k == "imp":
        return (not holds(a[1], w, R, V)) or holds(a[2], w, R, V)
    if k == "and":
        return holds(a[1], w, R, V) and holds(a[2], w, R, V)
    if k == "or":
        return holds(a[1], w, R, V) or holds(a[2], w, R, V)
    if k == "box":
        return all(holds(a[1], v, R, V) for v in R[w])
    raise ValueError(k)


def trees(n: int):
    """Rooted trees on nodes 0..n-1 (parent index < child), as transitive-closure maps."""
    for parents in product(*[range(i) for i in range(1, n)]):
        children: dict[int, set[int]] = {i: set() for i in range(n)}
        for c, p in enumerate(parents, start=1):
            children[p].add(c)

        def desc(w: int, children: dict[int, set[int]] = children) -> set[int]:
            out: set[int] = set()
            for c in children[w]:
                out |= {c} | desc(c)
            return out

        yield {w: desc(w) for w in range(n)}


def countermodel(a: Formula, max_nodes: int = 4):
    """A (nodes, R, V) falsifying `a` at the root of a small tree, or None."""
    ps = sorted(atoms(a))
    for n in range(1, max_nodes + 1):
        for R in trees(n):
            for vals in product([False, True], repeat=n * len(ps)):
                V = {(w, p): vals[w * len(ps) + i] for w in range(n) for i, p in enumerate(ps)}
                if not holds(a, 0, R, V):
                    return n, R, V
    return None


# ------------------------------------------- arithmetic truth of letterless sentences

def true_in_arithmetic(a: Formula, height: int = 64) -> bool:
    """A letterless sentence is true in N iff it holds at the top of a long enough linear
    frame (box X at world k means X holds at every world below k). Exact for letterless GL
    sentences and for nothing else."""
    R = {k: set(range(k)) for k in range(height)}
    return holds(a, height - 1, R, {})


# ------------------------------------------- modal agents (program equilibrium)

def play(agent_a, agent_b, height: int = 64):
    """Outcome of two modal agents. Each decides at world k from `Box(pred)`, true iff `pred`
    held at every world below k (provability, read on a linear frame bottom-up). The value at
    a high enough world is the arithmetic truth of the agents' fixed point."""
    ca: list[bool] = []
    cb: list[bool] = []
    for k in range(height):
        def box_a(pred, k=k):  # box(pred) at world k
            return all(pred(j) for j in range(k))

        ca_k = agent_a(lambda j: cb[j], lambda j: ca[j], box_a)
        cb_k = agent_b(lambda j: ca[j], lambda j: cb[j], box_a)
        ca.append(ca_k)
        cb.append(cb_k)
    return ca[-1], cb[-1]


def FairBot(opp, me, Box):  # cooperate iff it is provable that the opponent cooperates
    return Box(opp)


def DefectBot(opp, me, Box):
    return False


def CooperateBot(opp, me, Box):
    return True


AGENTS = {"FairBot": FairBot, "DefectBot": DefectBot, "CooperateBot": CooperateBot}


# ------------------------------------------- the checks

def known_cases() -> dict[str, tuple[Formula, bool]]:
    """Named formulas and whether GL proves them (literature values)."""
    p = var("p")
    q = var("q")
    return {
        "K: box(p->q)->(box p->box q)": (imp(box(imp(p, q)), imp(box(p), box(q))), True),
        "4: box p->box box p": (imp(box(p), box(box(p))), True),
        "Loeb: box(box p->p)->box p": (imp(box(imp(box(p), p)), box(p)), True),
        "T: box p->p (reflection)": (imp(box(p), p), False),
        "Con is not provable: not box bot": (CON, False),
        "G2: Con -> not box Con": (imp(CON, neg(box(CON))), True),
        "proving own consistency implies inconsistent: box Con->box bot":
            (imp(box(CON), box(BOT)), True),
        "self-assertion closes (Henkin): both(p<->box p) -> p":
            (imp(conj(iff(p, box(p)), box(iff(p, box(p)))), p), True),
        "self-denial = consistency (Goedel): both(p<->not box p) -> (p<->Con)":
            (imp(conj(iff(p, neg(box(p))), box(iff(p, neg(box(p))))), iff(p, CON)), True),
    }


def check_known_cases() -> list[str]:
    out = []
    for name, (f, expected) in known_cases().items():
        got = prove(f)
        cm = None if got else countermodel(f, 4)
        assert got == expected, (name, got)
        assert got or cm is not None, ("no countermodel found for unprovable", name)
        out.append(("PROVABLE      " if got else "NOT PROVABLE  ") + name
                   + ("" if got else f"   (countermodel on {cm[0]} nodes)"))
    return out


def differential(samples: int = 300, seed: int = 20261004) -> int:
    """Prover vs countermodel oracle on random formulas. Returns the number that agree.

    Raises AssertionError on disagreement in either direction."""
    rng = random.Random(seed)
    p, q = var("p"), var("q")

    def rand(d: int) -> Formula:
        if d == 0:
            return rng.choice([p, q, BOT])
        k = rng.choice(["not", "imp", "and", "or", "box", "box"])
        if k == "not":
            return neg(rand(d - 1))
        if k == "box":
            return box(rand(d - 1))
        return {"imp": imp, "and": conj, "or": disj}[k](rand(d - 1), rand(d - 1))

    agree = 0
    for _ in range(samples):
        f = rand(3)
        proved = prove(f)
        cm = countermodel(f, 4)
        assert not (proved and cm is not None), ("unsound", f)
        assert proved or cm is not None, ("prover failed but no small countermodel", f)
        agree += 1
    return agree


def check() -> list[str]:
    """Run every check. Raises AssertionError on failure; returns the printed lines."""
    out = ["GL known cases (prover, with oracle countermodel for each unprovable one):"]
    out += ["  " + line for line in check_known_cases()]
    out.append("")
    out.append("arithmetic truth of letterless sentences:")
    for name, f in {"Con": CON, "box bot": box(BOT), "not box Con": neg(box(CON)),
                    "diamond top (= Con)": diamond(TOP)}.items():
        out.append(f"  {name}: {true_in_arithmetic(f)}")
    out.append("")
    n = differential()
    out.append(f"differential: prover and countermodel oracle agree on {n}/300 random formulas")
    out.append("")
    out.append("modal agents (outcome = arithmetic truth of the fixed point):")
    for a in AGENTS:
        for b in AGENTS:
            ra, rb = play(AGENTS[a], AGENTS[b])
            out.append(f"  {a:12s} vs {b:12s}: {'C' if ra else 'D'} {'C' if rb else 'D'}")
    return out


def main() -> int:
    print("\n".join(check()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
