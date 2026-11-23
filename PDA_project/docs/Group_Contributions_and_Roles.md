# Group Members & Individual Contributions Breakdown
## Course: CSET302 – Automata Theory and Computability
### Simulator Project Topic: #12 – Pushdown Automata Simulator
**Institution:** School of Computer Science Engineering & Technology (SCSET), Bennett University, Greater Noida  
**Faculty Evaluator:** Rashmi Ma’am  
**Team Structure:** Group #12 (5 Students as mandated by CSET302 Guidelines)

---

## Team Roster & Allocation Matrix

| Student Name | Enrollment ID | Designated Project Role | Primary Focus Area | Effort Share |
| :--- | :---: | :--- | :--- | :---: |
| **NAVDEEP KAUSHIK** | **S24CSEU2699** | System Architect & Project Lead | Formal 7-Tuple Model, Architecture Design, Milestone Coordination | 20% |
| **SHRAVAN KUMAR** | **S24CSEU2677** | Core Automata Engine & BFS Developer | Python Engine (`src/pda_engine.py`), NPDA BFS Graph Traversal, Dual Modes | 20% |
| **AYUSH KUMAR** | **S24CSEU2698** | Frontend UI & Visualizer Specialist | Animated Vertical Stack, SVG State Graph with Glow, Dynamic Tape Head | 20% |
| **SRIJAN PANDEY** | **S24CSEU2691** | QA Engineer & Test Suite Lead | Python Unit Tests (`tests/test_pda.py`), 21-Case Test Matrix, 7 Presets | 20% |
| **PIYUSH DAGAR** | **S24CSEU2680** | Technical Documentation & Deliverables | Milestone-II Technical Report, User Manual, Viva-Voce Guide, PPT Deck | 20% |

---

## Detailed Task Breakdown

### 1. NAVDEEP KAUSHIK (S24CSEU2699) — System Architect & Team Lead
- Formulated the formal 7-tuple model $M = (Q, \Sigma, \Gamma, \delta, q_0, Z_0, F)$ adhering to standard automata theory.
- Designed the decoupled multi-tier architecture (Presentation, Engine, and Validation layers).
- Established the formal determinism rules ($|\delta(q, a, X)| \le 1$ and $\epsilon$-mutual exclusion).
- Led group milestone reviews, repository standardization, and overall project integration.

### 2. SHRAVAN KUMAR (S24CSEU2677) — Core Automata Engine Developer
- Programmed the Python 3 core simulation engine (`src/pda_engine.py`) with transition map indexing.
- Developed the cycle-safe Breadth-First Search (BFS) graph traversal algorithm for non-deterministic PDAs.
- Implemented dual acceptance mode logic (Acceptance by Final State $L_f$ and Empty Stack $L_e$).
- Ported computational algorithms to client-side ES6 JavaScript (`js/pda_simulator.js`) for instant browser execution.

### 3. AYUSH KUMAR (S24CSEU2698) — Frontend UI & Visualizer Specialist
- Designed and built the responsive web application layout (`index.html` and `css/style.css`).
- Engineered the interactive animated vertical LIFO stack with dynamic CSS transitions and '← TOP' pointer.
- Programmed the synchronous horizontal input tape visualizer tracking reading head coordinates (`▲ HEAD` and `▲ NO TRANSITION`).
- Developed the dynamic SVG state graph generator with curved Bézier arcs and glowing active states.

### 4. SRIJAN PANDEY (S24CSEU2691) — Quality Assurance & Test Engineer
- Authored the comprehensive Python unit testing harness (`tests/test_pda.py`) with 8 automated test suites (100% pass rate).
- Formulated the 21-case experimental test matrix spanning normal, boundary, and edge conditions.
- Curated and validated the library of 7 classical benchmark PDA presets (including $a^n b^n$, palindromes, and brackets).
- Derived complete by-hand mathematical traces to verify simulation outputs against theoretical models.

### 5. PIYUSH DAGAR (S24CSEU2680) — Technical Documentation & Deliverables Lead
- Authored the complete Milestone-II Technical Documentation Report conforming to SCSET guidelines.
- Compiled the comprehensive User Manual and Quick-Start guide for terminal and browser execution.
- Prepared the Viva-Voce defense guide with 25+ theoretical and implementation examination questions.
- Managed the 11-slide PowerPoint presentation deck (`Pushdown_Automata_Simulator_Presentation.pptx` and `slides.html`).
