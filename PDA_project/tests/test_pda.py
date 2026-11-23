"""
Comprehensive Unit Tests for Pushdown Automata (PDA) Engine
Validates normal cases, edge cases, DPDA, NPDA, acceptance by final state and empty stack.
"""

import unittest
import json
import os
import sys

# Ensure src is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from pda_engine import PushdownAutomaton, AcceptanceMode, Transition

PRESETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "presets"))

def load_preset(filename: str) -> PushdownAutomaton:
    path = os.path.join(PRESETS_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return PushdownAutomaton.from_dict(data)

class TestPDAEngine(unittest.TestCase):

    def test_an_bn_final_state(self):
        pda = load_preset("an_bn.json")
        self.assertTrue(pda.is_deterministic())

        # Accepted test cases
        for s in ["ab", "aabb", "aaabbb", "aaaabbbb"]:
            res = pda.simulate(s)
            self.assertTrue(res.accepted, f"Expected '{s}' to be accepted")
            self.assertEqual(res.execution_path[-1].state, "q2")

        # Rejected test cases
        for s in ["", "a", "b", "aab", "abb", "ba", "aabba", "bbaa"]:
            res = pda.simulate(s)
            self.assertFalse(res.accepted, f"Expected '{s}' to be rejected")

    def test_an_bn_empty_stack(self):
        pda = load_preset("an_bn_empty_stack.json")
        self.assertEqual(pda.acceptance_mode, AcceptanceMode.EMPTY_STACK)

        for s in ["ab", "aabb", "aaabbb"]:
            res = pda.simulate(s)
            self.assertTrue(res.accepted, f"Expected '{s}' to be accepted by empty stack")
            self.assertEqual(len(res.execution_path[-1].stack), 0)

        for s in ["", "a", "b", "abb", "aab", "ba"]:
            res = pda.simulate(s)
            self.assertFalse(res.accepted, f"Expected '{s}' to be rejected")

    def test_odd_palindrome(self):
        pda = load_preset("odd_palindrome.json")
        self.assertTrue(pda.is_deterministic())

        # Accepted: w c w^R
        for s in ["c", "aca", "bcb", "abcba", "abbcbba", "baacaab"]:
            res = pda.simulate(s)
            self.assertTrue(res.accepted, f"Expected '{s}' to be accepted")

        # Rejected
        for s in ["", "a", "b", "cc", "acb", "abccba", "abcb", "abcbaa", "baacabb"]:
            res = pda.simulate(s)
            self.assertFalse(res.accepted, f"Expected '{s}' to be rejected")

    def test_even_palindrome_npda(self):
        pda = load_preset("even_palindrome.json")
        self.assertFalse(pda.is_deterministic())  # NPDA

        # Accepted: w w^R
        for s in ["", "aa", "bb", "abba", "baab", "aabbaa", "ababbaba"]:
            res = pda.simulate(s)
            self.assertTrue(res.accepted, f"Expected '{s}' to be accepted by NPDA")

        # Rejected
        for s in ["a", "b", "ab", "ba", "aba", "bab", "abbb", "aab"]:
            res = pda.simulate(s)
            self.assertFalse(res.accepted, f"Expected '{s}' to be rejected")

    def test_balanced_parentheses(self):
        pda = load_preset("balanced_parentheses.json")
        # Note: PDA has an epsilon-transition on Z0 alongside input moves on Z0,
        # which makes it technically an NPDA according to formal theory.
        self.assertFalse(pda.is_deterministic())

        # Accepted
        for s in ["", "()", "[]", "([])", "()[]", "[()]", "([()][])"]:
            res = pda.simulate(s)
            self.assertTrue(res.accepted, f"Expected '{s}' to be accepted")

        # Rejected
        for s in ["(", ")", "[", "]", "([)]", "(()", "())", "[(])"]:
            res = pda.simulate(s)
            self.assertFalse(res.accepted, f"Expected '{s}' to be rejected")

    def test_equal_a_b(self):
        pda = load_preset("equal_a_b.json")

        # Accepted: equal count of a and b in any order
        for s in ["", "ab", "ba", "aabb", "baba", "abba", "baab", "ababbaba"]:
            res = pda.simulate(s)
            self.assertTrue(res.accepted, f"Expected '{s}' to be accepted")

        # Rejected: unequal counts
        for s in ["a", "b", "aab", "abb", "aaabb", "bbba"]:
            res = pda.simulate(s)
            self.assertFalse(res.accepted, f"Expected '{s}' to be rejected")

    def test_an_b2n(self):
        pda = load_preset("an_b2n.json")

        for s in ["abb", "aabbbb", "aaabbbbbb"]:
            res = pda.simulate(s)
            self.assertTrue(res.accepted, f"Expected '{s}' to be accepted")

        for s in ["", "ab", "abbb", "aab", "aabb"]:
            res = pda.simulate(s)
            self.assertFalse(res.accepted, f"Expected '{s}' to be rejected")

    def test_invalid_alphabet_symbol(self):
        pda = load_preset("an_bn.json")
        res = pda.simulate("abc")
        self.assertFalse(res.accepted)
        self.assertIn("not part of input alphabet", res.acceptance_reason)

if __name__ == "__main__":
    unittest.main()
