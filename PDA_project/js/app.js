/**
 * Pushdown Automata Simulator Application Controller
 * Connects UI inputs, simulation engine, visualizer and batch testing
 */

document.addEventListener("DOMContentLoaded", () => {
  // DOM Elements
  const presetSelect = document.getElementById("preset-select");
  const inputStringEl = document.getElementById("input-string");
  const btnLoad = document.getElementById("btn-load");
  const btnStepFwd = document.getElementById("btn-step-fwd");
  const btnStepBack = document.getElementById("btn-step-back");
  const btnPlay = document.getElementById("btn-play");
  const btnReset = document.getElementById("btn-reset");
  const speedSlider = document.getElementById("speed-slider");
  const speedLabel = document.getElementById("speed-label");

  // Form inputs
  const pdaNameInput = document.getElementById("pda-name");
  const statesInput = document.getElementById("states-input");
  const inputAlphabetInput = document.getElementById("input-alphabet-input");
  const stackAlphabetInput = document.getElementById("stack-alphabet-input");
  const startStateInput = document.getElementById("start-state-input");
  const startStackInput = document.getElementById("start-stack-input");
  const finalStatesInput = document.getElementById("final-states-input");
  const acceptanceModeInput = document.getElementById("acceptance-mode-input");
  const transitionsTableBody = document.getElementById("transitions-tbody");
  const btnAddTransition = document.getElementById("btn-add-transition");
  const btnApplyConfig = document.getElementById("btn-apply-config");
  const pdaTypeBadge = document.getElementById("pda-type-badge");

  // Visualizer elements
  const visualizer = new PDAVisualizer({
    svg: document.getElementById("diagram-svg"),
    stackContainer: document.getElementById("stack-container"),
    tapeContainer: document.getElementById("tape-container"),
    traceTableBody: document.getElementById("trace-tbody"),
    idDisplay: document.getElementById("id-display"),
    actionDisplay: document.getElementById("action-display"),
    statusBadge: document.getElementById("status-badge"),
    stackCountBadge: document.getElementById("stack-depth-badge")
  });

  // App State
  let currentPDA = null;
  let currentSimulation = null;
  let currentStepIdx = 0;
  let isPlaying = false;
  let playInterval = null;
  let currentInputString = "";

  // 1. Populate Presets Dropdown
  for (const key in PRESETS) {
    const opt = document.createElement("option");
    opt.value = key;
    opt.textContent = PRESETS[key].name;
    presetSelect.appendChild(opt);
  }

  // Load a preset into config & simulator
  function loadPreset(key) {
    const data = PRESETS[key];
    if (!data) return;

    pdaNameInput.value = data.name;
    statesInput.value = data.states.join(", ");
    inputAlphabetInput.value = data.input_alphabet.join(", ");
    stackAlphabetInput.value = data.stack_alphabet.join(", ");
    startStateInput.value = data.start_state;
    startStackInput.value = data.start_stack_symbol;
    finalStatesInput.value = data.final_states.join(", ");
    acceptanceModeInput.value = data.acceptance_mode;

    renderTransitionsEditor(data.transitions);

    // Apply configuration
    applyConfigFromForm();

    // Set sample input string if available
    if (data.sample_accepted && data.sample_accepted.length > 0) {
      inputStringEl.value = data.sample_accepted[0];
    } else {
      inputStringEl.value = "";
    }

    renderBatchTests(data);
    resetSimulation();
  }

  // Render transitions editor table
  function renderTransitionsEditor(transitions) {
    transitionsTableBody.innerHTML = "";
    transitions.forEach((t, idx) => {
      const tr = document.createElement("tr");
      const pushStr = Array.isArray(t.push_symbols) ? t.push_symbols.join('') : (t.push_symbols || "ε");
      tr.innerHTML = `
        <td><input type="text" class="t-from" value="${t.from_state}"></td>
        <td><input type="text" class="t-inp" value="${t.input_symbol}"></td>
        <td><input type="text" class="t-pop" value="${t.pop_symbol}"></td>
        <td><input type="text" class="t-to" value="${t.to_state}"></td>
        <td><input type="text" class="t-push" value="${pushStr}"></td>
        <td><button class="btn btn-sm btn-danger btn-del-t">✕</button></td>
      `;
      tr.querySelector(".btn-del-t").addEventListener("click", () => {
        tr.remove();
        applyConfigFromForm();
      });
      transitionsTableBody.appendChild(tr);
    });
  }

  // Parse form into PDA object
  function applyConfigFromForm() {
    const parseList = str => str.split(",").map(s => s.trim()).filter(s => s.length > 0);

    const rows = transitionsTableBody.querySelectorAll("tr");
    const rawTransitions = [];
    rows.forEach(r => {
      rawTransitions.push({
        from_state: r.querySelector(".t-from").value.trim(),
        input_symbol: r.querySelector(".t-inp").value.trim(),
        pop_symbol: r.querySelector(".t-pop").value.trim(),
        to_state: r.querySelector(".t-to").value.trim(),
        push_symbols: r.querySelector(".t-push").value.trim()
      });
    });

    const config = {
      name: pdaNameInput.value.trim(),
      states: parseList(statesInput.value),
      input_alphabet: parseList(inputAlphabetInput.value),
      stack_alphabet: parseList(stackAlphabetInput.value),
      start_state: startStateInput.value.trim(),
      start_stack_symbol: startStackInput.value.trim(),
      final_states: parseList(finalStatesInput.value),
      acceptance_mode: acceptanceModeInput.value,
      transitions: rawTransitions
    };

    currentPDA = new PDASimulator(config);

    // Update Determinism Badge
    const isDet = currentPDA.isDeterministic();
    if (pdaTypeBadge) {
      pdaTypeBadge.textContent = isDet ? "Deterministic (DPDA)" : "Nondeterministic (NPDA)";
      pdaTypeBadge.className = "badge " + (isDet ? "badge-primary" : "badge-purple");
    }

    // Render static state diagram
    visualizer.renderDiagram(currentPDA, currentPDA.startState, null);
  }

  // Add transition row
  btnAddTransition.addEventListener("click", () => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><input type="text" class="t-from" value="${startStateInput.value.trim() || 'q0'}"></td>
      <td><input type="text" class="t-inp" value="a"></td>
      <td><input type="text" class="t-pop" value="${startStackInput.value.trim() || 'Z0'}"></td>
      <td><input type="text" class="t-to" value="${startStateInput.value.trim() || 'q0'}"></td>
      <td><input type="text" class="t-push" value="ε"></td>
      <td><button class="btn btn-sm btn-danger btn-del-t">✕</button></td>
    `;
    tr.querySelector(".btn-del-t").addEventListener("click", () => {
      tr.remove();
      applyConfigFromForm();
    });
    transitionsTableBody.appendChild(tr);
    applyConfigFromForm();
  });

  btnApplyConfig.addEventListener("click", () => {
    applyConfigFromForm();
    resetSimulation();
  });

  presetSelect.addEventListener("change", (e) => {
    loadPreset(e.target.value);
  });

  // ==========================================
  // SIMULATION CONTROLS
  // ==========================================
  function resetSimulation() {
    stopPlayback();
    currentInputString = inputStringEl.value.trim();
    if (!currentPDA) applyConfigFromForm();

    currentSimulation = currentPDA.simulate(currentInputString);
    currentStepIdx = 0;

    const initialNode = currentSimulation.trace[0] || {
      step: 0,
      state: currentPDA.startState,
      remainingInput: currentInputString,
      stack: currentPDA.startStackSymbol ? [currentPDA.startStackSymbol] : [],
      idString: `(${currentPDA.startState}, ${currentInputString || 'ε'}, ${currentPDA.startStackSymbol || 'ε'})`,
      action: "Ready to simulate"
    };

    const isImmediateEnd = currentSimulation.trace.length <= 1;

    visualizer.updateStepInfo(initialNode, currentSimulation.totalSteps, currentInputString, isImmediateEnd && !currentSimulation.accepted);
    visualizer.renderDiagram(currentPDA, initialNode.state, null);
    visualizer.renderTrace(currentSimulation.trace, 0);

    const statusBadge = document.getElementById("status-badge");
    if (isImmediateEnd) {
      visualizer.updateVerdict(currentSimulation.accepted, currentSimulation.reason);
    } else {
      if (statusBadge) statusBadge.style.display = "none";
    }
  }

  function renderCurrentStep() {
    if (!currentSimulation || !currentSimulation.trace.length) return;

    const stepNode = currentSimulation.trace[currentStepIdx];
    const isAtEnd = currentStepIdx === currentSimulation.trace.length - 1;
    const isHaltedReject = isAtEnd && !currentSimulation.accepted;

    visualizer.updateStepInfo(stepNode, currentSimulation.totalSteps, currentInputString, isHaltedReject);
    visualizer.renderDiagram(currentPDA, stepNode.state, stepNode.transition);
    visualizer.renderTrace(currentSimulation.trace, currentStepIdx);

    // If at final step, show verdict
    if (isAtEnd) {
      visualizer.updateVerdict(currentSimulation.accepted, currentSimulation.reason);
      stopPlayback();
    } else {
      const statusBadge = document.getElementById("status-badge");
      if (statusBadge) statusBadge.style.display = "none";
    }
  }

  function stepForward() {
    if (!currentSimulation) resetSimulation();
    if (currentStepIdx < currentSimulation.trace.length - 1) {
      currentStepIdx++;
      renderCurrentStep();
    } else {
      renderCurrentStep();
      stopPlayback();
    }
  }

  function stepBackward() {
    if (!currentSimulation) return;
    if (currentStepIdx > 0) {
      currentStepIdx--;
      renderCurrentStep();
    }
  }

  function startPlayback() {
    if (isPlaying) return;
    isPlaying = true;
    btnPlay.innerHTML = "❚❚ Pause";
    btnPlay.classList.replace("btn-success", "btn-outline");

    const delay = parseInt(speedSlider.value, 10);
    playInterval = setInterval(() => {
      if (currentStepIdx < currentSimulation.trace.length - 1) {
        stepForward();
      } else {
        stopPlayback();
      }
    }, delay);
  }

  function stopPlayback() {
    isPlaying = false;
    if (playInterval) clearInterval(playInterval);
    playInterval = null;
    if (btnPlay) {
      btnPlay.innerHTML = "▶ Play";
      btnPlay.classList.replace("btn-outline", "btn-success");
    }
  }

  btnLoad.addEventListener("click", resetSimulation);
  btnStepFwd.addEventListener("click", stepForward);
  btnStepBack.addEventListener("click", stepBackward);
  btnReset.addEventListener("click", resetSimulation);

  btnPlay.addEventListener("click", () => {
    if (isPlaying) {
      stopPlayback();
    } else {
      if (currentSimulation && currentSimulation.trace.length <= 1) {
        renderCurrentStep();
        return;
      }
      if (currentStepIdx >= currentSimulation.trace.length - 1) {
        currentStepIdx = 0;
      }
      startPlayback();
    }
  });

  speedSlider.addEventListener("input", (e) => {
    const ms = e.target.value;
    speedLabel.textContent = `${(ms / 1000).toFixed(1)}s`;
    if (isPlaying) {
      stopPlayback();
      startPlayback();
    }
  });

  // Global jump to step for table row clicks
  window.jumpToStep = function(stepIdx) {
    if (stepIdx >= 0 && stepIdx < currentSimulation.trace.length) {
      currentStepIdx = stepIdx;
      renderCurrentStep();
    }
  };

  // ==========================================
  // BATCH TEST SUITE
  // ==========================================
  function renderBatchTests(presetData) {
    const tbody = document.getElementById("batch-tbody");
    if (!tbody) return;
    tbody.innerHTML = "";

    const acceptedSamples = (presetData.sample_accepted || []).map(s => ({ str: s, expected: true }));
    const rejectedSamples = (presetData.sample_rejected || []).map(s => ({ str: s, expected: false }));
    const allSamples = [...acceptedSamples, ...rejectedSamples];

    allSamples.forEach((item, idx) => {
      const tr = document.createElement("tr");
      const displayStr = item.str === "" ? "ε (empty string)" : item.str;
      tr.innerHTML = `
        <td><code>${displayStr}</code></td>
        <td><span class="status-tag ${item.expected ? 'pass' : 'fail'}">${item.expected ? 'ACCEPT' : 'REJECT'}</span></td>
        <td class="batch-actual">-</td>
        <td class="batch-verdict">-</td>
        <td>
          <button class="btn btn-sm btn-outline btn-test-single" data-str="${item.str}">Test</button>
        </td>
      `;
      tr.querySelector(".btn-test-single").addEventListener("click", () => {
        inputStringEl.value = item.str;
        resetSimulation();
        // Switch to Simulator view if on mobile/tab
        const simTab = document.querySelector('[data-tab="simulator"]');
        if (simTab) simTab.click();
      });
      tbody.appendChild(tr);
    });
  }

  const btnRunBatch = document.getElementById("btn-run-batch");
  if (btnRunBatch) {
    btnRunBatch.addEventListener("click", () => {
      if (!currentPDA) applyConfigFromForm();
      const rows = document.querySelectorAll("#batch-tbody tr");
      let passedCount = 0;

      rows.forEach(row => {
        const testBtn = row.querySelector(".btn-test-single");
        const str = testBtn.getAttribute("data-str");
        const expectedIsAccept = row.querySelector(".status-tag").classList.contains("pass");

        const res = currentPDA.simulate(str);
        const actualTd = row.querySelector(".batch-actual");
        const verdictTd = row.querySelector(".batch-verdict");

        actualTd.innerHTML = `<span class="status-tag ${res.accepted ? 'pass' : 'fail'}">${res.accepted ? 'ACCEPT' : 'REJECT'}</span>`;

        const isMatch = res.accepted === expectedIsAccept;
        if (isMatch) passedCount++;
        verdictTd.innerHTML = isMatch
          ? `<span style="color: #10b981; font-weight: bold;">✓ PASS</span>`
          : `<span style="color: #ef4444; font-weight: bold;">✗ FAIL</span>`;
      });

      const summaryEl = document.getElementById("batch-summary");
      if (summaryEl) {
        summaryEl.textContent = `Completed: ${passedCount} / ${rows.length} test cases passed.`;
        summaryEl.style.color = passedCount === rows.length ? "#10b981" : "#ef4444";
      }
    });
  }

  // ==========================================
  // TAB NAVIGATION
  // ==========================================
  const tabBtns = document.querySelectorAll(".tab-btn");
  const tabContents = document.querySelectorAll(".tab-content");

  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      tabBtns.forEach(b => b.classList.remove("active"));
      tabContents.forEach(c => c.classList.remove("active"));
      btn.classList.add("active");
      const target = document.getElementById(btn.getAttribute("data-tab"));
      if (target) target.classList.add("active");
    });
  });

  // Export PDA JSON
  const btnExportJson = document.getElementById("btn-export-json");
  if (btnExportJson) {
    btnExportJson.addEventListener("click", () => {
      if (!currentPDA) applyConfigFromForm();
      const exportData = {
        name: pdaNameInput.value.trim(),
        states: currentPDA.states,
        input_alphabet: currentPDA.inputAlphabet,
        stack_alphabet: currentPDA.stackAlphabet,
        start_state: currentPDA.startState,
        start_stack_symbol: currentPDA.startStackSymbol,
        final_states: currentPDA.finalStates,
        acceptance_mode: currentPDA.acceptanceMode,
        transitions: currentPDA.rawTransitions
      };
      const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `pda_${currentPDA.startState}_export.json`;
      a.click();
      URL.revokeObjectURL(url);
    });
  }

  // Initial Load: Preset an_bn
  loadPreset("an_bn");
});
