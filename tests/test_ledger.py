"""The commit-before-outcome ledger: tamper evidence, no silent drops, exact chance tail."""
import itertools
import unittest
from fractions import Fraction

from hyperlogic.ledger import GENESIS, Ledger, match_to_sample_tail, seal, tail_probability


def make(n=4, p="1/10"):
    led = Ledger()
    for i in range(n):
        led.commit(f"prediction {i}", f"salt{i}", p, f"2026-10-0{i + 1}T00:00:00Z")
    return led


class LedgerTests(unittest.TestCase):
    def test_chain_detects_removal_and_reordering(self):
        self.assertTrue(make().verify_chain())
        led = make()
        del led.entries[1]
        self.assertFalse(led.verify_chain())
        led = make()
        led.entries[0], led.entries[1] = led.entries[1], led.entries[0]
        self.assertFalse(led.verify_chain())

    def test_editing_the_last_entry_is_caught_only_by_a_published_head(self):
        led = make()
        published = led.head()
        led.entries[-1].baseline = Fraction(9, 10)
        self.assertTrue(led.verify_chain())          # nothing after it links to it ...
        self.assertNotEqual(led.head(), published)   # ... so the published head is what exposes it

    def test_changing_a_committed_field_breaks_the_next_link(self):
        led = make()
        led.entries[1].baseline = Fraction(1, 2)
        self.assertFalse(led.verify_chain())

    def test_reveal_must_match_the_seal(self):
        led = make(1)
        with self.assertRaises(ValueError):
            led.reveal(0, "a different prediction", "salt0")
        with self.assertRaises(ValueError):
            led.reveal(0, "prediction 0", "wrong salt")
        led.reveal(0, "prediction 0", "salt0")
        self.assertEqual(led.entries[0].revealed_text, "prediction 0")

    def test_resolution_needs_a_reveal_and_happens_once(self):
        led = make(1)
        with self.assertRaises(ValueError):
            led.resolve(0, True, "2026-11-01")
        led.reveal(0, "prediction 0", "salt0")
        led.resolve(0, True, "2026-11-01")
        with self.assertRaises(ValueError):
            led.resolve(0, False, "2026-11-02")

    def test_nothing_can_be_dropped_silently(self):
        led = make(4, "1/10")
        for i in range(4):
            led.reveal(i, f"prediction {i}", f"salt{i}")
        led.resolve(0, True, "t")
        led.withdraw(1, "t")             # withdrawn counts as a miss
        # entries 2 and 3 are left unresolved: they count as misses too
        s = led.score()
        self.assertEqual((s["committed"], s["hits"], s["counted_as_misses"]), (4, 1, 3))
        self.assertEqual(s["p_at_least_this_many_by_chance"], 1 - Fraction(9, 10) ** 4)

    def test_selective_reporting_is_the_failure_the_ledger_prevents(self):
        # Ten predictions at 10% chance, one hit. Reporting only the hit looks like p = 1/10 for that
        # one claim; counting all ten gives the honest tail.
        led = make(10, "1/10")
        for i in range(10):
            led.reveal(i, f"prediction {i}", f"salt{i}")
        led.resolve(0, True, "t")
        for i in range(1, 10):
            led.resolve(i, False, "t")
        honest = led.score()["p_at_least_this_many_by_chance"]
        self.assertEqual(honest, 1 - Fraction(9, 10) ** 10)
        self.assertGreater(honest, Fraction(6, 10))     # one hit in ten at 10% is unremarkable

    def test_tail_probability_matches_brute_force(self):
        ps = [Fraction(1, 5), Fraction(1, 3), Fraction(1, 10), Fraction(1, 2)]
        for hits in range(0, 5):
            total = Fraction(0)
            for combo in itertools.product((0, 1), repeat=4):
                if sum(combo) >= hits:
                    prob = Fraction(1)
                    for c, p in zip(combo, ps):
                        prob *= p if c else 1 - p
                    total += prob
            self.assertEqual(tail_probability(ps, hits), total)

    def test_a_real_effect_would_show(self):
        led = make(10, "1/10")
        for i in range(10):
            led.reveal(i, f"prediction {i}", f"salt{i}")
            led.resolve(i, i < 7, "t")                  # seven hits in ten at 10% each
        self.assertLess(led.score()["p_at_least_this_many_by_chance"], Fraction(1, 10 ** 5))

    def test_baseline_must_be_a_real_chance_and_commit_needs_a_timestamp(self):
        led = Ledger()
        for bad in (0, 1, "3/2", -1):
            with self.assertRaises(ValueError):
                led.commit("x", "s", bad, "t")
        with self.assertRaises(ValueError):
            led.commit("x", "s", "1/2", "")

    def test_json_round_trip_preserves_the_chain(self):
        led = make()
        led.reveal(0, "prediction 0", "salt0")
        led.resolve(0, True, "t")
        back = Ledger.from_json(led.to_json())
        self.assertTrue(back.verify_chain())
        self.assertEqual(back.score(), led.score())
        self.assertEqual(Ledger().head(), GENESIS)
        self.assertNotEqual(seal("a", "s"), seal("a", "t"))


class MatchToSampleTests(unittest.TestCase):
    def test_chance_level_is_unremarkable_and_a_clear_effect_is_not(self):
        self.assertGreater(match_to_sample_tail(3, 12, 4), Fraction(1, 2))          # 12 trials, 4 options: 3 expected
        self.assertLess(match_to_sample_tail(9, 12, 4), Fraction(1, 1000))

    def test_matches_the_binomial_tail_by_brute_force(self):
        n, k = 6, 3
        total = sum(Fraction(1, 3) ** j * Fraction(2, 3) ** (n - j) * _comb(n, j) for j in range(k, n + 1))
        self.assertEqual(match_to_sample_tail(k, n, 3), total)

    def test_a_fixed_artifact_cannot_depend_on_a_later_random_choice(self):
        # The recorded text is constant; the randomised response is drawn afterwards. Over every possible
        # draw the fixed text matches exactly one of the options, so a judge who maximises agreement with
        # the fixed text is right in exactly 1 of N equally likely draws: the chance level.
        options = ["a", "b", "c", "d"]
        fixed_best_match = "b"
        right = sum(1 for draw in options if draw == fixed_best_match)
        self.assertEqual(Fraction(right, len(options)), Fraction(1, 4))

    def test_arguments_are_validated(self):
        for bad in ((1, 0, 4), (1, 5, 1), (6, 5, 4), (-1, 5, 4)):
            with self.assertRaises(ValueError):
                match_to_sample_tail(*bad)


def _comb(n, k):
    from math import comb
    return comb(n, k)


if __name__ == "__main__":
    unittest.main()
