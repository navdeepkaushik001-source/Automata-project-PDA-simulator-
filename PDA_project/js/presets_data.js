/**
 * Pre-defined Pushdown Automata presets for CSET302 Simulator
 */
const PRESETS = {
  "an_bn": {
    "name": "L = { a^n b^n | n >= 1 } (Final State)",
    "description": "Standard deterministic PDA recognizing strings with equal number of 'a's followed by equal 'b's.",
    "states": ["q0", "q1", "q2"],
    "input_alphabet": ["a", "b"],
    "stack_alphabet": ["A", "Z0"],
    "start_state": "q0",
    "start_stack_symbol": "Z0",
    "final_states": ["q2"],
    "acceptance_mode": "final_state",
    "sample_accepted": ["ab", "aabb", "aaabbb", "aaaabbbb"],
    "sample_rejected": ["", "a", "b", "aab", "abb", "ba", "aabba"],
    "transitions": [
      { "from_state": "q0", "input_symbol": "a", "pop_symbol": "Z0", "to_state": "q0", "push_symbols": "AZ0" },
      { "from_state": "q0", "input_symbol": "a", "pop_symbol": "A",  "to_state": "q0", "push_symbols": "AA" },
      { "from_state": "q0", "input_symbol": "b", "pop_symbol": "A",  "to_state": "q1", "push_symbols": "ε" },
      { "from_state": "q1", "input_symbol": "b", "pop_symbol": "A",  "to_state": "q1", "push_symbols": "ε" },
      { "from_state": "q1", "input_symbol": "ε", "pop_symbol": "Z0", "to_state": "q2", "push_symbols": "Z0" }
    ]
  },
  "an_bn_empty": {
    "name": "L = { a^n b^n | n >= 1 } (Empty Stack)",
    "description": "Acceptance by empty stack. Note that F = {} and Z0 is popped on epsilon at the end.",
    "states": ["q0", "q1"],
    "input_alphabet": ["a", "b"],
    "stack_alphabet": ["A", "Z0"],
    "start_state": "q0",
    "start_stack_symbol": "Z0",
    "final_states": [],
    "acceptance_mode": "empty_stack",
    "sample_accepted": ["ab", "aabb", "aaabbb"],
    "sample_rejected": ["", "a", "b", "abb", "aab", "ba"],
    "transitions": [
      { "from_state": "q0", "input_symbol": "a", "pop_symbol": "Z0", "to_state": "q0", "push_symbols": "AZ0" },
      { "from_state": "q0", "input_symbol": "a", "pop_symbol": "A",  "to_state": "q0", "push_symbols": "AA" },
      { "from_state": "q0", "input_symbol": "b", "pop_symbol": "A",  "to_state": "q1", "push_symbols": "ε" },
      { "from_state": "q1", "input_symbol": "b", "pop_symbol": "A",  "to_state": "q1", "push_symbols": "ε" },
      { "from_state": "q1", "input_symbol": "ε", "pop_symbol": "Z0", "to_state": "q1", "push_symbols": "ε" }
    ]
  },
  "odd_palindrome": {
    "name": "L = { w c w^R | w in {a,b}* } (Odd Palindrome)",
    "description": "Deterministic PDA where 'c' is the unmistakable middle pivot marker.",
    "states": ["q0", "q1", "q2"],
    "input_alphabet": ["a", "b", "c"],
    "stack_alphabet": ["A", "B", "Z0"],
    "start_state": "q0",
    "start_stack_symbol": "Z0",
    "final_states": ["q2"],
    "acceptance_mode": "final_state",
    "sample_accepted": ["c", "aca", "bcb", "abcba", "baacaab", "abbcbba"],
    "sample_rejected": ["", "a", "b", "cc", "acb", "abccba", "abcb", "baacabb"],
    "transitions": [
      { "from_state": "q0", "input_symbol": "a", "pop_symbol": "Z0", "to_state": "q0", "push_symbols": "AZ0" },
      { "from_state": "q0", "input_symbol": "a", "pop_symbol": "A",  "to_state": "q0", "push_symbols": "AA" },
      { "from_state": "q0", "input_symbol": "a", "pop_symbol": "B",  "to_state": "q0", "push_symbols": "AB" },
      { "from_state": "q0", "input_symbol": "b", "pop_symbol": "Z0", "to_state": "q0", "push_symbols": "BZ0" },
      { "from_state": "q0", "input_symbol": "b", "pop_symbol": "A",  "to_state": "q0", "push_symbols": "BA" },
      { "from_state": "q0", "input_symbol": "b", "pop_symbol": "B",  "to_state": "q0", "push_symbols": "BB" },

      { "from_state": "q0", "input_symbol": "c", "pop_symbol": "Z0", "to_state": "q1", "push_symbols": "Z0" },
      { "from_state": "q0", "input_symbol": "c", "pop_symbol": "A",  "to_state": "q1", "push_symbols": "A" },
      { "from_state": "q0", "input_symbol": "c", "pop_symbol": "B",  "to_state": "q1", "push_symbols": "B" },

      { "from_state": "q1", "input_symbol": "a", "pop_symbol": "A",  "to_state": "q1", "push_symbols": "ε" },
      { "from_state": "q1", "input_symbol": "b", "pop_symbol": "B",  "to_state": "q1", "push_symbols": "ε" },
      { "from_state": "q1", "input_symbol": "ε", "pop_symbol": "Z0", "to_state": "q2", "push_symbols": "Z0" }
    ]
  },
  "even_palindrome": {
    "name": "L = { w w^R | w in {a,b}* } (Even Palindrome - NPDA)",
    "description": "Nondeterministic PDA that guesses the middle of the string via epsilon-transition.",
    "states": ["q0", "q1", "q2"],
    "input_alphabet": ["a", "b"],
    "stack_alphabet": ["A", "B", "Z0"],
    "start_state": "q0",
    "start_stack_symbol": "Z0",
    "final_states": ["q2"],
    "acceptance_mode": "final_state",
    "sample_accepted": ["", "aa", "bb", "abba", "baab", "aabbaa", "ababbaba"],
    "sample_rejected": ["a", "b", "ab", "ba", "aba", "bab", "abbb", "aab"],
    "transitions": [
      { "from_state": "q0", "input_symbol": "a", "pop_symbol": "Z0", "to_state": "q0", "push_symbols": "AZ0" },
      { "from_state": "q0", "input_symbol": "a", "pop_symbol": "A",  "to_state": "q0", "push_symbols": "AA" },
      { "from_state": "q0", "input_symbol": "a", "pop_symbol": "B",  "to_state": "q0", "push_symbols": "AB" },
      { "from_state": "q0", "input_symbol": "b", "pop_symbol": "Z0", "to_state": "q0", "push_symbols": "BZ0" },
      { "from_state": "q0", "input_symbol": "b", "pop_symbol": "A",  "to_state": "q0", "push_symbols": "BA" },
      { "from_state": "q0", "input_symbol": "b", "pop_symbol": "B",  "to_state": "q0", "push_symbols": "BB" },

      { "from_state": "q0", "input_symbol": "ε", "pop_symbol": "Z0", "to_state": "q1", "push_symbols": "Z0" },
      { "from_state": "q0", "input_symbol": "ε", "pop_symbol": "A",  "to_state": "q1", "push_symbols": "A" },
      { "from_state": "q0", "input_symbol": "ε", "pop_symbol": "B",  "to_state": "q1", "push_symbols": "B" },

      { "from_state": "q1", "input_symbol": "a", "pop_symbol": "A",  "to_state": "q1", "push_symbols": "ε" },
      { "from_state": "q1", "input_symbol": "b", "pop_symbol": "B",  "to_state": "q1", "push_symbols": "ε" },
      { "from_state": "q1", "input_symbol": "ε", "pop_symbol": "Z0", "to_state": "q2", "push_symbols": "Z0" }
    ]
  },
  "balanced_parentheses": {
    "name": "Balanced Parentheses & Brackets () []",
    "description": "Validates matched and properly nested () and [].",
    "states": ["q0", "q1"],
    "input_alphabet": ["(", ")", "[", "]"],
    "stack_alphabet": ["P", "B", "Z0"],
    "start_state": "q0",
    "start_stack_symbol": "Z0",
    "final_states": ["q1"],
    "acceptance_mode": "final_state",
    "sample_accepted": ["", "()", "[]", "([])", "()[]", "[()]", "([()][])"],
    "sample_rejected": ["(", ")", "[", "]", "([)]", "(()", "())", "[(])"],
    "transitions": [
      { "from_state": "q0", "input_symbol": "(", "pop_symbol": "Z0", "to_state": "q0", "push_symbols": "PZ0" },
      { "from_state": "q0", "input_symbol": "(", "pop_symbol": "P",  "to_state": "q0", "push_symbols": "PP" },
      { "from_state": "q0", "input_symbol": "(", "pop_symbol": "B",  "to_state": "q0", "push_symbols": "PB" },

      { "from_state": "q0", "input_symbol": "[", "pop_symbol": "Z0", "to_state": "q0", "push_symbols": "BZ0" },
      { "from_state": "q0", "input_symbol": "[", "pop_symbol": "P",  "to_state": "q0", "push_symbols": "BP" },
      { "from_state": "q0", "input_symbol": "[", "pop_symbol": "B",  "to_state": "q0", "push_symbols": "BB" },

      { "from_state": "q0", "input_symbol": ")", "pop_symbol": "P",  "to_state": "q0", "push_symbols": "ε" },
      { "from_state": "q0", "input_symbol": "]", "pop_symbol": "B",  "to_state": "q0", "push_symbols": "ε" },

      { "from_state": "q0", "input_symbol": "ε", "pop_symbol": "Z0", "to_state": "q1", "push_symbols": "Z0" }
    ]
  },
  "equal_a_b": {
    "name": "L = { w in {a,b}* | n_a(w) = n_b(w) }",
    "description": "Equal count of 'a' and 'b' in arbitrary intermixed orders.",
    "states": ["q0", "q_acc"],
    "input_alphabet": ["a", "b"],
    "stack_alphabet": ["A", "B", "Z0"],
    "start_state": "q0",
    "start_stack_symbol": "Z0",
    "final_states": ["q_acc"],
    "acceptance_mode": "final_state",
    "sample_accepted": ["", "ab", "ba", "aabb", "baba", "abba", "baab", "ababbaba"],
    "sample_rejected": ["a", "b", "aab", "abb", "aaabb", "bbba"],
    "transitions": [
      { "from_state": "q0", "input_symbol": "a", "pop_symbol": "Z0", "to_state": "q0", "push_symbols": "AZ0" },
      { "from_state": "q0", "input_symbol": "a", "pop_symbol": "A",  "to_state": "q0", "push_symbols": "AA" },
      { "from_state": "q0", "input_symbol": "a", "pop_symbol": "B",  "to_state": "q0", "push_symbols": "ε" },

      { "from_state": "q0", "input_symbol": "b", "pop_symbol": "Z0", "to_state": "q0", "push_symbols": "BZ0" },
      { "from_state": "q0", "input_symbol": "b", "pop_symbol": "B",  "to_state": "q0", "push_symbols": "BB" },
      { "from_state": "q0", "input_symbol": "b", "pop_symbol": "A",  "to_state": "q0", "push_symbols": "ε" },

      { "from_state": "q0", "input_symbol": "ε", "pop_symbol": "Z0", "to_state": "q_acc", "push_symbols": "Z0" }
    ]
  },
  "an_b2n": {
    "name": "L = { a^n b^2n | n >= 1 }",
    "description": "Two 'b's for every 'a'. Pushes AA for each a, pops one A for each b.",
    "states": ["q0", "q1", "q2"],
    "input_alphabet": ["a", "b"],
    "stack_alphabet": ["A", "Z0"],
    "start_state": "q0",
    "start_stack_symbol": "Z0",
    "final_states": ["q2"],
    "acceptance_mode": "final_state",
    "sample_accepted": ["abb", "aabbbb", "aaabbbbbb"],
    "sample_rejected": ["", "ab", "abbb", "aab", "aabb"],
    "transitions": [
      { "from_state": "q0", "input_symbol": "a", "pop_symbol": "Z0", "to_state": "q0", "push_symbols": "AAZ0" },
      { "from_state": "q0", "input_symbol": "a", "pop_symbol": "A",  "to_state": "q0", "push_symbols": "AAA" },
      { "from_state": "q0", "input_symbol": "b", "pop_symbol": "A",  "to_state": "q1", "push_symbols": "ε" },
      { "from_state": "q1", "input_symbol": "b", "pop_symbol": "A",  "to_state": "q1", "push_symbols": "ε" },
      { "from_state": "q1", "input_symbol": "ε", "pop_symbol": "Z0", "to_state": "q2", "push_symbols": "Z0" }
    ]
  }
};
