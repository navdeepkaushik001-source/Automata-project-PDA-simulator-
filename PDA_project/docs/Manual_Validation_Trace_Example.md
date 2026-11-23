# Manually Validated Example & Step-by-Step Mathematical Trace
## Course: CSET302 – Automata Theory and Computability
### Subject: Pushdown Automata Simulator (#12)

This document provides exhaustive, by-hand mathematical validations of sample string computations. These traces verify the correctness of our simulator engine against classical textbook theory (Hopcroft, Motwani & Ullman).

---

## Example 1: Language $L = \{ a^n b^n \mid n \ge 1 \}$ (Acceptance by Final State)

### 1. Formal 7-Tuple Specification:
$$M = (Q, \Sigma, \Gamma, \delta, q_0, Z_0, F)$$
- $Q = \{q_0, q_1, q_2\}$
- $\Sigma = \{a, b\}$
- $\Gamma = \{A, Z_0\}$
- Start state $= q_0$
- Initial stack symbol $= Z_0$
- Final state set $F = \{q_2\}$
- Acceptance Mode: **Final State**

### 2. Transition Rules $\delta$:
1. $\delta(q_0, a, Z_0) = \{ (q_0, AZ_0) \}$  *(Read 'a' on bottom symbol, push A)*
2. $\delta(q_0, a, A) = \{ (q_0, AA) \}$      *(Read 'a' with A on top, push another A)*
3. $\delta(q_0, b, A) = \{ (q_1, \epsilon) \}$ *(Read first 'b', pop matching A, switch to state q1)*
4. $\delta(q_1, b, A) = \{ (q_1, \epsilon) \}$ *(Read subsequent 'b's, pop matching A)*
5. $\delta(q_1, \epsilon, Z_0) = \{ (q_2, Z_0) \}$ *(On input exhaustion and stack seeing Z0, epsilon-move to final state q2)*

---

### 3. Step-by-Step Manual Trace for Input String $w = \text{"aabb"}$

#### Mathematical Derivation Chain:
$$(q_0, \text{aabb}, Z_0) \vdash (q_0, \text{abb}, AZ_0) \vdash (q_0, \text{bb}, AAZ_0) \vdash (q_1, \text{b}, AZ_0) \vdash (q_1, \epsilon, Z_0) \vdash (q_2, \epsilon, Z_0)$$

#### Comprehensive Step-by-Step Table:
| Step | Current State ($q$) | Remaining String ($w$) | Stack Top $\to$ Bottom ($\gamma$) | Input Read ($a$) | Stack Pop ($X$) | Stack Push ($\alpha$) | Transition Applied | Next State ($p$) | Instantaneous Description (ID) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **0** | $q_0$ | `aabb` | $Z_0$ | - | - | - | *(Initial)* | $q_0$ | $(q_0, \text{aabb}, Z_0)$ |
| **1** | $q_0$ | `abb` | $A Z_0$ | `a` | $Z_0$ | $A Z_0$ | $\delta(q_0, a, Z_0) \to (q_0, AZ_0)$ | $q_0$ | $(q_0, \text{abb}, AZ_0)$ |
| **2** | $q_0$ | `bb` | $A A Z_0$ | `a` | $A$ | $A A$ | $\delta(q_0, a, A) \to (q_0, AA)$ | $q_0$ | $(q_0, \text{bb}, AAZ_0)$ |
| **3** | $q_0$ | `b` | $A Z_0$ | `b` | $A$ | $\epsilon$ | $\delta(q_0, b, A) \to (q_1, \epsilon)$ | $q_1$ | $(q_1, \text{b}, AZ_0)$ |
| **4** | $q_1$ | $\epsilon$ | $Z_0$ | `b` | $A$ | $\epsilon$ | $\delta(q_1, b, A) \to (q_1, \epsilon)$ | $q_1$ | $(q_1, \epsilon, Z_0)$ |
| **5** | $q_1$ | $\epsilon$ | $Z_0$ | $\epsilon$ | $Z_0$ | $Z_0$ | $\delta(q_1, \epsilon, Z_0) \to (q_2, Z_0)$ | $q_2$ | $(q_2, \epsilon, Z_0)$ |

#### Acceptance Evaluation:
- **Condition 1 (Input Consumed):** Remaining input is $\epsilon$ (fully consumed).
- **Condition 2 (Final State):** Current state $q_2 \in F = \{q_2\}$.
- **Result:** **ACCEPTED**.

---

## Example 2: Negative Validation on Invalid String $w = \text{"aab"}$

We test the non-member string $w = \text{"aab"}$ ($n_a = 2 \ne n_b = 1$):

1. **Step 0:** $(q_0, \text{aab}, Z_0)$
2. **Step 1:** Read 'a' $\to (q_0, \text{ab}, AZ_0)$
3. **Step 2:** Read 'a' $\to (q_0, \text{b}, AAZ_0)$
4. **Step 3:** Read 'b' $\to (q_1, \epsilon, AZ_0)$
5. **Step 4:** At configuration $(q_1, \epsilon, AZ_0)$:
   - Remaining input is $\epsilon$.
   - Stack top is $A$.
   - Current state is $q_1 \notin F$.
   - Only transition from $q_1$ on $\epsilon$ requires stack top $Z_0$ ($\delta(q_1, \epsilon, Z_0)$), but current stack top is $A$.
   - No transition is defined for $(q_1, \epsilon, A)$.
   - The automaton **halts without reaching a final state**.

#### Rejection Evaluation:
- Final configuration reached: $(q_1, \epsilon, AZ_0)$.
- State $q_1 \notin F$, stack is not empty ($AZ_0 \ne \epsilon$).
- **Result:** **REJECTED** (Correctly rejects invalid string).
