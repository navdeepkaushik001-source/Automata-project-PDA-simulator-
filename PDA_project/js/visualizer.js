/**
 * Interactive Visualizer for Pushdown Automata Simulator
 * Renders:
 * 1. State Diagram (SVG Graph with layout & active state/transition highlighting)
 * 2. Animated Stack Component (Push/Pop operations, Top pointer)
 * 3. Input Tape Component (Head pointer, consumed vs remaining characters)
 * 4. Step-by-Step Trace & Instantaneous Descriptions
 */

class PDAVisualizer {
  constructor(elements) {
    this.svg = elements.svg;
    this.stackContainer = elements.stackContainer;
    this.tapeContainer = elements.tapeContainer;
    this.traceTableBody = elements.traceTableBody;
    this.idDisplay = elements.idDisplay;
    this.actionDisplay = elements.actionDisplay;
    this.statusBadge = elements.statusBadge;
    this.stackCountBadge = elements.stackCountBadge;

    this.statePositions = new Map();
  }

  // ==========================================
  // 1. STATE DIAGRAM RENDERING (SVG)
  // ==========================================
  renderDiagram(pda, activeState = null, activeTransition = null) {
    if (!this.svg) return;
    this.svg.innerHTML = "";

    const width = this.svg.clientWidth || 550;
    const height = this.svg.clientHeight || 280;

    // Define SVG markers for arrowheads
    const defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
    defs.innerHTML = `
      <marker id="arrow" viewBox="0 0 10 10" refX="24" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#4a5568"/>
      </marker>
      <marker id="arrow-active" viewBox="0 0 10 10" refX="24" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#2563eb"/>
      </marker>
      <marker id="start-arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto">
        <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#10b981"/>
      </marker>
    `;
    this.svg.appendChild(defs);

    const states = pda.states;
    const numStates = states.length;
    this.statePositions.clear();

    // Compute layout: linear or circular
    if (numStates <= 4) {
      // Linear layout with ample margin
      const margin = 80;
      const step = numStates > 1 ? (width - 2 * margin) / (numStates - 1) : 0;
      states.forEach((st, idx) => {
        const x = numStates === 1 ? width / 2 : margin + idx * step;
        const y = height / 2;
        this.statePositions.set(st, { x, y });
      });
    } else {
      // Circular layout
      const cx = width / 2;
      const cy = height / 2;
      const r = Math.min(width, height) * 0.38;
      states.forEach((st, idx) => {
        const angle = (2 * Math.PI * idx) / numStates - Math.PI / 2;
        const x = cx + r * Math.cos(angle);
        const y = cy + r * Math.sin(angle);
        this.statePositions.set(st, { x, y });
      });
    }

    // Group transitions by pair (from, to)
    const grouped = new Map();
    for (const t of pda.rawTransitions) {
      const key = `${t.from_state}->${t.to_state}`;
      if (!grouped.has(key)) grouped.set(key, []);
      const pushStr = Array.isArray(t.push_symbols) ? t.push_symbols.join('') : (t.push_symbols || "ε");
      grouped.get(key).push(`${t.input_symbol}, ${t.pop_symbol} → ${pushStr}`);
    }

    // Draw transitions
    const gTransitions = document.createElementNS("http://www.w3.org/2000/svg", "g");
    grouped.forEach((labels, key) => {
      const [from, to] = key.split("->");
      const p1 = this.statePositions.get(from);
      const p2 = this.statePositions.get(to);
      if (!p1 || !p2) return;

      const isSelfLoop = from === to;
      const isActive = activeTransition && 
        activeTransition.from_state === from && 
        activeTransition.to_state === to;

      if (isSelfLoop) {
        // Self loop above node
        const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
        const r = 26;
        const d = `M ${p1.x - 12} ${p1.y - 22} C ${p1.x - 30} ${p1.y - 75}, ${p1.x + 30} ${p1.y - 75}, ${p1.x + 12} ${p1.y - 22}`;
        path.setAttribute("d", d);
        path.setAttribute("fill", "none");
        path.setAttribute("stroke", isActive ? "#2563eb" : "#94a3b8");
        path.setAttribute("stroke-width", isActive ? "3" : "1.8");
        path.setAttribute("marker-end", isActive ? "url(#arrow-active)" : "url(#arrow)");
        gTransitions.appendChild(path);

        const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
        text.setAttribute("x", p1.x);
        text.setAttribute("y", p1.y - 68);
        text.setAttribute("text-anchor", "middle");
        text.setAttribute("font-size", "11px");
        text.setAttribute("font-family", "system-ui, sans-serif");
        text.setAttribute("fill", isActive ? "#1d4ed8" : "#475569");
        text.textContent = labels.slice(0, 2).join(" | ") + (labels.length > 2 ? ` (+${labels.length - 2})` : "");
        gTransitions.appendChild(text);
      } else {
        // Directed curved path between distinct states
        const dx = p2.x - p1.x;
        const dy = p2.y - p1.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        const curve = 28; // curvature offset

        // Normal vector
        const nx = -dy / dist;
        const ny = dx / dist;

        const mx = (p1.x + p2.x) / 2 + nx * curve;
        const my = (p1.y + p2.y) / 2 + ny * curve;

        const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
        const d = `M ${p1.x} ${p1.y} Q ${mx} ${my} ${p2.x} ${p2.y}`;
        path.setAttribute("d", d);
        path.setAttribute("fill", "none");
        path.setAttribute("stroke", isActive ? "#2563eb" : "#94a3b8");
        path.setAttribute("stroke-width", isActive ? "3" : "1.8");
        path.setAttribute("marker-end", isActive ? "url(#arrow-active)" : "url(#arrow)");
        gTransitions.appendChild(path);

        const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
        text.setAttribute("x", mx);
        text.setAttribute("y", my - 4);
        text.setAttribute("text-anchor", "middle");
        text.setAttribute("font-size", "11px");
        text.setAttribute("font-family", "system-ui, sans-serif");
        text.setAttribute("fill", isActive ? "#1d4ed8" : "#475569");
        text.textContent = labels.slice(0, 2).join(" | ") + (labels.length > 2 ? ` (+${labels.length - 2})` : "");
        gTransitions.appendChild(text);
      }
    });
    this.svg.appendChild(gTransitions);

    // Draw States
    const gStates = document.createElementNS("http://www.w3.org/2000/svg", "g");
    states.forEach(st => {
      const pos = this.statePositions.get(st);
      const isStart = st === pda.startState;
      const isFinal = pda.finalStates.includes(st);
      const isActive = st === activeState;

      // Start state incoming arrow
      if (isStart) {
        const startLine = document.createElementNS("http://www.w3.org/2000/svg", "line");
        startLine.setAttribute("x1", pos.x - 55);
        startLine.setAttribute("y1", pos.y);
        startLine.setAttribute("x2", pos.x - 26);
        startLine.setAttribute("y2", pos.y);
        startLine.setAttribute("stroke", "#10b981");
        startLine.setAttribute("stroke-width", "2.5");
        startLine.setAttribute("marker-end", "url(#start-arrow)");
        gStates.appendChild(startLine);

        const startText = document.createElementNS("http://www.w3.org/2000/svg", "text");
        startText.setAttribute("x", pos.x - 56);
        startText.setAttribute("y", pos.y - 6);
        startText.setAttribute("font-size", "10px");
        startText.setAttribute("font-weight", "bold");
        startText.setAttribute("fill", "#10b981");
        startText.textContent = "Start";
        gStates.appendChild(startText);
      }

      // Outer circle (for final states or halo)
      if (isFinal) {
        const outer = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        outer.setAttribute("cx", pos.x);
        outer.setAttribute("cy", pos.y);
        outer.setAttribute("r", "26");
        outer.setAttribute("fill", "none");
        outer.setAttribute("stroke", isActive ? "#2563eb" : "#475569");
        outer.setAttribute("stroke-width", "2");
        gStates.appendChild(outer);
      }

      // Main State Circle
      const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      circle.setAttribute("cx", pos.x);
      circle.setAttribute("cy", pos.y);
      circle.setAttribute("r", "22");
      circle.setAttribute("fill", isActive ? "#dbeafe" : "#ffffff");
      circle.setAttribute("stroke", isActive ? "#2563eb" : "#64748b");
      circle.setAttribute("stroke-width", isActive ? "3.5" : "2");
      if (isActive) {
        circle.setAttribute("filter", "drop-shadow(0px 0px 8px rgba(37,99,235,0.4))");
      }
      gStates.appendChild(circle);

      // State Label
      const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
      text.setAttribute("x", pos.x);
      text.setAttribute("y", pos.y + 4);
      text.setAttribute("text-anchor", "middle");
      text.setAttribute("font-size", "13px");
      text.setAttribute("font-weight", "600");
      text.setAttribute("font-family", "system-ui, sans-serif");
      text.setAttribute("fill", isActive ? "#1d4ed8" : "#1e293b");
      text.textContent = st;
      gStates.appendChild(text);
    });
    this.svg.appendChild(gStates);
  }

  // ==========================================
  // 2. INPUT TAPE RENDERING
  // ==========================================
  renderTape(fullString, remainingString, isHalted = false) {
    if (!this.tapeContainer) return;
    this.tapeContainer.innerHTML = "";

    const consumedCount = fullString.length - remainingString.length;

    if (fullString.length === 0) {
      const cell = document.createElement("div");
      cell.className = "tape-cell current" + (isHalted ? " halted" : "");
      cell.innerHTML = `<span>ε</span><div class="tape-pointer${isHalted ? ' halted' : ''}">${isHalted ? '▲ NO MOVE' : '▲ HEAD'}</div>`;
      this.tapeContainer.appendChild(cell);
      return;
    }

    for (let i = 0; i < fullString.length; i++) {
      const char = fullString[i];
      const cell = document.createElement("div");
      cell.className = "tape-cell";

      if (i < consumedCount) {
        cell.classList.add("consumed");
        cell.innerHTML = `<span>${char}</span><small class="cell-idx">✓</small>`;
      } else if (i === consumedCount) {
        cell.classList.add("current");
        if (isHalted) cell.classList.add("halted");
        cell.innerHTML = `<span>${char}</span><div class="tape-pointer${isHalted ? ' halted' : ''}">${isHalted ? '▲ NO TRANSITION' : '▲ HEAD'}</div>`;
      } else {
        cell.classList.add("unconsumed");
        cell.innerHTML = `<span>${char}</span>`;
      }
      this.tapeContainer.appendChild(cell);
    }

    // End-of-tape marker cell
    const eofCell = document.createElement("div");
    eofCell.className = "tape-cell eof-cell";
    if (consumedCount >= fullString.length) {
      eofCell.classList.add("current");
      if (isHalted) eofCell.classList.add("halted");
      eofCell.innerHTML = `<span>$</span><div class="tape-pointer${isHalted ? ' halted' : ''}">${isHalted ? '▲ NO TRANSITION' : '▲ HEAD'}</div>`;
    } else {
      eofCell.innerHTML = `<span>$</span>`;
    }
    this.tapeContainer.appendChild(eofCell);
  }

  // ==========================================
  // 3. ANIMATED VERTICAL STACK RENDERING
  // ==========================================
  renderStack(stackArray) {
    if (!this.stackContainer) return;
    this.stackContainer.innerHTML = "";

    if (this.stackCountBadge) {
      this.stackCountBadge.textContent = `Depth: ${stackArray.length}`;
    }

    if (stackArray.length === 0) {
      const emptyDiv = document.createElement("div");
      emptyDiv.className = "stack-empty-msg";
      emptyDiv.innerHTML = "<span>(Empty Stack)</span>";
      this.stackContainer.appendChild(emptyDiv);
      return;
    }

    // Stack is passed as [top, ..., bottom]
    stackArray.forEach((symbol, index) => {
      const cell = document.createElement("div");
      cell.className = "stack-cell";
      if (index === 0) {
        cell.classList.add("stack-top");
        cell.innerHTML = `
          <span class="symbol">${symbol}</span>
          <span class="top-tag">← TOP</span>
        `;
      } else {
        cell.innerHTML = `<span class="symbol">${symbol}</span>`;
      }
      this.stackContainer.appendChild(cell);
    });
  }

  // ==========================================
  // 4. TRACE TABLE & CURRENT STEP INFO
  // ==========================================
  renderTrace(trace, activeStepIdx) {
    if (!this.traceTableBody) return;
    this.traceTableBody.innerHTML = "";

    trace.forEach((step, idx) => {
      const tr = document.createElement("tr");
      tr.className = idx === activeStepIdx ? "active-step-row" : "";
      tr.onclick = () => {
        if (window.jumpToStep) window.jumpToStep(idx);
      };

      const remDisp = step.remainingInput ? step.remainingInput : "ε";
      const stackDisp = step.stack.length > 0 ? step.stack.join('') : "ε";

      tr.innerHTML = `
        <td><span class="step-badge">${step.step}</span></td>
        <td><strong>${step.state}</strong></td>
        <td><code>${remDisp}</code></td>
        <td><code>${stackDisp}</code></td>
        <td><small>${step.action}</small></td>
      `;
      this.traceTableBody.appendChild(tr);

      if (idx === activeStepIdx) {
        // Scroll active row into view
        tr.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
    });
  }

  updateStepInfo(stepNode, totalSteps, fullInput, isHalted = false) {
    if (this.idDisplay) {
      this.idDisplay.textContent = stepNode.idString;
    }
    if (this.actionDisplay) {
      this.actionDisplay.textContent = stepNode.action || "Simulation running";
    }
    this.renderTape(fullInput, stepNode.remainingInput, isHalted);
    this.renderStack(stepNode.stack);
  }

  updateVerdict(accepted, reason) {
    if (!this.statusBadge) return;
    this.statusBadge.className = "status-banner " + (accepted ? "accepted" : "rejected");
    this.statusBadge.innerHTML = `
      <div class="verdict-title">${accepted ? "✓ INPUT ACCEPTED" : "✗ INPUT REJECTED"}</div>
      <div class="verdict-reason">${reason}</div>
    `;
  }
}
