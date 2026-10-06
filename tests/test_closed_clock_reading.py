"""An executable reading of the L0 triangle: positions of a closed three-step clock.

PROPOSED, OUTSIDE L0. Nothing here is an L0 claim and no L0 file is touched.

Setting (from hyperphysics `docs/research/TIME_BUBBLE_SHEET.md`): a frozen computation is a chain of
states `psi_t` and rules `U_t`; its energy is the total squared violation of derivation steps, so a
chain is valid exactly when every step `psi_{t+1} = U_{t+1} psi_t` holds. Close the chain into a
3-cycle (the closing rule is `U_3 = (U_2 U_1)^dagger`) and read the three clock positions as the three
registers (position 0 is the closure/shape, then matter, then reading).

Interpretation of the primitives in a `SignModel`: `turns` = the successor position; `advances`
holds `(turn(x), x)` exactly when the step `x -> turn(x)` is valid; `derives` holds `(y, closure)` for
every `y` reachable from the closure by valid steps (zero or more); `returns` holds `(y, x)` when `x`
is reachable from `y` by one or more valid steps. Then: the four axioms hold IFF all three steps are
valid, i.e. iff the cycle has zero violation energy. Checked on random closed cycles (positive) and on
cycles with one state corrupted (negative controls), with the state-space arithmetic done in plain
complex numbers (no outside dependency).

What this shows: the L0 axioms have an exact physical-structure interpretation under which
`ax-triangle` is circuit closure. What it does not show: that L0 IS this, that three is the right number
(GC-3 stays open), or that L0 is a logic.
"""
import cmath
import math
import random
import unittest

from hyperlogic.triangle import SignModel, check_axioms, failed_axioms, is_model

SIGNS = ("closure", "matter", "reading")
TOL = 1e-9


def unitary(rng):
    a, b, c = (rng.uniform(0, 2 * math.pi) for _ in range(3))
    return [[math.cos(a) * cmath.exp(1j * b), -math.sin(a) * cmath.exp(1j * c)],
            [math.sin(a) * cmath.exp(-1j * c), math.cos(a) * cmath.exp(-1j * b)]]


def mv(m, v):
    return [m[0][0] * v[0] + m[0][1] * v[1], m[1][0] * v[0] + m[1][1] * v[1]]


def mm(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]


def dag(m):
    return [[m[0][0].conjugate(), m[1][0].conjugate()], [m[0][1].conjugate(), m[1][1].conjugate()]]


def closed_cycle(rng):
    u1, u2 = unitary(rng), unitary(rng)
    u3 = dag(mm(u2, u1))
    psi0 = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(2)]
    n = math.sqrt(sum(abs(x) ** 2 for x in psi0))
    psi0 = [x / n for x in psi0]
    return [u1, u2, u3], [psi0, mv(u1, psi0), mv(u2, mv(u1, psi0))]


def violations(gates, psis):
    total = 0.0
    for t in range(3):
        nxt = psis[(t + 1) % 3]
        pred = mv(gates[t], psis[t])
        total += sum(abs(a - b) ** 2 for a, b in zip(nxt, pred))
    return total


def sign_model(gates, psis):
    valid = {t: sum(abs(a - b) ** 2 for a, b in zip(psis[(t + 1) % 3], mv(gates[t], psis[t]))) < TOL
             for t in range(3)}
    turns = tuple((SIGNS[t], SIGNS[(t + 1) % 3]) for t in range(3))
    advances = frozenset((SIGNS[(t + 1) % 3], SIGNS[t]) for t in range(3) if valid[t])
    def reach(t0, minimum):
        out, cur, steps = set(), t0, 0
        while valid[cur] and steps < 3:
            cur = (cur + 1) % 3
            steps += 1
            out.add(cur)
        if minimum == 0:
            out.add(t0)
        return out
    derives = frozenset((SIGNS[y], SIGNS[0]) for y in reach(0, 0))
    returns = frozenset((SIGNS[y], SIGNS[x]) for y in range(3) for x in reach(y, 1))
    return SignModel("closed-clock", SIGNS, "closure", turns, advances, derives, returns)


class ClosedClockReadingTests(unittest.TestCase):
    def test_a_closed_valid_cycle_is_a_model_of_all_four_axioms(self):
        rng = random.Random(20261006)
        for _ in range(50):
            gates, psis = closed_cycle(rng)
            self.assertLess(violations(gates, psis), TOL)
            m = sign_model(gates, psis)
            self.assertTrue(is_model(m), failed_axioms(m))

    def test_model_iff_zero_violation_energy(self):
        rng = random.Random(20261007)
        for i in range(200):
            gates, psis = closed_cycle(rng)
            if i % 2:
                k = rng.randrange(3)
                psis[k] = [x + 0.3 for x in psis[k]]  # corrupt one state: a contradiction
            m = sign_model(gates, psis)
            self.assertEqual(is_model(m), violations(gates, psis) < TOL, i)

    def test_negative_control_open_circuit_fails_triangle(self):
        rng = random.Random(20261008)
        gates, psis = closed_cycle(rng)
        gates[2] = unitary(rng)   # the closing rule no longer closes the circuit
        m = sign_model(gates, psis)
        self.assertFalse(is_model(m))
        self.assertIn("ax-advance", failed_axioms(m))

    def test_negative_control_corrupted_state_is_reported_by_name(self):
        rng = random.Random(20261009)
        gates, psis = closed_cycle(rng)
        psis[1] = [x + 0.5 for x in psis[1]]
        self.assertTrue(failed_axioms(sign_model(gates, psis)))

    def test_verdicts_stay_non_boolean(self):
        rng = random.Random(20261010)
        gates, psis = closed_cycle(rng)
        for v in check_axioms(sign_model(gates, psis)):
            with self.assertRaises(TypeError):
                bool(v)


if __name__ == "__main__":
    unittest.main()
