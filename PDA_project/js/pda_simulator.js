/**
 * Pushdown Automaton Core Simulation Engine (Client-Side JS)
 * Implements M = (Q, Sigma, Gamma, delta, q0, Z0, F)
 * Breadth-First Search for DPDA and NPDA exploration
 */

class PDASimulator {
  constructor(config) {
    this.name = config.name || "Pushdown Automaton";
    this.description = config.description || "";
    this.states = [...new Set(config.states || [])].sort();
    this.inputAlphabet = [...new Set(config.input_alphabet || [])].sort();
    this.stackAlphabet = [...new Set(config.stack_alphabet || [])].sort();
    this.startState = config.start_state || "q0";
    this.startStackSymbol = config.start_stack_symbol || "Z0";
    this.finalStates = [...new Set(config.final_states || [])].sort();
    this.acceptanceMode = config.acceptance_mode || "final_state";
    this.transitions = (config.transitions || []).map(t => ({
      from_state: t.from_state,
      input_symbol: this.normalizeInput(t.input_symbol),
      pop_symbol: t.pop_symbol,
      to_state: t.to_state,
      push_symbols: this.tokenizePush(t.push_symbols)
    }));
    this.rawTransitions = config.transitions || [];

    this.buildIndex();
  }

  normalizeInput(sym) {
    if (!sym || sym === "ε" || sym === "λ" || sym === "eps" || sym === "epsilon") {
      return "ε";
    }
    return sym;
  }

  tokenizePush(symbols) {
    if (!symbols || symbols === "ε" || symbols === "λ" || symbols === "eps" || symbols === "epsilon") {
      return [];
    }
    if (Array.isArray(symbols)) {
      return symbols.filter(s => s && s !== "ε");
    }
    // Greedy match against stack alphabet symbols sorted by length descending
    const sorted = [...this.stackAlphabet].sort((a, b) => b.length - a.length);
    const tokens = [];
    let i = 0;
    while (i < symbols.length) {
      let matched = false;
      for (const sym of sorted) {
        if (sym && symbols.startsWith(sym, i)) {
          tokens.push(sym);
          i += sym.length;
          matched = true;
          break;
        }
      }
      if (!matched) {
        tokens.push(symbols[i]);
        i += 1;
      }
    }
    return tokens;
  }

  buildIndex() {
    this.transitionIndex = new Map();
    for (const t of this.transitions) {
      const key = `${t.from_state}|${t.input_symbol}|${t.pop_symbol}`;
      if (!this.transitionIndex.has(key)) {
        this.transitionIndex.set(key, []);
      }
      this.transitionIndex.get(key).push(t);
    }
  }

  isDeterministic() {
    for (const q of this.states) {
      for (const x of this.stackAlphabet) {
        const epsKey = `${q}|ε|${x}`;
        const epsList = this.transitionIndex.get(epsKey) || [];
        if (epsList.length > 1) return false;
        const hasEps = epsList.length === 1;

        for (const a of this.inputAlphabet) {
          const inpKey = `${q}|${a}|${x}`;
          const inpList = this.transitionIndex.get(inpKey) || [];
          if (inpList.length > 1) return false;
          if (hasEps && inpList.length > 0) return false;
        }
      }
    }
    return true;
  }

  isAcceptedConfig(state, remainingInput, stack) {
    if (remainingInput.length > 0) return false;

    if (this.acceptanceMode === "final_state") {
      return this.finalStates.includes(state);
    } else if (this.acceptanceMode === "empty_stack") {
      return stack.length === 0;
    } else if (this.acceptanceMode === "both") {
      return this.finalStates.includes(state) && stack.length === 0;
    }
    return false;
  }

  simulate(inputString, maxSteps = 1500) {
    // Validate characters
    for (const ch of inputString) {
      if (!this.inputAlphabet.includes(ch)) {
        return {
          accepted: false,
          reason: `Symbol '${ch}' is not in the input alphabet Σ {${this.inputAlphabet.join(', ')}}`,
          trace: [],
          totalSteps: 0,
          isDeterministic: this.isDeterministic()
        };
      }
    }

    const initialStack = this.startStackSymbol ? [this.startStackSymbol] : [];
    const initialNode = {
      step: 0,
      state: this.startState,
      remainingInput: inputString,
      inputConsumed: "",
      stack: initialStack,
      idString: `(${this.startState}, ${inputString || 'ε'}, ${initialStack.join('') || 'ε'})`,
      action: "Initial configuration",
      transition: null
    };

    if (this.isAcceptedConfig(this.startState, inputString, initialStack)) {
      return {
        accepted: true,
        reason: "Accepted at initial configuration.",
        trace: [initialNode],
        totalSteps: 0,
        isDeterministic: this.isDeterministic(),
        branchesExplored: 1
      };
    }

    const queue = [{ node: initialNode, path: [initialNode] }];
    const visited = new Set();
    const sig = `${initialNode.state}|${initialNode.remainingInput}|${initialNode.stack.join(',')}`;
    visited.add(sig);

    let totalNodesExplored = 0;
    let longestPath = [initialNode];

    while (queue.length > 0) {
      totalNodesExplored++;
      const { node: curr, path } = queue.shift();

      if (path.length > longestPath.length) {
        longestPath = path;
      }

      if (totalNodesExplored > maxSteps) {
        return {
          accepted: false,
          reason: `Simulation limit (${maxSteps} steps) exceeded. Possible infinite computation branch.`,
          trace: longestPath,
          totalSteps: longestPath.length - 1,
          isDeterministic: this.isDeterministic(),
          branchesExplored: totalNodesExplored
        };
      }

      if (this.isAcceptedConfig(curr.state, curr.remainingInput, curr.stack)) {
        return {
          accepted: true,
          reason: this.acceptanceMode === "empty_stack" 
            ? "Input exhausted and stack is completely empty."
            : `Input exhausted and state '${curr.state}' is in final states {${this.finalStates.join(', ')}}.`,
          trace: path,
          totalSteps: path.length - 1,
          isDeterministic: this.isDeterministic(),
          branchesExplored: totalNodesExplored
        };
      }

      if (curr.stack.length === 0) {
        continue;
      }

      const top = curr.stack[0];
      const restStack = curr.stack.slice(1);
      const possibleMoves = [];

      // Epsilon transitions: delta(state, eps, top)
      const epsKey = `${curr.state}|ε|${top}`;
      const epsMoves = this.transitionIndex.get(epsKey) || [];
      for (const t of epsMoves) {
        possibleMoves.push({ t, isEps: true });
      }

      // Input consuming moves
      if (curr.remainingInput.length > 0) {
        const char = curr.remainingInput[0];
        const charKey = `${curr.state}|${char}|${top}`;
        const charMoves = this.transitionIndex.get(charKey) || [];
        for (const t of charMoves) {
          possibleMoves.push({ t, isEps: false, char });
        }
      }

      for (const move of possibleMoves) {
        const { t, isEps, char } = move;
        const newRemaining = isEps ? curr.remainingInput : curr.remainingInput.slice(1);
        const consumed = isEps ? "ε" : char;
        const newStack = [...t.push_symbols, ...restStack];

        const stateSig = `${t.to_state}|${newRemaining}|${newStack.join(',')}`;
        if (visited.has(stateSig)) continue;
        visited.add(stateSig);

        const pushStr = t.push_symbols.join('') || "ε";
        const actionStr = isEps
          ? `Epsilon move: pop '${t.pop_symbol}', push '${pushStr}' -> state ${t.to_state}`
          : `Read '${consumed}': pop '${t.pop_symbol}', push '${pushStr}' -> state ${t.to_state}`;

        const nextNode = {
          step: path.length,
          state: t.to_state,
          remainingInput: newRemaining,
          inputConsumed: consumed,
          stack: newStack,
          idString: `(${t.to_state}, ${newRemaining || 'ε'}, ${newStack.join('') || 'ε'})`,
          action: actionStr,
          transition: t
        };

        if (this.isAcceptedConfig(t.to_state, newRemaining, newStack)) {
          return {
            accepted: true,
            reason: this.acceptanceMode === "empty_stack"
              ? "Input exhausted and stack is completely empty."
              : `Input exhausted and reached accepting state '${t.to_state}'.`,
            trace: [...path, nextNode],
            totalSteps: path.length,
            isDeterministic: this.isDeterministic(),
            branchesExplored: totalNodesExplored
          };
        }

        queue.push({ node: nextNode, path: [...path, nextNode] });
      }
    }

    const last = longestPath[longestPath.length - 1];
    let rejectReason = "";
    if (last.remainingInput && last.remainingInput.length > 0) {
      const nextChar = last.remainingInput[0];
      const topStack = last.stack.length > 0 ? last.stack[0] : "ε";
      rejectReason = `No transition rule defined for state '${last.state}' with input symbol '${nextChar}' and stack top '${topStack}'. Automaton halted at step ${last.step}. Input rejected.`;
      if (longestPath.length === 1 && longestPath[0].action === "Initial configuration") {
        longestPath[0].action = `Halted immediately: no rule δ(${last.state}, ${nextChar}, ${topStack})`;
      }
    } else {
      const topStr = last.stack.length > 0 ? last.stack.join('') : "ε";
      if (this.acceptanceMode === "final_state") {
        rejectReason = `Input completely consumed, but halted in non-accepting state '${last.state}' (Final states: {${this.finalStates.join(', ')}}). Input rejected.`;
      } else if (this.acceptanceMode === "empty_stack") {
        rejectReason = `Input completely consumed, but stack is not empty (Stack: '${topStr}'). Input rejected.`;
      } else {
        rejectReason = `Input rejected: requires reaching final state and empty stack (State: '${last.state}', Stack: '${topStr}').`;
      }
    }

    return {
      accepted: false,
      reason: rejectReason,
      trace: longestPath,
      totalSteps: longestPath.length - 1,
      isDeterministic: this.isDeterministic(),
      branchesExplored: totalNodesExplored
    };
  }
}
