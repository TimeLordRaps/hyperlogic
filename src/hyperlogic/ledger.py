"""PROPOSED, OUTSIDE L0: a commit-before-outcome prediction ledger.

THIS MODULE IS NOT PART OF THE L0 TRIANGLE AND IS NOT COVERED BY ITS CLAIMS. It sits beside
`status.py` and discharges none of GC-1 .. GC-5.

WHY. A claim of the form "this kind of experience tracks events it could not have known" is
unfalsifiable by looking back: an observer who counts matches afterwards counts the hits and
forgets the misses, and with enough events something always matches. The status layer shows the
structure (`R1`: tests always return null). What can be checked is a claim stated BEFORE the
outcome, with the chance of a match stated before the outcome, with every committed claim counted.

WHAT IT DOES.
  * `commit` seals a prediction as `sha256(salt + text)` together with the probability a pure chance
    process gives it, a category and a caller-supplied timestamp, and chains each entry to the
    previous one by hash, so entries cannot be edited, removed or reordered without detection
    (`verify_chain`).
  * `reveal` opens a commitment and checks it against the seal; `resolve` records the outcome.
  * `score` counts EVERY committed entry: unrevealed or unresolved entries count as misses and a
    withdrawn entry counts as a miss, so nothing can be dropped silently. It reports hits, the hits
    expected from the stated baselines, and the exact probability of at least that many hits if every
    prediction were an independent chance event with its stated baseline (Poisson-binomial tail).

WHAT IT DOES NOT DO. It does not check that a baseline is honest (a baseline stated too low makes
chance look impressive), that the entries are independent, or that the timestamps are true; a
timestamp is as trustworthy as the party that supplies it, so a publication of the ledger's head
hash somewhere a third party can see it is part of using this. It decides nothing about any
postulate: it computes one tail probability under stated assumptions.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from fractions import Fraction

GENESIS = "0" * 64


def _h(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()


def seal(text: str, salt: str) -> str:
    """The commitment to a prediction text."""
    if not text or not salt:
        raise ValueError("text and salt must be nonempty")
    return _h("seal", salt, text)


@dataclass
class Entry:
    index: int
    committed_at: str
    category: str
    baseline: Fraction            # chance probability of a hit, fixed at commit time
    sealed: str
    prev: str
    revealed_text: str | None = None
    outcome: bool | None = None
    withdrawn: bool = False
    resolved_at: str | None = None

    def digest(self) -> str:
        return _h("entry", str(self.index), self.committed_at, self.category,
                  str(self.baseline), self.sealed, self.prev)


@dataclass
class Ledger:
    entries: list = field(default_factory=list)

    def head(self) -> str:
        return self.entries[-1].digest() if self.entries else GENESIS

    def commit(self, text: str, salt: str, baseline, when: str, category: str = "general") -> Entry:
        p = Fraction(baseline)
        if not 0 < p < 1:
            raise ValueError("a baseline chance must lie strictly between 0 and 1")
        if not when or not category:
            raise ValueError("a timestamp and a category are required")
        entry = Entry(len(self.entries), when, category, p, seal(text, salt), self.head())
        self.entries.append(entry)
        return entry

    def reveal(self, index: int, text: str, salt: str) -> None:
        entry = self.entries[index]
        if entry.sealed != seal(text, salt):
            raise ValueError("the text and salt do not match the sealed commitment")
        entry.revealed_text = text

    def resolve(self, index: int, outcome: bool, when: str) -> None:
        entry = self.entries[index]
        if entry.revealed_text is None:
            raise ValueError("an entry must be revealed before it is resolved")
        if entry.outcome is not None or entry.withdrawn:
            raise ValueError("an entry is resolved once")
        entry.outcome, entry.resolved_at = bool(outcome), when

    def withdraw(self, index: int, when: str) -> None:
        entry = self.entries[index]
        if entry.outcome is not None or entry.withdrawn:
            raise ValueError("an entry is resolved once")
        entry.withdrawn, entry.resolved_at = True, when

    def verify_chain(self) -> bool:
        prev = GENESIS
        for i, e in enumerate(self.entries):
            if e.index != i or e.prev != prev:
                return False
            prev = e.digest()
        return True

    def score(self) -> dict:
        """Every committed entry counts; only a recorded hit is a hit."""
        hits = sum(1 for e in self.entries if e.outcome is True)
        expected = sum(e.baseline for e in self.entries)
        return {
            "committed": len(self.entries),
            "hits": hits,
            "counted_as_misses": sum(1 for e in self.entries if e.outcome is not True),
            "expected_hits_by_chance": expected,
            "p_at_least_this_many_by_chance": tail_probability([e.baseline for e in self.entries], hits),
        }

    def to_json(self) -> str:
        rows = [{**e.__dict__, "baseline": str(e.baseline)} for e in self.entries]
        return json.dumps(rows, sort_keys=True)

    @classmethod
    def from_json(cls, blob: str) -> "Ledger":
        ledger = cls()
        for row in json.loads(blob):
            row["baseline"] = Fraction(row["baseline"])
            ledger.entries.append(Entry(**row))
        return ledger


def tail_probability(baselines, hits: int) -> Fraction:
    """Exact P(X >= hits) for X a sum of independent Bernoulli variables with the given chances
    (a Poisson-binomial tail, by dynamic programming over exact fractions)."""
    dist = [Fraction(1)]
    for p in baselines:
        p = Fraction(p)
        nxt = [Fraction(0)] * (len(dist) + 1)
        for k, mass in enumerate(dist):
            nxt[k] += mass * (1 - p)
            nxt[k + 1] += mass * p
        dist = nxt
    return sum(dist[hits:], Fraction(0))
