# Bridge Analyzer

## Purpose

Process **Category C (Bridge) materials** — classroom transcripts, lecture recordings, defense comments, recruitment talks, and student-facing explanations of research — to connect the academic method layer with the mentoring persona layer.

Category A materials show how the mentor thinks academically.
Category B materials show how they interact in supervision.
Category C materials show **how they translate academic thought into student-facing guidance** — the bridge between the two.

---

## Input

You will receive Category C materials for mentor **{name}**:

- Classroom teaching transcripts or recordings
- Course lecture notes
- Thesis defense comments
- Recruitment / introductory talks to prospective students
- Conference pedagogical talks
- Student-facing summaries of the mentor's research approach
- Any material where the mentor is explaining their academic work to students or non-specialists

---

## Extraction Dimensions

### 1. How They Explain Complex Concepts to Students

When explaining theory or methodology to students (not peers), what strategies do they use?

Extract:
- Do they use analogies? What kinds?
- Do they build from concrete examples to abstract principles, or the reverse?
- Do they use diagrams, lists, or prose?
- Do they simplify or refuse to simplify?
- How do they handle student confusion ("I don't understand")?

```
Output format:
concept_explanation_style:
  direction: [concrete→abstract / abstract→concrete / mixed]
  uses_analogy: [yes/no, with examples if yes]
  simplification_willingness: [refuses / selective / frequent]
  response_to_confusion:
    - [description] (source, confidence)
```

---

### 2. How They Frame What Students Should Be Doing

When speaking to students about the research process — what do they emphasize?

Extract:
- What research virtues do they invoke most often (rigor / curiosity / clarity / breadth / depth / honesty)?
- What warnings do they repeat?
- How do they describe the difference between student-level and professional-level work?
- What do they say makes a thesis "pass" vs. "excel"?

```
Output format:
research_framing_for_students:
  emphasized_virtues:
    - [virtue] (source, confidence)
  repeated_warnings:
    - [warning] (source, confidence)
  pass_vs_excel_distinction:
    - [statement] (source, confidence)
```

---

### 3. How They Present Their Own Work to Students

When describing their own research in student-facing contexts — what do they foreground?

Extract:
- Do they emphasize the problem or the method?
- Do they describe their failures or detours?
- Do they present their conclusions as provisional or settled?
- What do they want students to take away from their work?

```
Output format:
self_presentation_to_students:
  emphasis: [problem-first / method-first / finding-first]
  shows_failures: [yes/no/partial]
  conclusion_certainty: [provisional / settled / varies]
  intended_takeaway:
    - [statement] (source, confidence)
```

---

### 4. Signature Pedagogical Moves

Are there distinctive things they do in teaching that connect directly to their academic method?

Extract:
- Do they assign readings specifically chosen to illustrate methodological problems?
- Do they use Socratic questioning in class?
- Do they assign "diagnostic" exercises (e.g., "find a paper and explain why the research question is weak")?
- Do they have a signature assignment type?

```
Output format:
pedagogical_moves:
  - move: [description]
    academic_method_connection: [how it connects to their method layer]
    source: [source type]
    confidence: [high/medium/low]
```

---

### 5. Bridge Phrasings

Phrases that appear in both academic and student-facing contexts — language that connects their research thinking to their supervision style.

Extract:
- Phrases they use when introducing students to their research program
- Phrases from their academic writing that reappear in their teaching
- Phrases that reveal how they translate academic standards into supervision expectations

```
Output format:
bridge_phrasings:
  - phrase: "[the phrase]"
    academic_source: [where it appears in Category A]
    teaching_context: [how/when it appears in teaching]
```

---

## Output Format

Return structured YAML-style output. Include source type and confidence for all items.

Bridge analysis is used by `mentor_builder.md` to:
1. Ensure the persona layer reflects how the mentor actually talks to students, not just how they write academically
2. Fill the voice gap between formal academic positions and informal supervision behavior
3. Identify key phrases that should appear in the mentor skill's outputs

---

## Insufficiency Handling

If no Category C materials are provided:

```
⚠ No Category C materials provided.
  Bridge analysis skipped.
  mentor_builder.md will infer the student-facing register from Category A and B materials only.
  This may result in a persona that sounds too formal (academic writing style) or
  too informal (chat log style) without appropriate calibration.
  Recommend adding: lecture transcripts, defense comments, or teaching notes.
```
