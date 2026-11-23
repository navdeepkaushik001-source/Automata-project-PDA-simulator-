#!/usr/bin/env python3
"""
Command Line Interface (CLI) for Pushdown Automata Simulator
Course: CSET302 - Automata Theory and Computability
Topic: Pushdown Automata Simulator (#12)
"""

import argparse
import json
import os
import sys

from src.pda_engine import PushdownAutomaton, AcceptanceMode, EPSILON

def print_header(title: str):
    print("\n" + "=" * 65)
    print(f" {title.center(63)} ")
    print("=" * 65)

def format_trace_table(trace):
    lines = []
    header = f"{'Step':<5} | {'State':<7} | {'Remaining Input':<18} | {'Stack (Top->Bottom)':<20} | {'Action / Rule Applied'}"
    sep = "-" * len(header)
    lines.append(sep)
    lines.append(header)
    lines.append(sep)

    for item in trace:
        step = str(item["step"])
        st = item["state"]
        rem = item["remaining_input"] if item["remaining_input"] else EPSILON
        stk = "".join(item["stack"]) if item["stack"] else EPSILON
        act = item["action"]
        lines.append(f"{step:<5} | {st:<7} | {rem:<18} | {stk:<20} | {act}")

    lines.append(sep)
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(
        description="Pushdown Automata (PDA) Simulator - CSET302 Project"
    )
    parser.add_argument(
        "--preset",
        "-p",
        type=str,
        default="presets/an_bn.json",
        help="Path to PDA configuration JSON file (default: presets/an_bn.json)",
    )
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        help="Input string to simulate (e.g. 'aaabbb')",
    )
    parser.add_argument(
        "--batch",
        "-b",
        nargs="+",
        help="Batch test multiple strings (e.g. --batch ab aabb aab abb)",
    )
    parser.add_argument(
        "--export-trace",
        type=str,
        help="Export trace table to a text file",
    )
    parser.add_argument(
        "--info",
        action="store_true",
        help="Display formal 7-tuple specification of the PDA",
    )

    args = parser.parse_args()

    # Load PDA configuration
    if not os.path.exists(args.preset):
        print(f"Error: PDA file '{args.preset}' not found.")
        sys.exit(1)

    with open(args.preset, "r", encoding="utf-8") as f:
        data = json.load(f)

    pda = PushdownAutomaton.from_dict(data)

    print_header(f"CSET302 PDA Simulator: {pda.name}")
    print(f"Description: {pda.description}")
    print(f"Type: {'Deterministic (DPDA)' if pda.is_deterministic() else 'Nondeterministic (NPDA)'}")
    print(f"Acceptance Mode: {pda.acceptance_mode.value.replace('_', ' ').title()}")

    if args.info or (not args.input and not args.batch):
        print("\n--- Formal 7-Tuple Specification M = (Q, Σ, Γ, δ, q0, Z0, F) ---")
        print(f"  Q     (States)             : {{{', '.join(pda.states)}}}")
        print(f"  Σ     (Input Alphabet)     : {{{', '.join(pda.input_alphabet)}}}")
        print(f"  Γ     (Stack Alphabet)     : {{{', '.join(pda.stack_alphabet)}}}")
        print(f"  q0    (Start State)        : {pda.start_state}")
        print(f"  Z0    (Start Stack Symbol) : {pda.start_stack_symbol}")
        print(f"  F     (Final States)       : {{{', '.join(pda.final_states)}}}")
        print("\n  δ (Transition Function):")
        for i, t in enumerate(pda.transitions, 1):
            push_str = t.push_symbols if t.push_symbols else EPSILON
            print(f"    {i:2d}. δ({t.from_state}, {t.input_symbol}, {t.pop_symbol}) -> ({t.to_state}, {push_str})")

    if args.batch:
        print_header("Batch Validation Results")
        print(f"{'Input String':<15} | {'Result':<10} | {'Steps':<6} | {'Reason'}")
        print("-" * 65)
        for s in args.batch:
            res = pda.simulate(s)
            status = "ACCEPTED" if res.accepted else "REJECTED"
            reason = res.acceptance_reason[:35] + ("..." if len(res.acceptance_reason) > 35 else "")
            print(f"'{s}':<15 | {status:<10} | {res.total_steps:<6} | {reason}")
        print("-" * 65)

    if args.input is not None:
        input_str = args.input
        print_header(f"Simulating Input String: '{input_str}'")
        res = pda.simulate(input_str)

        trace_data = [step.to_dict() for step in res.execution_path]
        print(format_trace_table(trace_data))

        print(f"\nFinal Verdict: {'>>> ACCEPTED <<<' if res.accepted else '>>> REJECTED <<<'}")
        print(f"Reason: {res.acceptance_reason}")
        print(f"Total Steps: {res.total_steps}")
        print(f"Branches Explored: {res.branch_count}")

        if args.export_trace:
            with open(args.export_trace, "w", encoding="utf-8") as out_f:
                out_f.write(f"PDA Simulation Trace: {pda.name}\n")
                out_f.write(f"Input: '{input_str}'\n")
                out_f.write(f"Result: {'ACCEPTED' if res.accepted else 'REJECTED'}\n")
                out_f.write(f"Reason: {res.acceptance_reason}\n\n")
                out_f.write(format_trace_table(trace_data))
            print(f"\n[Saved trace table to '{args.export_trace}']")

if __name__ == "__main__":
    main()
