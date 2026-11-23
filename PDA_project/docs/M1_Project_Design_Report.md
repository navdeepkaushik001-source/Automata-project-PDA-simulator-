# Milestone 1 (M1) Project Design Report
## Course: CSET302 – Automata Theory and Computability
### Project Topic: #12 – Pushdown Automata (PDA) Simulator
**Evaluation Focus:** Problem Analysis & Project Design (5 Marks)

---

## 1. Problem Definition & Automata Specification (1 Mark)

### 1.1 Problem Statement & Objectives
In formal language and computability theory, Finite Automata (DFA/NFA) can only recognize Regular Languages because their memory is strictly finite (encoded purely in states). Context-Free Languages (CFLs)—such as balanced parentheses $\{ ( )^n \}$, arithmetic expressions, and palindrome languages $\{ w w^R \}$—require an auxiliary unbounded memory with Last-In-First-Out (LIFO) access.

The **Pushdown Automaton (PDA)** is the foundational theoretical computational model for CFLs and compiler syntax analysis. However, students and researchers frequently struggle with:
1. Tracking the dynamic push/pop operations of the stack alongside input reading.
2. Visualizing nondeterministic execution paths (NPDA branching) where the machine must guess configurations (e.g. palindrome midpoints).
3. Distinguishing between **Acceptance by Final State** ($L_f$) and **Acceptance by Empty Stack** ($L_e$).

**Project Objectives:**
- Design and implement a robust, interactive Pushdown Automata Simulator supporting both **Deterministic PDAs (DPDA)** and **Non-Deterministic PDAs (NPDA)**.
- Support both standard acceptance criteria: Final State and Empty Stack (as well as combined).
- Provide real-time graphical visualization of:
  - Input tape consumption and head movement.
  - Physical LIFO stack behavior with push/pop operations.
  - State transition graph with active node and transition arc illumination.
  - Instantaneous Descriptions (IDs): $(q, w, \gamma)$.
- Enable dynamic user input (arbitrary 7-tuples and transition tables) and automated validation against pre-loaded benchmark test suites.

---

### 1.2 Formal Automata Theoretical Specification
Formally, a Pushdown Automaton is defined as a 7-tuple:
$$M = (Q, \Sigma, \Gamma, \delta, q_0, Z_0, F)$$

Where:
1. **$Q$**: A finite, non-empty set of states.
2. **$\Sigma$**: A finite set of input alphabet symbols.
3. **$\Gamma$**: A finite set of stack alphabet symbols.
4. **$\delta$**: The transition function mapping:
   $$\delta: Q \times (\Sigma \cup \{\epsilon\}) \times \Gamma \to \mathcal{P}_{\text{finite}}(Q \times \Gamma^*)$$
   where $\epsilon$ denotes the empty string, and $\Gamma^*$ denotes any sequence of stack symbols (including $\epsilon$ for a pure pop).
5. **$q_0 \in Q$**: The initial/start state.
6. **$Z_0 \in \Gamma$**: The initial bottom-of-stack start symbol.
7. **$F \subseteq Q$**: The set of final (accepting) states.

#### Instantaneous Description (ID)
A configuration of $M$ at any instant is represented by a 3-tuple:
$$(q, w, \gamma) \in Q \times \Sigma^* \times \Gamma^*$$
- $q$: Current state.
- $w$: Unconsumed remaining input string.
- $\gamma$: Current stack contents written from top to bottom (the leftmost symbol of $\gamma$ is at the top of the stack).

A move is denoted by the relation $\vdash$:
$$(q, a w, X \beta) \vdash (p, w, \alpha \beta) \quad \text{if } (p, \alpha) \in \delta(q, a, X)$$
where $a \in \Sigma \cup \{\epsilon\}$, $X \in \Gamma$, and $\alpha, \beta \in \Gamma^*$.

#### Formal Acceptance Criteria
1. **Language Accepted by Final State ($L(M)$):**
   $$L(M) = \{ w \in \Sigma^* \mid (q_0, w, Z_0) \vdash^* (q, \epsilon, \gamma) \text{ for some } q \in F, \gamma \in \Gamma^* \}$$
2. **Language Accepted by Empty Stack ($N(M)$):**
   $$N(M) = \{ w \in \Sigma^* \mid (q_0, w, Z_0) \vdash^* (q, \epsilon, \epsilon) \text{ for some } q \in Q \}$$

---

## 2. Existing Tools Review & Feasibility Analysis (1 Mark)

### 2.1 Review of Existing Tools
| Existing Tool | Platform | Advantages | Key Limitations |
| :--- | :--- | :--- | :--- |
| **JFLAP (Java)** | Desktop Java Swing | Mature, widely used in academia, supports multi-tape machines. | Outdated UI; requires local Java Runtime (JRE); clunky stack display without real-time physical animation; does not easily export/import JSON; difficult web integration. |
| **Cyberzhg PDA Simulator** | Web (JavaScript) | Simple web accessibility. | Minimalist text-based interface; lacks animated physical stack visualizer; limited support for stepping backwards; no batch automated regression test suite. |
| **Automata-Simulator (GitHub)** | Python CLI | Good CLI scriptability. | No interactive GUI; lacks visual feedback on tape and stack heads; poor educational utility for novice students. |

### 2.2 Limitations Addressed by Our Proposed Simulator
1. **Zero-Install Web Architecture**: Runs natively in any modern web browser via clean HTML5/CSS3/JavaScript, plus an optional Python backend engine.
2. **Dual Representation**: Interactive graphical visualizer (SVG state graph, animated physical stack, tape reading head) coupled with a rigorous step-by-step Instantaneous Description log.
3. **NPDA Multi-Branch Exploration**: Solves nondeterministic branching using Breadth-First Search (BFS) with state-signature cycle detection, preventing infinite $\epsilon$-loops.
4. **Automated Batch Verification**: Includes 1-click regression testing on normal and edge cases with expected vs. actual validation matrices.

---

## 3. Simulator Design & Methodology (2 Marks)

### 3.1 System Architecture & Modules
The simulator follows a modular, decoupled Model-View-Controller (MVC) architecture:

```
+-------------------------------------------------------------------+
|                        PRESENTATION LAYER                         |
|  - HTML5 Responsive UI Grid                                       |
|  - Dynamic Form & Interactive Transition Table                    |
|  - Playback Controls (Play, Pause, Step Fwd/Back, Speed Slider)   |
+---------------------------------+---------------------------------+
                                  |
                                  v
+---------------------------------+---------------------------------+
|                        VISUALIZER LAYER                           |
|  - SVG State Diagram Generator (Node/Arc Layout & Glow Highlight) |
|  - Animated Vertical Stack Renderer (LIFO Push/Pop Animations)    |
|  - Tape Visualizer with Synchronized Head Position Indicator      |
|  - Trace Table & Instantaneous Description (ID) Formatter         |
+---------------------------------+---------------------------------+
                                  |
                                  v
+---------------------------------+---------------------------------+
|                       CORE AUTOMATA ENGINE                        |
|  - 7-Tuple Validator & Transition Indexer                         |
|  - Determinism Classifier (DPDA vs NPDA Check)                    |
|  - BFS Search & Path Finder (Cycle Detection & Depth Limiter)     |
|  - Dual Acceptance Evaluator (Final State vs Empty Stack)         |
+-------------------------------------------------------------------+
```

### 3.2 System Flowchart (IPO Workflow)

```
[ User Input: PDA 7-Tuple / Preset + Input String ]
                       |
                       v
       [ Validate 7-Tuple Definition ]
          /                        \
      (Errors)                   (Valid)
        /                            \
[ Show Validation Alert ]       [ Build Fast Transition Map ]
                                     |
                                     v
                        [ Determinism Evaluation ]
                         (Check |δ| and ε-moves)
                                     |
                                     v
                        [ BFS Execution Engine ]
                                     |
                +--------------------+--------------------+
                |                                         |
       (Deterministic Path)                    (Non-Deterministic BFS)
                |                                         |
                +--------------------+--------------------+
                                     |
                        [ Generate Full Trace & IDs ]
                                     |
                        [ Check Acceptance Mode ]
                        /                       \
              (Accepted Path)              (Rejected Path)
                     |                            |
       [ Status: ✓ ACCEPTED ]          [ Status: ✗ REJECTED ]
                     \                            /
             [ Update Tape, Stack, State Diagram & Trace Table ]
```

---

## 4. Algorithm Selection & Correctness (1 Mark)

### 4.1 Selected Algorithm: BFS Configuration Exploration
To correctly simulate both DPDA and NPDA without risking infinite loops caused by cyclic $\epsilon$-transitions, we employ a **Breadth-First Search (BFS)** algorithm over the configuration space.

#### Pseudocode
```
Algorithm: SimulatePDA(M, input_string, max_steps)
Input: 
  M = (Q, Sigma, Gamma, delta, q0, Z0, F), 
  input_string in Sigma*, 
  max_steps (default: 1500)
Output: 
  SimulationResult(accepted, execution_path, reason)

1.  Validate all characters of input_string against Sigma.
2.  initial_stack <- [Z0]
3.  initial_id <- (q0, input_string, initial_stack)
4.  if IsAccepted(initial_id, M):
5.      return Result(True, [initial_id], "Accepted at start")
6.
7.  Queue <- EmptyQueue()
8.  Visited <- EmptySet()
9.  Queue.enqueue( (initial_id, [initial_id]) )
10. Visited.add( (q0, input_string, initial_stack) )
11.
12. nodes_explored <- 0
13. longest_path <- [initial_id]
14.
15. while not Queue.isEmpty():
16.     nodes_explored <- nodes_explored + 1
17.     if nodes_explored > max_steps:
18.         return Result(False, longest_path, "Step limit exceeded")
19.
20.     (curr_id, path) <- Queue.dequeue()
21.     if length(path) > length(longest_path):
22.         longest_path <- path
23.
24.     if IsAccepted(curr_id, M):
25.         return Result(True, path, "Accepted")
26.
27.     if curr_id.stack is empty:
28.         continue  // cannot transition with empty stack
29.
30.     top_symbol <- curr_id.stack[0]
31.     rest_stack <- curr_id.stack[1:]
32.
33.     // Explore Epsilon Transitions
34.     for each (to_state, push_tokens) in delta(curr_id.state, ε, top_symbol):
35.         new_stack <- push_tokens + rest_stack
36.         config_sig <- (to_state, curr_id.remaining_input, new_stack)
37.         if config_sig not in Visited:
38.             Visited.add(config_sig)
39.             next_id <- (to_state, curr_id.remaining_input, new_stack)
40.             Queue.enqueue( (next_id, path + [next_id]) )
41.
42.     // Explore Input-Consuming Transitions
43.     if curr_id.remaining_input is not empty:
44.         a <- curr_id.remaining_input[0]
45.         rem_w <- curr_id.remaining_input[1:]
46.         for each (to_state, push_tokens) in delta(curr_id.state, a, top_symbol):
47.             new_stack <- push_tokens + rest_stack
48.             config_sig <- (to_state, rem_w, new_stack)
49.             if config_sig not in Visited:
50.                 Visited.add(config_sig)
51.                 next_id <- (to_state, rem_w, new_stack)
52.                 Queue.enqueue( (next_id, path + [next_id]) )
53.
54. return Result(False, longest_path, "No accepting path found")
```

---

## 5. Manually Validated Example
We validate the PDA for $L = \{ a^n b^n \mid n \ge 1 \}$ by Final State on input string $w = \text{"aabb"}$.

### PDA Formal Definition:
- $Q = \{q_0, q_1, q_2\}$
- $\Sigma = \{a, b\}$
- $\Gamma = \{A, Z_0\}$
- Start state $= q_0$, Start stack symbol $= Z_0$, Final states $F = \{q_2\}$
- Transitions:
  1. $\delta(q_0, a, Z_0) \to (q_0, AZ_0)$
  2. $\delta(q_0, a, A) \to (q_0, AA)$
  3. $\delta(q_0, b, A) \to (q_1, \epsilon)$
  4. $\delta(q_1, b, A) \to (q_1, \epsilon)$
  5. $\delta(q_1, \epsilon, Z_0) \to (q_2, Z_0)$

### Step-by-Step Manual Trace Table:
| Step | Current State | Remaining Input | Stack Contents | Transition Applied | New State | Resulting Stack | Instantaneous Description (ID) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **0** | $q_0$ | `aabb` | $Z_0$ | Start Configuration | $q_0$ | $Z_0$ | $(q_0, \text{aabb}, Z_0)$ |
| **1** | $q_0$ | `abb` | $AZ_0$ | $\delta(q_0, a, Z_0) \to (q_0, AZ_0)$ | $q_0$ | $AZ_0$ | $(q_0, \text{abb}, AZ_0)$ |
| **2** | $q_0$ | `bb` | $AAZ_0$ | $\delta(q_0, a, A) \to (q_0, AA)$ | $q_0$ | $AAZ_0$ | $(q_0, \text{bb}, AAZ_0)$ |
| **3** | $q_0$ | `b` | $AZ_0$ | $\delta(q_0, b, A) \to (q_1, \epsilon)$ | $q_1$ | $AZ_0$ | $(q_1, \text{b}, AZ_0)$ |
| **4** | $q_1$ | $\epsilon$ | $Z_0$ | $\delta(q_1, b, A) \to (q_1, \epsilon)$ | $q_1$ | $Z_0$ | $(q_1, \epsilon, Z_0)$ |
| **5** | $q_1$ | $\epsilon$ | $Z_0$ | $\delta(q_1, \epsilon, Z_0) \to (q_2, Z_0)$ | $q_2$ | $Z_0$ | $(q_2, \epsilon, Z_0)$ |

**Validation Verdict:**
Input is completely consumed ($\epsilon$), current state is $q_2 \in F$.
**Output:** **ACCEPTED** (Matches theoretical expectation and simulator output).
