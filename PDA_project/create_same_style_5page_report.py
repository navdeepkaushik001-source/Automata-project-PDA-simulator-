#!/usr/bin/env python3
"""
Generate the exact 5-page report in DOCX format matching the reference NFA Simulator layout,
fonts, styling, and page structure, tailored for Project #12: Pushdown Automata (PDA) Simulator.

Students:
- Navdeep Kaushik | S24CSEU2699
- Shravan Kumar | S24CSEU2677
- Ayush Kumar | S24CSEU2698
- Srijan Pandey | S24CSEU2691
- Piyush Dagar | S24CSEU2680

Submitted to:
Rashmi Ma’am
Department of Computer Science and Engineering
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def create_same_style_report():
    doc = docx.Document()
    
    # Page setup - A4 paper with exact margins matching sample
    section = doc.sections[0]
    section.page_width = Inches(8.27)   # A4 width
    section.page_height = Inches(11.69) # A4 height
    section.top_margin = Inches(0.85)
    section.bottom_margin = Inches(0.85)
    section.left_margin = Inches(0.95)
    section.right_margin = Inches(0.95)
    
    # Configure header & footer
    section.different_first_page_header_footer = False
    
    # Header: None (clean, matching sample)
    header = section.header
    header.is_linked_to_previous = False
    hp = header.paragraphs[0]
    hp.text = ""
    
    # Footer: Centered "PDA Simulator | Milestone 1"
    footer = section.footer
    footer.is_linked_to_previous = False
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    frun = fp.add_run("PDA Simulator | Milestone 1")
    frun.font.name = "Aptos"
    frun.font.size = Pt(9.5)
    frun.font.color.rgb = RGBColor(89, 89, 89) # Muted gray
    
    # Base Style Configuration
    styles = doc.styles
    normal_style = styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Aptos'
    normal_font.size = Pt(10)
    normal_font.color.rgb = RGBColor(38, 38, 38)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)
    
    # Palette
    NAVY_HEADING = RGBColor(31, 78, 121)    # #1F4E79 (Exact reference heading color)
    TEXT_BLACK = RGBColor(38, 38, 38)       # #262626 (Off-black body text)
    MUTED_GRAY = RGBColor(89, 89, 89)       # #595959
    
    def set_cell_background(cell, hex_color):
        tcPr = cell._tc.get_or_add_tcPr()
        tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'))

    def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def set_table_borders_sample(table):
        tblPr = table._tbl.tblPr
        borders = parse_xml(f'''
            <w:tblBorders {nsdecls("w")}>
                <w:top w:val="single" w:sz="8" w:space="0" w:color="314E79"/>
                <w:bottom w:val="single" w:sz="8" w:space="0" w:color="314E79"/>
                <w:left w:val="none"/>
                <w:right w:val="none"/>
                <w:insideH w:val="none"/>
                <w:insideV w:val="none"/>
            </w:tblBorders>
        ''')
        tblPr.append(borders)

    def add_section_heading(text, space_before=12):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Aptos"
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = NAVY_HEADING
        return p

    def add_sub_heading(text, space_before=8):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.name = "Aptos"
        run.font.size = Pt(10.5)
        run.font.bold = True
        run.font.color.rgb = NAVY_HEADING
        return p

    def add_bullet(text):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        r_bullet = p.add_run("•  ")
        r_bullet.font.name = "Aptos"
        r_bullet.font.bold = True
        r_bullet.font.color.rgb = TEXT_BLACK
        r_text = p.add_run(text)
        r_text.font.name = "Aptos"
        r_text.font.size = Pt(10)
        r_text.font.color.rgb = TEXT_BLACK
        return p

    def add_numbered(num_str, text):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.first_line_indent = Inches(-0.25)
        p.paragraph_format.space_after = Pt(2.5)
        p.paragraph_format.line_spacing = 1.15
        r_num = p.add_run(num_str + " ")
        r_num.font.name = "Aptos"
        r_num.font.bold = True
        r_num.font.color.rgb = TEXT_BLACK
        r_text = p.add_run(text)
        r_text.font.name = "Aptos"
        r_text.font.size = Pt(10)
        r_text.font.color.rgb = TEXT_BLACK
        return p

    def format_sample_table(table, col_widths, headers, data, align_cols=None):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        set_table_borders_sample(table)
        
        # Header Row
        hdr_row = table.rows[0]
        trPr = hdr_row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        
        for idx, heading in enumerate(headers):
            cell = hdr_row.cells[idx]
            cell.width = col_widths[idx]
            set_cell_background(cell, "FFFFFF")
            set_cell_margins(cell, top=90, bottom=90, left=100, right=100)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            align = align_cols[idx] if align_cols and idx < len(align_cols) else WD_ALIGN_PARAGRAPH.LEFT
            p.alignment = align
            run = p.add_run(heading)
            run.font.name = "Aptos"
            run.font.bold = True
            run.font.size = Pt(9.5)
            run.font.color.rgb = NAVY_HEADING
            
        # Data Rows (Alternating Shading: Light Blue / White matching reference)
        for r_idx, row_values in enumerate(data):
            row = table.rows[r_idx + 1]
            trPr = row._tr.get_or_add_trPr()
            trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
            
            # Reference PDF alternates: row 0 is light blue, row 1 is white, row 2 is light blue...
            bg_color = "D9E2F3" if (r_idx % 2 == 0) else "FFFFFF"
            for c_idx, val in enumerate(row_values):
                cell = row.cells[c_idx]
                cell.width = col_widths[c_idx]
                set_cell_background(cell, bg_color)
                set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(0)
                align = align_cols[c_idx] if align_cols and c_idx < len(align_cols) else WD_ALIGN_PARAGRAPH.LEFT
                p.alignment = align
                run = p.add_run(str(val))
                run.font.name = "Aptos"
                run.font.size = Pt(9.5)
                run.font.color.rgb = TEXT_BLACK

    # =============================================================
    # PAGE 1: COVER PAGE (Exact Reference Layout)
    # =============================================================
    logo_path = "/Users/sunnykaushik/.gemini/antigravity/brain/3067ee5b-9a93-4550-90a2-9368439afd87/.user_uploaded/media_1795342160013_54aa9f19.png"
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(20)
        p_logo.paragraph_format.space_after = Pt(28)
        r_logo = p_logo.add_run()
        r_logo.add_picture(logo_path, width=Inches(2.55))

    p_m1 = doc.add_paragraph()
    p_m1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_m1.paragraph_format.space_after = Pt(10)
    r_m1 = p_m1.add_run("MILESTONE 1 PROJECT REPORT")
    r_m1.font.name = "Aptos"
    r_m1.font.size = Pt(13)
    r_m1.font.bold = True
    r_m1.font.color.rgb = RGBColor(0, 0, 0)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run("PDA SIMULATOR")
    r_title.font.name = "Aptos"
    r_title.font.size = Pt(24)
    r_title.font.bold = True
    r_title.font.color.rgb = NAVY_HEADING

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(40)
    r_sub = p_sub.add_run("Interactive Pushdown Automata Simulator")
    r_sub.font.name = "Aptos"
    r_sub.font.size = Pt(11)
    r_sub.font.color.rgb = TEXT_BLACK

    p_by = doc.add_paragraph()
    p_by.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_by.paragraph_format.space_after = Pt(12)
    r_by = p_by.add_run("Submitted by")
    r_by.font.name = "Aptos"
    r_by.font.size = Pt(11)
    r_by.font.bold = True
    r_by.font.color.rgb = RGBColor(0, 0, 0)

    students = [
        "Navdeep Kaushik  |  S24CSEU2699",
        "Shravan Kumar  |  S24CSEU2677",
        "Ayush Kumar  |  S24CSEU2698",
        "Srijan Pandey  |  S24CSEU2691",
        "Piyush Dagar  |  S24CSEU2680"
    ]
    for s in students:
        p_s = doc.add_paragraph()
        p_s.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_s.paragraph_format.space_after = Pt(3)
        r_s = p_s.add_run(s)
        r_s.font.name = "Aptos"
        r_s.font.size = Pt(10)
        r_s.font.color.rgb = TEXT_BLACK

    p_to = doc.add_paragraph()
    p_to.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_to.paragraph_format.space_before = Pt(32)
    p_to.paragraph_format.space_after = Pt(6)
    r_to = p_to.add_run("Submitted to")
    r_to.font.name = "Aptos"
    r_to.font.size = Pt(11)
    r_to.font.bold = True
    r_to.font.color.rgb = RGBColor(0, 0, 0)

    p_rashmi = doc.add_paragraph()
    p_rashmi.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_rashmi.paragraph_format.space_after = Pt(14)
    r_rashmi = p_rashmi.add_run("Rashmi Ma’am")
    r_rashmi.font.name = "Aptos"
    r_rashmi.font.size = Pt(12)
    r_rashmi.font.bold = True
    r_rashmi.font.color.rgb = RGBColor(0, 0, 0)

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_after = Pt(0)
    r_dept = p_dept.add_run("Department of Computer Science and Engineering")
    r_dept.font.name = "Aptos"
    r_dept.font.size = Pt(9.5)
    r_dept.font.color.rgb = MUTED_GRAY

    # END OF PAGE 1
    doc.add_page_break()

    # =============================================================
    # PAGE 2: SECTIONS 1, 2, 3 (Exact Reference Layout)
    # =============================================================
    add_section_heading("1. Problem Statement and Objectives", space_before=4)
    
    p = doc.add_paragraph()
    p.add_run(
        "Automata and formal languages are easier to understand on paper than to trace in practice. "
        "When an automaton introduces an auxiliary memory like a Last-In-First-Out (LIFO) stack, "
        "students often lose track of stack operations, especially when concurrent input consumption "
        "and ε-moves take place. Non-deterministic Pushdown Automata (NPDA) add another layer of "
        "complexity because multiple valid transitions can exist for the same state, input, and stack top. "
        "Our project addresses this by providing a simple web interface where a user can define a Pushdown "
        "Automaton, enter an input string, and watch in real time how the state, stack contents, and input tape change."
    )
    
    p = doc.add_paragraph()
    p.add_run(
        "The main aim is to make pushdown automata concepts more approachable through hands-on "
        "experimentation rather than relying only on static transition tables and hand-drawn diagrams."
    )

    add_bullet("Create a PDA by specifying states, input symbols, stack symbols, the starting state, bottom stack symbol, accepting states and transitions.")
    add_bullet("Check whether a given string is accepted or rejected.")
    add_bullet("Show the state, stack contents, and remaining tape reached after each input symbol or ε-transition.")
    add_bullet("Support both standard acceptance modes: Acceptance by Final State and Acceptance by Empty Stack.")
    add_bullet("Present the automata visually and flag invalid definitions.")

    add_section_heading("2. Theoretical Specification", space_before=10)
    p = doc.add_paragraph()
    p.add_run(
        "A Pushdown Automaton is defined by the seven-tuple M = (Q, Σ, Γ, δ, q₀, Z₀, F). Here Q is the finite set "
        "of states, Σ is the input alphabet, Γ is the stack alphabet, δ is the transition function, q₀ is the start state, "
        "Z₀ is the initial bottom-of-stack symbol and F is the set of final states. Unlike a finite automaton, a PDA uses "
        "an auxiliary stack to store and manipulate symbols."
    )
    p = doc.add_paragraph()
    p.add_run(
        "For a general PDA, δ: Q × (Σ ∪ {ε}) × Γ → P_finite(Q × Γ*). An ε-transition changes state or alters the stack without "
        "consuming an input symbol. An Instantaneous Description (ID) is denoted by (q, w, γ), representing the active state q, "
        "remaining unread input w, and stack string γ from top to bottom. A string is accepted by final state if, after all input "
        "is processed, the machine enters a state in F. Alternatively, under empty stack acceptance, a string is accepted if the "
        "stack becomes empty upon consuming the entire input."
    )
    p = doc.add_paragraph()
    p.add_run(
        "In a deterministic PDA (DPDA), at most one transition is possible for any configuration, and if an ε-transition exists, "
        "no input-consuming transition is allowed. In an NPDA, multiple choices permit recognizing languages like even palindromes."
    )

    add_section_heading("3. Analysis of Existing Tools", space_before=10)
    p = doc.add_paragraph()
    p.add_run(
        "Tools such as JFLAP already allow learners to build and explore pushdown automata. Automata Tutor is also used "
        "for guided automata exercises. These tools show the value of interactive learning, but they can be more feature-rich "
        "than a beginner needs or require local Java installations. Our project focuses on a straightforward browser-based "
        "workflow: define a PDA, test a string, inspect the stack and state changes, and view step-by-step traces."
    )

    t3_headers = ["Tool", "Relevant feature", "How our project is positioned"]
    t3_data = [
        ["JFLAP", "Automata editing, simulation and conversion", "A focused browser-based alternative for basic PDA tasks"],
        ["Automata Tutor", "Guided automata learning and exercises", "Emphasis on direct visual experimentation"],
        ["PDA Simulator (ours)", "PDA editing, stack animation and dual acceptance", "All core learning steps in one clean interface"]
    ]
    t3_widths = [Inches(1.8), Inches(2.2), Inches(2.37)]
    t3_table = doc.add_table(rows=len(t3_data) + 1, cols=3)
    format_sample_table(t3_table, t3_widths, t3_headers, t3_data)

    # END OF PAGE 2
    doc.add_page_break()

    # =============================================================
    # PAGE 3: SECTIONS 4, 5 (Exact Reference Layout)
    # =============================================================
    add_section_heading("4. System Design", space_before=4)
    
    add_sub_heading("Architecture")
    p = doc.add_paragraph()
    p.add_run(
        "The interface is built with standard web technologies (HTML5, CSS3, and JavaScript) and backed by a Python core engine. "
        "The user enters a PDA definition, which is checked by the validation logic. From there, the simulation engine processes a "
        "test string using a breadth-first search to explore valid computational branches. Visual diagram components display the "
        "automata, physical stack, and simulation results."
    )
    
    p = doc.add_paragraph()
    p.add_run("User input → PDA validation → [Simulation engine / BFS NPDA solver] → Visual diagram and result")

    add_sub_heading("Flowchart")
    p = doc.add_paragraph()
    p.add_run("Start → Enter PDA → Validate definition → If invalid, show errors and revise → If valid, choose simulation mode → Display the result → End.")

    add_sub_heading("UML / logical modules")
    t4_headers = ["Module", "Responsibility"]
    t4_data = [
        ["PDA data type", "Stores states, input alphabet, stack alphabet, start state, final states and transitions"],
        ["Validator", "Checks the automaton definition for syntax and alphabet integrity"],
        ["Simulator", "Calculates stack operations, state movements, BFS exploration and acceptance"],
        ["Determinism checker", "Verifies whether the automaton meets DPDA uniqueness criteria"],
        ["Diagram components", "Draw the PDA state graph, animated vertical stack and tape head"]
    ]
    t4_widths = [Inches(2.3), Inches(4.07)]
    t4_table = doc.add_table(rows=len(t4_data) + 1, cols=2)
    format_sample_table(t4_table, t4_widths, t4_headers, t4_data)

    p_note = doc.add_paragraph()
    p_note.paragraph_format.space_before = Pt(4)
    p_note.add_run(
        "These are logical modules, not necessarily separate object-oriented classes: the web code primarily "
        "uses modular JavaScript functions and data structures."
    )

    add_section_heading("5. UI Mock-up", space_before=10)
    p = doc.add_paragraph()
    p.add_run(
        "The proposed screen places PDA setup controls at the top, a state diagram and animated stack in the center, "
        "and simulation controls below. A student can enter states such as q0, q1 and q2, set the input alphabet to {a, b}, "
        "stack alphabet to {A, Z0}, choose q0 as the start state, Z0 as bottom of stack, and q2 as a final state, and then provide transitions."
    )

    t5_headers = ["PDA setup", "Example value"]
    t5_data = [
        ["States", "q0, q1, q2"],
        ["Input alphabet", "a, b"],
        ["Stack alphabet", "A, Z0"],
        ["Start state", "q0"],
        ["Start stack symbol", "Z0"],
        ["Final state", "q2"],
        ["Input string", "aabb"]
    ]
    t5_widths = [Inches(2.5), Inches(3.87)]
    t5_table = doc.add_table(rows=len(t5_data) + 1, cols=2)
    format_sample_table(t5_table, t5_widths, t5_headers, t5_data)

    p_screen = doc.add_paragraph()
    p_screen.paragraph_format.space_before = Pt(4)
    p_screen.add_run(
        "Suggested screen arrangement: PDA definition → editable transitions → graphical state diagram and animated stack "
        "→ input string and step controls → acceptance/rejection message → detailed trace view."
    )

    # END OF PAGE 3
    doc.add_page_break()

    # =============================================================
    # PAGE 4: SECTIONS 6, 7 (Exact Reference Layout)
    # =============================================================
    add_section_heading("6. Algorithm and Pseudocode", space_before=4)
    
    add_sub_heading("PDA simulation")
    add_numbered("1.", "Set activeConfiguration = initial ID (q0, inputString, [Z0]).")
    add_numbered("2.", "For the current configuration, collect all matching transitions based on state, next input symbol (or ε), and stack top.")
    add_numbered("3.", "Apply the transition: consume symbol (if non-ε), pop stack top, and push specified symbols.")
    add_numbered("4.", "Save active state, stack contents, and unread tape after each move for step-by-step display.")
    add_numbered("5.", "If input is empty and acceptance criteria (final state or empty stack) is satisfied, accept; otherwise reject.")

    add_sub_heading("Determinism verification")
    add_numbered("1.", "For each state q and stack symbol X, check the number of transitions defined on ε and input symbols.")
    add_numbered("2.", "If any (q, symbol, X) has more than one transition, mark automaton as non-deterministic.")
    add_numbered("3.", "If an ε-transition exists for (q, ε, X) alongside any symbol transition (q, a, X), mark as non-deterministic.")
    add_numbered("4.", "If all configurations maintain at most one mutually exclusive transition, classify as DPDA.")

    add_section_heading("7. Manually Solved Validation Example", space_before=10)
    p = doc.add_paragraph()
    p.add_run(
        "Consider the default PDA in the project for language L = { aⁿ bⁿ | n ≥ 1 }, with Q = {q0, q1, q2}, "
        "Σ = {a, b}, Γ = {A, Z0}, start state q0, initial stack symbol Z0, and final state {q2}."
    )

    t7_headers = ["State", "On a", "On b", "On ε"]
    t7_data = [
        ["→ q0", "(q0, AZ0) on Z0, (q0, AA) on A", "(q1, ε) on A", "∅"],
        ["q1", "∅", "(q1, ε) on A", "(q2, Z0) on Z0"],
        ["* q2", "∅", "∅", "∅"]
    ]
    t7_widths = [Inches(1.2), Inches(2.7), Inches(1.3), Inches(1.17)]
    t7_table = doc.add_table(rows=len(t7_data) + 1, cols=4)
    format_sample_table(t7_table, t7_widths, t7_headers, t7_data)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.add_run(
        "Test input: aabb. Initially, the active configuration is (q0, aabb, Z0). "
        "After reading 'a', it pushes A to become (q0, abb, AZ0). "
        "After reading 'a', it pushes A to become (q0, bb, AAZ0). "
        "After reading 'b', it pops A and moves to state q1 with (q1, b, AZ0). "
        "After reading 'b', it pops A to become (q1, ε, Z0). "
        "On empty input ε with stack top Z0, it moves to state q2. "
        "Because q2 is a final state, the string aabb is accepted."
    )

    p = doc.add_paragraph()
    p.add_run("The complete step-by-step configuration trace for this input is:")

    t7_trace_headers = ["Step", "State", "Remaining input", "Stack (Top to Bottom)", "Transition"]
    t7_trace_data = [
        ["0", "q0", "aabb", "Z0", "Initial state"],
        ["1", "q0", "abb", "A, Z0", "δ(q0, a, Z0) → (q0, AZ0)"],
        ["2", "q0", "bb", "A, A, Z0", "δ(q0, a, A) → (q0, AA)"],
        ["3", "q1", "b", "A, Z0", "δ(q0, b, A) → (q1, ε)"],
        ["4", "q1", "ε", "Z0", "δ(q1, b, A) → (q1, ε)"],
        ["5", "q2", "ε", "Z0", "δ(q1, ε, Z0) → (q2, Z0)"]
    ]
    t7_trace_widths = [Inches(0.6), Inches(0.8), Inches(1.5), Inches(1.7), Inches(1.77)]
    t7_trace_table = doc.add_table(rows=len(t7_trace_data) + 1, cols=5)
    format_sample_table(t7_trace_table, t7_trace_widths, t7_trace_headers, t7_trace_data)

    p_accept = doc.add_paragraph()
    p_accept.paragraph_format.space_before = Pt(4)
    p_accept.add_run(
        "State q2 is accepting because it belongs to F. The simulator also accepts aabb, "
        "supporting the correctness of the transition logic for this test."
    )

    # END OF PAGE 4
    doc.add_page_break()

    # =============================================================
    # PAGE 5: SECTION 8 & CONCLUSION (Exact Reference Layout)
    # =============================================================
    add_section_heading("8. Preliminary Prototype and Next Steps", space_before=4)
    
    p = doc.add_paragraph()
    p.add_run(
        "The supplied project already includes an interactive web application, a core PDA simulation engine, "
        "determinism checking logic, validation utilities, and dynamic stack and diagram components. This gives us "
        "a useful starting prototype for M1. However, the source review is not the same as a complete browser test, "
        "so runtime behavior and edge cases still need verification."
    )
    
    p = doc.add_paragraph()
    p.add_run(
        "In the next milestone, we plan to test more examples, especially concurrent ε-transitions, empty strings, "
        "unreachable states and invalid input. We will also improve the interface based on feedback and document the test results."
    )

    add_section_heading("Conclusion", space_before=16)
    p = doc.add_paragraph()
    p.add_run(
        "Our PDA Simulator is intended to turn a difficult theory topic into something students can explore for themselves. "
        "M1 establishes the problem, the underlying theory, the system design and a manually checked example. The existing "
        "code gives us a practical base to build on, while further testing and refinement remain part of the next stage."
    )

    return doc

if __name__ == "__main__":
    doc = create_same_style_report()
    
    # Save as the single authoritative DOCX file
    target_path = "/Users/sunnykaushik/.gemini/antigravity/scratch/pushdown-automata-simulator/Project_12_PDA_Simulator_Milestone_2_Report.docx"
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    doc.save(target_path)
    print(f"5-page exact-style report saved successfully to: {target_path}")
