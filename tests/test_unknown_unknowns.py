"""An unknown unknown, formally: not known, and not known to be not known (GL, hyperlogic layer).

For a theory T read through GL's box, an unknown unknown is a sentence phi with
(not box phi) and (not box not box phi) both true. Con(T) = not box bottom is one:
true in the standard model, T cannot prove it (Goedel II), and T cannot prove that it
cannot (else T would prove Con(T), since box bottom implies box phi for every phi).
This holds for every consistent, sound theory the logic applies to, including any
theory an agent could hold of itself. It says nothing about any particular agent's access.
"""
import unittest

from hyperlogic.provability import (box, conj, countermodel, neg, prove,
                                    true_in_arithmetic)

BOT = ("bot",)
CON = neg(box(BOT))


def unknown_unknown(phi):
    return conj(neg(box(phi)), neg(box(neg(box(phi)))))


class UnknownUnknownTests(unittest.TestCase):
    def test_con_is_true_but_not_proved(self):
        self.assertTrue(true_in_arithmetic(CON))
        self.assertFalse(prove(CON))

    def test_theory_cannot_prove_that_it_cannot_prove_con(self):
        self.assertFalse(prove(neg(box(neg(box(CON))))))
        self.assertIsNotNone(countermodel(neg(box(neg(box(CON))))))

    def test_con_is_an_unknown_unknown_true_in_the_standard_model(self):
        self.assertTrue(true_in_arithmetic(unknown_unknown(CON)))
        self.assertFalse(prove(neg(unknown_unknown(CON))))

    def test_negative_control_a_theorem_is_not_an_unknown_unknown(self):
        theorem = neg(BOT)  # provable in GL: not bottom
        self.assertTrue(prove(theorem))
        self.assertFalse(prove(neg(box(theorem))))  # box of a theorem is provable
        self.assertTrue(prove(box(theorem)))


if __name__ == "__main__":
    unittest.main()
