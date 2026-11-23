"""
Pushdown Automata (PDA) Engine
Course: CSET302 - Automata Theory and Computability
Topic: Pushdown Automata Simulator (#12)

Formal Definition:
A Pushdown Automaton is a 7-tuple: M = (Q, Sigma, Gamma, delta, q0, Z0, F)
where:
  Q     : Finite set of states
  Sigma : Finite input alphabet
  Gamma : Finite stack alphabet
  delta : Transition function: Q x (Sigma U {eps}) x Gamma -> P_finite(Q x Gamma*)
  q0    : Initial state (q0 in Q)
  Z0    : Initial stack symbol (Z0 in Gamma)
  F     : Set of final/accepting states (F subset of Q)
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Any, Union
import json
import collections

EPSILON = "ε"
LAMBDA = "λ"

def is_epsilon(sym: str) -> bool:
    return sym in ("", EPSILON, LAMBDA, "eps", "epsilon")

def tokenize_symbols(text: Union[str, List[str]], alphabet: List[str]) -> Tuple[str, ...]:
    """Tokenize a push sequence into stack alphabet symbols."""
    if isinstance(text, list):
        return tuple(s for s in text if not is_epsilon(s))
    if not text or is_epsilon(text):
        return ()
    sorted_alpha = sorted(alphabet, key=len, reverse=True)
    tokens: List[str] = []
    i = 0
    while i < len(text):
        matched = False
        for sym in sorted_alpha:
            if sym and text.startswith(sym, i):
                tokens.append(sym)
                i += len(sym)
                matched = True
                break
        if not matched:
            tokens.append(text[i])
            i += 1
    return tuple(tokens)

class AcceptanceMode(Enum):
    FINAL_STATE = "final_state"
    EMPTY_STACK = "empty_stack"
    BOTH = "both"

@dataclass(frozen=True)
class Transition:
    from_state: str
    input_symbol: str          # character or EPSILON
    pop_symbol: str            # stack symbol to pop
    to_state: str
    push_symbols: str          # string of symbols or EPSILON for pure pop

    def to_dict(self) -> Dict[str, str]:
        return {
            "from_state": self.from_state,
            "input_symbol": self.input_symbol,
            "pop_symbol": self.pop_symbol,
            "to_state": self.to_state,
            "push_symbols": self.push_symbols
        }

@dataclass
class InstantaneousDescription:
    """
    Instantaneous Description (ID) represents the configuration (q, w, gamma)
    q: current state
    w: remaining input string
    gamma: stack content from top to bottom (gamma[0] is top)
    """
    state: str
    remaining_input: str
    stack: Tuple[str, ...]
    step_number: int = 0
    transition_used: Optional[Transition] = None
    input_consumed: str = ""
    action_description: str = ""

    @property
    def id_string(self) -> str:
        w_disp = self.remaining_input if self.remaining_input else EPSILON
        gamma_disp = "".join(self.stack) if self.stack else EPSILON
        return f"({self.state}, {w_disp}, {gamma_disp})"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step": self.step_number,
            "state": self.state,
            "remaining_input": self.remaining_input,
            "input_consumed": self.input_consumed,
            "stack": list(self.stack),
            "stack_string": "".join(self.stack),
            "id_string": self.id_string,
            "action": self.action_description,
            "transition": self.transition_used.to_dict() if self.transition_used else None
        }

@dataclass
class SimulationResult:
    accepted: bool
    acceptance_reason: str
    execution_path: List[InstantaneousDescription]
    total_steps: int
    is_deterministic: bool
    branch_count: int = 1
    rejected_branches: int = 0
    message: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "accepted": self.accepted,
            "reason": self.acceptance_reason,
            "total_steps": self.total_steps,
            "is_deterministic": self.is_deterministic,
            "branch_count": self.branch_count,
            "rejected_branches": self.rejected_branches,
            "message": self.message,
            "trace": [step.to_dict() for step in self.execution_path]
        }

class PushdownAutomaton:
    def __init__(
        self,
        name: str = "Pushdown Automaton",
        description: str = "",
        states: Optional[List[str]] = None,
        input_alphabet: Optional[List[str]] = None,
        stack_alphabet: Optional[List[str]] = None,
        transitions: Optional[List[Transition]] = None,
        start_state: str = "q0",
        start_stack_symbol: str = "Z0",
        final_states: Optional[List[str]] = None,
        acceptance_mode: AcceptanceMode = AcceptanceMode.FINAL_STATE,
    ):
        self.name = name
        self.description = description
        self.states = sorted(list(set(states or [])))
        self.input_alphabet = sorted(list(set(input_alphabet or [])))
        self.stack_alphabet = sorted(list(set(stack_alphabet or [])))
        self.transitions: List[Transition] = transitions or []
        self.start_state = start_state
        self.start_stack_symbol = start_stack_symbol
        self.final_states = sorted(list(set(final_states or [])))
        self.acceptance_mode = acceptance_mode

        # Fast lookup mapping: (from_state, input_symbol, pop_symbol) -> list of (to_state, push_tokens, Transition)
        self._build_transition_index()

    def _normalize_input_sym(self, sym: str) -> str:
        if is_epsilon(sym):
            return EPSILON
        return sym

    def _build_transition_index(self):
        self._transition_map: Dict[Tuple[str, str, str], List[Tuple[str, Tuple[str, ...], Transition]]] = collections.defaultdict(list)
        for t in self.transitions:
            inp = self._normalize_input_sym(t.input_symbol)
            push_tokens = tokenize_symbols(t.push_symbols, self.stack_alphabet)
            self._transition_map[(t.from_state, inp, t.pop_symbol)].append(
                (t.to_state, push_tokens, t)
            )

    def is_deterministic(self) -> bool:
        """
        A PDA is deterministic (DPDA) iff for every state q, input a in Sigma U {eps}, and top of stack X in Gamma:
        1. |delta(q, a, X)| <= 1
        2. If delta(q, eps, X) is non-empty, then delta(q, a, X) must be empty for all a in Sigma.
        """
        for q in self.states:
            for x in self.stack_alphabet:
                eps_transitions = self._transition_map.get((q, EPSILON, x), [])
                if len(eps_transitions) > 1:
                    return False
                has_eps = len(eps_transitions) == 1

                for a in self.input_alphabet:
                    inp_transitions = self._transition_map.get((q, a, x), [])
                    if len(inp_transitions) > 1:
                        return False
                    if has_eps and len(inp_transitions) > 0:
                        return False
        return True

    def validate_definition(self) -> List[str]:
        """Validate PDA 7-tuple integrity and return list of errors if any."""
        errors = []
        if self.start_state not in self.states:
            errors.append(f"Start state '{self.start_state}' is not in Q ({self.states}).")
        if self.start_stack_symbol not in self.stack_alphabet:
            errors.append(f"Initial stack symbol '{self.start_stack_symbol}' is not in Gamma ({self.stack_alphabet}).")
        for f in self.final_states:
            if f not in self.states:
                errors.append(f"Final state '{f}' is not in Q ({self.states}).")

        for i, t in enumerate(self.transitions):
            if t.from_state not in self.states:
                errors.append(f"Transition #{i+1} from_state '{t.from_state}' not in Q.")
            if t.to_state not in self.states:
                errors.append(f"Transition #{i+1} to_state '{t.to_state}' not in Q.")
            if not is_epsilon(t.input_symbol) and t.input_symbol not in self.input_alphabet:
                errors.append(f"Transition #{i+1} input '{t.input_symbol}' not in Sigma.")
            if t.pop_symbol not in self.stack_alphabet:
                errors.append(f"Transition #{i+1} pop '{t.pop_symbol}' not in Gamma.")
            tokens = tokenize_symbols(t.push_symbols, self.stack_alphabet)
            for ch in tokens:
                if ch not in self.stack_alphabet:
                    errors.append(f"Transition #{i+1} push symbol '{ch}' not in Gamma.")
        return errors

    def _is_accepted_configuration(self, state: str, remaining_input: str, stack: Tuple[str, ...]) -> Tuple[bool, str]:
        """Check if a configuration satisfies the acceptance condition."""
        if remaining_input != "":
            return False, "Input not completely consumed."

        if self.acceptance_mode == AcceptanceMode.FINAL_STATE:
            if state in self.final_states:
                return True, f"Input exhausted and current state '{state}' is an accepting final state."
            return False, f"Input exhausted but state '{state}' is not in final states {self.final_states}."

        elif self.acceptance_mode == AcceptanceMode.EMPTY_STACK:
            if len(stack) == 0:
                return True, "Input exhausted and stack is completely empty."
            return False, f"Input exhausted but stack is not empty (stack={''.join(stack)})."

        elif self.acceptance_mode == AcceptanceMode.BOTH:
            if state in self.final_states and len(stack) == 0:
                return True, f"Input exhausted, state '{state}' is final, and stack is empty."
            return False, f"Requires both final state and empty stack (state={state}, stack={''.join(stack)})."

        return False, "Unknown acceptance mode."

    def simulate(self, input_string: str, max_steps: int = 1500) -> SimulationResult:
        """
        Simulate the PDA on the given input string using Breadth-First Search (BFS)
        to handle both Deterministic and Non-Deterministic PDAs.
        Finds the shortest accepting computation path if one exists.
        """
        # Validate input symbols against alphabet
        for char in input_string:
            if char not in self.input_alphabet:
                return SimulationResult(
                    accepted=False,
                    acceptance_reason=f"Symbol '{char}' in input is not part of input alphabet Sigma {self.input_alphabet}",
                    execution_path=[],
                    total_steps=0,
                    is_deterministic=self.is_deterministic(),
                    message=f"Alphabet violation: '{char}'"
                )

        initial_stack = (self.start_stack_symbol,) if self.start_stack_symbol else ()
        initial_id = InstantaneousDescription(
            state=self.start_state,
            remaining_input=input_string,
            stack=initial_stack,
            step_number=0,
            action_description="Initial configuration"
        )

        # Check immediate acceptance for empty string
        is_acc, reason = self._is_accepted_configuration(
            self.start_state, input_string, initial_stack
        )
        if is_acc:
            return SimulationResult(
                accepted=True,
                acceptance_reason=reason,
                execution_path=[initial_id],
                total_steps=0,
                is_deterministic=self.is_deterministic(),
                message="Accepted at initial configuration."
            )

        # Queue item: (current_id, history_list)
        queue = collections.deque([(initial_id, [initial_id])])
        visited: Set[Tuple[str, str, Tuple[str, ...]]] = set()
        visited.add((initial_id.state, initial_id.remaining_input, initial_id.stack))

        total_nodes_explored = 0
        longest_rejected_path: List[InstantaneousDescription] = [initial_id]
        rejected_branches = 0

        while queue:
            total_nodes_explored += 1
            curr_id, path = queue.popleft()

            if len(path) > len(longest_rejected_path):
                longest_rejected_path = path

            if total_nodes_explored > max_steps:
                return SimulationResult(
                    accepted=False,
                    acceptance_reason=f"Simulation step limit ({max_steps}) exceeded. Possible non-terminating branch.",
                    execution_path=longest_rejected_path,
                    total_steps=len(longest_rejected_path) - 1,
                    is_deterministic=self.is_deterministic(),
                    branch_count=total_nodes_explored,
                    message="Computation step limit reached."
                )

            # Check if current configuration is accepted
            is_acc, reason = self._is_accepted_configuration(
                curr_id.state, curr_id.remaining_input, curr_id.stack
            )
            if is_acc:
                return SimulationResult(
                    accepted=True,
                    acceptance_reason=reason,
                    execution_path=path,
                    total_steps=len(path) - 1,
                    is_deterministic=self.is_deterministic(),
                    branch_count=total_nodes_explored,
                    rejected_branches=rejected_branches,
                    message="Input accepted by PDA."
                )

            # To apply a transition, stack must not be empty
            if not curr_id.stack:
                rejected_branches += 1
                continue

            top_stack = curr_id.stack[0]
            rest_stack = curr_id.stack[1:]
            possible_moves: List[Tuple[str, Tuple[str, ...], Transition, bool]] = []

            # 1. Epsilon transitions: delta(state, eps, top_stack)
            for to_state, push_tokens, t in self._transition_map.get((curr_id.state, EPSILON, top_stack), []):
                possible_moves.append((to_state, push_tokens, t, True))

            # 2. Input consuming transitions: delta(state, curr_char, top_stack)
            if curr_id.remaining_input:
                curr_char = curr_id.remaining_input[0]
                for to_state, push_tokens, t in self._transition_map.get((curr_id.state, curr_char, top_stack), []):
                    possible_moves.append((to_state, push_tokens, t, False))

            if not possible_moves:
                rejected_branches += 1
                continue

            for to_state, push_tokens, trans, is_eps in possible_moves:
                if is_eps:
                    new_remaining = curr_id.remaining_input
                    consumed_char = EPSILON
                    action_txt = f"Epsilon move: pop '{top_stack}', push '{''.join(push_tokens) or EPSILON}' -> state {to_state}"
                else:
                    new_remaining = curr_id.remaining_input[1:]
                    consumed_char = curr_id.remaining_input[0]
                    action_txt = f"Read '{consumed_char}': pop '{top_stack}', push '{''.join(push_tokens) or EPSILON}' -> state {to_state}"

                new_stack = push_tokens + rest_stack

                state_signature = (to_state, new_remaining, new_stack)
                # Cycle prevention on configuration state
                if state_signature in visited:
                    continue
                visited.add(state_signature)

                next_id = InstantaneousDescription(
                    state=to_state,
                    remaining_input=new_remaining,
                    stack=new_stack,
                    step_number=len(path),
                    transition_used=trans,
                    input_consumed=consumed_char,
                    action_description=action_txt
                )

                # Check if this move directly accepts
                is_acc_next, reason_next = self._is_accepted_configuration(
                    to_state, new_remaining, new_stack
                )
                if is_acc_next:
                    return SimulationResult(
                        accepted=True,
                        acceptance_reason=reason_next,
                        execution_path=path + [next_id],
                        total_steps=len(path),
                        is_deterministic=self.is_deterministic(),
                        branch_count=total_nodes_explored,
                        rejected_branches=rejected_branches,
                        message="Input accepted by PDA."
                    )

                queue.append((next_id, path + [next_id]))

        # If queue exhausts without finding an accepting path
        last_step = longest_rejected_path[-1]
        if last_step.remaining_input:
            next_ch = last_step.remaining_input[0]
            top_sym = last_step.stack[0] if last_step.stack else EPSILON
            reason_msg = (
                f"No transition defined for state '{last_step.state}' with input symbol '{next_ch}' "
                f"and stack top '{top_sym}'. Automaton halted at step {last_step.step_number}. Input rejected."
            )
            if len(longest_rejected_path) == 1 and longest_rejected_path[0].action_description == "Initial configuration":
                longest_rejected_path[0].action_description = f"Halted immediately: no rule δ({last_step.state}, {next_ch}, {top_sym})"
        else:
            top_str = "".join(last_step.stack) if last_step.stack else EPSILON
            if self.acceptance_mode == AcceptanceMode.FINAL_STATE:
                reason_msg = f"Input exhausted, but halted in non-accepting state '{last_step.state}' (Final states: {self.final_states}). Input rejected."
            elif self.acceptance_mode == AcceptanceMode.EMPTY_STACK:
                reason_msg = f"Input exhausted, but stack is not empty (Stack: '{top_str}'). Input rejected."
            else:
                reason_msg = f"Input exhausted, but requires both final state and empty stack (State: '{last_step.state}', Stack: '{top_str}'). Input rejected."

        return SimulationResult(
            accepted=False,
            acceptance_reason=reason_msg,
            execution_path=longest_rejected_path,
            total_steps=len(longest_rejected_path) - 1,
            is_deterministic=self.is_deterministic(),
            branch_count=total_nodes_explored,
            rejected_branches=rejected_branches,
            message="Input rejected by PDA."
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "states": self.states,
            "input_alphabet": self.input_alphabet,
            "stack_alphabet": self.stack_alphabet,
            "start_state": self.start_state,
            "start_stack_symbol": self.start_stack_symbol,
            "final_states": self.final_states,
            "acceptance_mode": self.acceptance_mode.value,
            "is_deterministic": self.is_deterministic(),
            "transitions": [t.to_dict() for t in self.transitions]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PushdownAutomaton":
        transitions = [
            Transition(
                from_state=t["from_state"],
                input_symbol=t["input_symbol"],
                pop_symbol=t["pop_symbol"],
                to_state=t["to_state"],
                push_symbols=t["push_symbols"]
            )
            for t in data.get("transitions", [])
        ]
        acc_mode = AcceptanceMode(data.get("acceptance_mode", "final_state"))
        return cls(
            name=data.get("name", "PDA"),
            description=data.get("description", ""),
            states=data.get("states", []),
            input_alphabet=data.get("input_alphabet", []),
            stack_alphabet=data.get("stack_alphabet", []),
            transitions=transitions,
            start_state=data.get("start_state", "q0"),
            start_stack_symbol=data.get("start_stack_symbol", "Z0"),
            final_states=data.get("final_states", []),
            acceptance_mode=acc_mode
        )
