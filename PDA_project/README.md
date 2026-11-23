# Pushdown Automata (PDA) Simulator
## CSET302: Automata Theory and Computability – Project #12

A comprehensive, interactive Pushdown Automata Simulator and verification engine developed for **CSET302: Automata Theory and Computability**. It fulfills all evaluation criteria for **Milestone 1 (5 Marks)** and **Milestone 2 (9 Marks)**.

---

## 🌟 Key Features

- **Dual Computational Engine**: High-performance Python backend (`src/pda_engine.py`) and zero-latency client-side JavaScript engine (`js/pda_simulator.js`).
- **Interactive Visual Environment**:
  - **Animated Physical Stack**: Vertical LIFO stack container with smooth push/pop CSS animations and dynamic `← TOP` indicator.
  - **Input Tape Visualizer**: Horizontally scrolling tape displaying consumed vs unread symbols with active `▲ HEAD` indicator.
  - **SVG State Graph**: Planar graph rendering of states, self-loops, and curved transitions with glowing active state/edge highlights.
  - **Live Instantaneous Description (ID)**: Real-time mathematical representation $(q, w, \gamma)$ at every step.
- **Support for Both Automata Classes**:
  - **Deterministic PDAs (DPDA)**
  - **Non-Deterministic PDAs (NPDA)** with Breadth-First Search (BFS) multi-branch exploration and cycle detection.
- **Both Acceptance Modes**:
  - Acceptance by **Final State** ($L_f$)
  - Acceptance by **Empty Stack** ($L_e$)
  - Combined mode
- **Pre-Loaded Classical Benchmark Library**:
  1. $L = \{ a^n b^n \mid n \ge 1 \}$ (Final State)
  2. $L = \{ a^n b^n \mid n \ge 1 \}$ (Empty Stack)
  3. $L = \{ w c w^R \mid w \in \{a,b\}^* \}$ (Odd Palindrome – DPDA)
  4. $L = \{ w w^R \mid w \in \{a,b\}^* \}$ (Even Palindrome – NPDA)
  5. Balanced Parentheses & Brackets () []
  6. Equal number of a's and b's: $n_a(w) = n_b(w)$
  7. Asymmetric count: $L = \{ a^n b^{2n} \mid n \ge 1 \}$
- **Batch Regression Test Runner**: 1-click execution across normal and edge cases with expected vs actual comparison table.
- **CLI Utility & Test Suite**: Full CLI tool (`pda_cli.py`) and unit tests (`tests/test_pda.py`) with 100% pass rate.

---

## 📁 Project Directory Structure

```
pushdown-automata-simulator/
├── index.html                   # Interactive Single-Page Web Application
├── app.py                       # Zero-dependency Python server & REST API
├── pda_cli.py                   # Command-line interface for simulation & batch runs
├── README.md                    # Project overview and quick start
├── css/
│   └── style.css                # Modern responsive academic UI styling
├── js/
│   ├── app.js                   # Application controller & event bindings
│   ├── visualizer.js            # SVG graph, animated stack, & tape visualizer
│   ├── pda_simulator.js         # Client-side BFS PDA simulation engine
│   └── presets_data.js          # Library of 7 standard PDA benchmarks
├── src/
│   └── pda_engine.py            # Python core simulation engine & 7-tuple model
├── presets/
│   ├── an_bn.json               # a^n b^n (Final State)
│   ├── an_bn_empty_stack.json   # a^n b^n (Empty Stack)
│   ├── odd_palindrome.json      # w c w^R (DPDA)
│   ├── even_palindrome.json     # w w^R (NPDA)
│   ├── balanced_parentheses.json# Matching () and []
│   ├── equal_a_b.json           # Equal a's and b's
│   └── an_b2n.json              # a^n b^2n
├── tests/
│   └── test_pda.py              # Automated unit tests (100% pass rate)
└── docs/                        # Complete Documentation Suite
    ├── M1_Project_Design_Report.md         # Milestone 1 Design Report (5 Marks)
    ├── M2_Final_Technical_Report.md        # Milestone 2 Final Report (9 Marks)
    ├── Manual_Validation_Trace_Example.md  # Hand-computed trace validation
    ├── Viva_Voce_Preparation_Guide.md      # 25+ Viva questions & model answers
    ├── Group_Contributions_and_Roles.md    # 5-member team workload matrix
    ├── User_Manual.md                      # Detailed usage instructions
    └── Presentation_Slide_Deck.md          # 10-slide defense presentation outline
```

---

## 🚀 How to Run

### 1. Direct Web Browser Execution (Zero Install)
Simply double-click `index.html` or open it in Chrome, Safari, or Edge. Everything works completely offline in your browser!

### 2. Python Web Server
```bash
python3 app.py
```
Then visit `http://localhost:8080/` in your browser.

### 3. Command Line Interface (CLI)
```bash
# Single string simulation with trace table:
python3 pda_cli.py --preset presets/an_bn.json --input "aaabbb"

# Batch testing multiple strings:
python3 pda_cli.py --preset presets/an_bn.json --batch "ab" "aabb" "aaabbb" "a" "abb" "ba"
```

### 4. Running Unit Tests
```bash
python3 tests/test_pda.py
```

---

## 👥 Group Roles (CSET302 5-Student Batch Rule)
- **Student 1 (Lead)**: System Architecture, 7-Tuple Modeling, Milestone Coordination
- **Student 2**: Core Automata Engines (Python & JS), NPDA BFS Traversal
- **Student 3**: Visualizer Engineering (SVG Graph, Physical Stack, Tape Head)
- **Student 4**: QA, Unit Testing, Benchmark Presets, Manual Trace Validations
- **Student 5**: Technical Reports (M1, M2), User Manual, Viva Defense Preparation
