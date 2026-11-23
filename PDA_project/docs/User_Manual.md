# Pushdown Automata Simulator – User Manual & Execution Guide
## Course: CSET302 – Automata Theory and Computability

---

## 1. Quick Start Guide

### Option A: Open directly in your Web Browser (Zero-Install!)
1. Open your file manager and navigate to the project directory:
   ```
   /Users/sunnykaushik/.gemini/antigravity/scratch/pushdown-automata-simulator/
   ```
2. Double-click **`index.html`** or right-click $\to$ *Open With Google Chrome / Safari / Edge*.
3. The simulator opens instantly with all features, animations, and pre-loaded presets active!

---

### Option B: Run via Python Local Web Server
If you prefer running through a local HTTP server:
1. Open Terminal and navigate to the folder:
   ```bash
   cd /Users/sunnykaushik/.gemini/antigravity/scratch/pushdown-automata-simulator
   ```
2. Start the built-in server:
   ```bash
   python3 app.py
   ```
3. Open your browser and visit:
   ```
   http://localhost:8080/
   ```

---

### Option C: Run via Command Line Interface (CLI)
You can test the automata engine directly in terminal:
```bash
# 1. Simulate an input string on the default a^n b^n PDA:
python3 pda_cli.py --preset presets/an_bn.json --input "aaabbb"

# 2. Run a batch test on multiple strings:
python3 pda_cli.py --preset presets/an_bn.json --batch "ab" "aabb" "aaabbb" "a" "abb" "ba"

# 3. Test the Non-deterministic PDA for Even Palindromes:
python3 pda_cli.py --preset presets/even_palindrome.json --input "abba"

# 4. Display the formal 7-tuple specification:
python3 pda_cli.py --preset presets/odd_palindrome.json --info

# 5. Export trace table to a text file:
python3 pda_cli.py --preset presets/an_bn.json --input "aabb" --export-trace trace_output.txt
```

---

### Option D: Run Automated Unit Tests
To verify all 8 test suites and confirm 100% correctness:
```bash
python3 tests/test_pda.py
```

---

## 2. Using the Web Interface

### 2.1 Selecting a Pre-Loaded Preset
1. In the top toolbar, click the **"Standard PDA Presets"** dropdown.
2. Select any of the 7 classic PDA benchmarks:
   - `L = { a^n b^n | n >= 1 } (Final State)`
   - `L = { a^n b^n | n >= 1 } (Empty Stack)`
   - `L = { w c w^R | w in {a,b}* } (Odd Palindrome - DPDA)`
   - `L = { w w^R | w in {a,b}* } (Even Palindrome - NPDA)`
   - `Balanced Parentheses & Brackets () []`
   - `L = { w in {a,b}* | n_a(w) = n_b(w) }`
   - `L = { a^n b^2n | n >= 1 }`
3. The 7-tuple definition, transition table, and state diagram update automatically.

### 2.2 Simulating an Input String
1. Type your input string into the input field (e.g. `aaabbb`).
2. Click **"Load & Reset"**.
3. Use the playback controls:
   - **`▶ Play`**: Automatically steps through the simulation at the chosen speed.
   - **`⏮ Step Back`**: Rewinds by one computation step.
   - **`⏭ Step Forward`**: Advances by one computation step.
   - **`↺ Reset`**: Returns to the initial configuration $(q_0, w, Z_0)$.
   - **Speed Slider**: Adjusts step delay between 0.2s (fast) and 2.0s (slow).

### 2.3 Visual Inspection
- **Input Tape**: Watch the blue `▲ HEAD` pointer move across tape cells. Consumed characters turn gray with checkmarks.
- **State Transition Graph**: The active state glows blue/cyan. The transition arc currently being traversed is highlighted.
- **Physical Stack**: Elements slide in during push operations and fade out during pop operations. The `← TOP` arrow indicates the top element.
- **Instantaneous Description Banner**: Displays the exact theoretical ID: $(q, w, \gamma)$.
- **Execution Trace Table**: Shows the complete history of steps. Clicking any row jumps the simulator directly to that step!

### 2.4 Defining a Custom PDA
1. In the left panel, edit the states, input alphabet, stack alphabet, start state, start stack symbol, and final states.
2. Choose your desired acceptance mode (*Final State*, *Empty Stack*, or *Both*).
3. Add or edit transition rules in the table:
   - Specify: `From State`, `Input Symbol` (use `ε` for epsilon), `Pop Symbol`, `To State`, and `Push Symbols` (use `ε` for pure pop).
4. Click **"Update PDA"**. The simulator validates your 7-tuple, detects if it is a DPDA or NPDA, and re-renders the diagram.

### 2.5 Automated Batch Regression Testing
1. Click the **"Batch Test Suite & Validation"** tab at the bottom of the page.
2. Click **"Run All Tests"**.
3. The simulator runs all pre-loaded normal and edge cases, compares actual vs. expected results, and displays a summary.
