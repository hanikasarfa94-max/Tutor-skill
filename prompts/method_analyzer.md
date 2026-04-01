# Method Analyzer

## Purpose

Extract the **Academic Method Layer** from Category A materials (papers, books, lectures, academic interviews, prefaces, book reviews).

This analysis feeds into `mentor_builder.md` to construct the `method.md` file.

---

## Input

You will receive one or more of the following for mentor **{name}**:

- Academic papers (full text or excerpts)
- Book chapters or monographs
- Lecture notes or transcripts
- Academic interviews or talks
- Prefaces, introductions, afterwords
- Book reviews or review essays

**Extract only what the materials support. Do not infer or generalize beyond the evidence. If a dimension has no evidence, mark it as `(insufficient material — recommend adding [type])`.**

---

## Extraction Principles

### Principle 1: Segment by Function, Not by Chapter

Do not treat whole papers or chapters as single units. Identify functionally distinct passages:

| Passage type | What it reveals |
|-------------|----------------|
| Problem-framing passages | How the mentor defines and delimits research problems |
| Conceptual-definition passages | How they define key terms; tolerance for ambiguity |
| Literature-critique passages | What counts as a good or bad use of prior work |
| Methodological self-explanations | Explicit statements about method preferences |
| Theoretical positioning passages | How they situate themselves in a field |
| Clarifications of common misunderstandings | What they think most scholars get wrong |
| Judgment-heavy concluding passages | How they evaluate the significance of findings |

### Principle 2: Prioritize Direct Statements

When the mentor explicitly states a preference, criterion, or principle — quote it directly. Inferred patterns should be labeled as inferred.

### Principle 3: Look for Recurrence

A single instance of behavior could be incidental. Patterns that appear across multiple works or multiple contexts carry higher confidence.

---

## Extraction Dimensions

### 1. Research Problem Sense

How does this mentor think about what makes a research problem legitimate, interesting, or worth pursuing?

Extract:
- Criteria for a "real" problem vs. a pseudo-problem
- How they distinguish a genuine puzzle from a question that only seems interesting
- Whether they prefer empirically-driven or theoretically-driven problem formation
- How they handle problems that span disciplines

```
Output format:
research_problem_sense:
  - [statement] (source: [paper/lecture/etc], evidence: direct/inferred, confidence: high/medium/low)
  - ...
```

---

### 2. Conceptual Discipline

How strict are they about conceptual precision? How do they handle vague or contested terms?

Extract:
- Do they define key terms early, or let them emerge from context?
- How do they respond to terminological slippage?
- Do they have signature concepts they return to across works?
- What happens when they find a concept being used loosely by others?

```
Output format:
concept_discipline:
  - [statement] (source, evidence, confidence)
  - ...
```

---

### 3. Literature Judgment Rules

How do they evaluate existing literature? What counts as a good engagement with prior work?

Extract:
- Do they value breadth or depth of citation?
- How do they handle contradictory prior findings?
- What do they criticize in how others use the literature?
- Do they prefer engaging with classics or with recent work?
- Do they value methodological critique of prior work?

```
Output format:
literature_judgment_rules:
  - [statement] (source, evidence, confidence)
  - ...
```

---

### 4. Methodology Preferences

What methodological approaches do they favor, and why? What do they find insufficient?

Extract:
- Preferred methods (quantitative / qualitative / mixed / interpretive / comparative / etc.)
- Stated reasons for preferring these methods
- What they critique in methods they don't favor
- How they handle methodological pluralism
- Their stance on triangulation, replication, generalizability

```
Output format:
methodology_preferences:
  - [statement] (source, evidence, confidence)
  - ...
```

---

### 5. Theoretical Stance

How do they position themselves theoretically? What theoretical traditions do they draw from or resist?

Extract:
- Named theoretical frameworks they use or align with
- Theoretical positions they explicitly argue against
- How they handle theory-method integration
- Whether they are theory-building or theory-applying

```
Output format:
theoretical_stance:
  - [statement] (source, evidence, confidence)
  - ...
```

---

### 6. Argument Style

How do they build and structure arguments? What do they consider a well-made argument?

Extract:
- Typical argument structure (inductive / deductive / abductive / comparative)
- How they handle counterarguments
- Whether they front-load conclusions or build toward them
- How they treat evidence: as proof, illustration, or anchor
- How long they dwell on a claim before moving on

```
Output format:
argument_style:
  - [statement] (source, evidence, confidence)
  - ...
```

---

### 7. Critique Patterns

When they criticize other scholars' work — how do they do it? What do they find most objectionable?

Extract:
- Most common types of critique (conceptual confusion, insufficient evidence, wrong method, wrong question, etc.)
- Tone of critique (direct, hedged, ironic, charitable, blunt)
- Whether they distinguish "interesting but wrong" from "not even wrong"
- How they critique methodology vs. interpretation vs. theoretical framing

```
Output format:
critique_patterns:
  - [statement] (source, evidence, confidence)
  - ...
```

---

### 8. Expectations for Student Work

Based on any explicit statements, prefaces, or teaching materials — what standards do they hold for student-produced work?

Extract:
- What they say a good thesis / paper / proposal must do
- Common mistakes they warn against
- Minimum threshold for "ready to submit" or "ready to discuss"
- What they consider signs of intellectual maturity in a student

```
Output format:
student_work_expectations:
  - [statement] (source, evidence, confidence)
  - ...
```

---

## Discipline-Specific Dimensions

After completing the eight universal dimensions above, run the relevant section below based on the mentor's discipline. These supplement — do not replace — the universal dimensions.

---

### 🧑‍💻 Humanities (Literature, History, Philosophy, Languages, Cultural Studies)

**Textual and Archival Method:**
- How do they treat primary sources? (close reading / distant reading / archival / philological)
- Do they read against the grain, or with the text's own logic first?
- How do they handle translation, attribution, or contested authorship?
- What is their stance on historicism vs. presentism?

**Interpretation Standards:**
- What distinguishes a "reading" from a "misreading" for them?
- How do they evaluate interpretive claims that can't be falsified?
- Do they require interpretations to be exhaustive, or is partiality acceptable?
- How do they handle the relationship between form and content?

**Canon and Field Positioning:**
- Do they engage primarily with canonical texts or marginal/recovering work?
- How do they situate themselves in theoretical debates (structuralism, post-structuralism, new historicism, etc.)?

```
Output format:
discipline_specific (humanities):
  primary_source_approach: [description]
  interpretation_standard: [statement] (source, evidence, confidence)
  theory_relationship: [description]
```

---

### 🔬 Empirical Social Sciences (Sociology, Political Science, Economics, Psychology, Education)

**Research Design Standards:**
- What counts as valid causal inference for them? (experiments / natural experiments / process tracing / comparative / statistical control)
- How do they handle the internal vs. external validity tradeoff?
- What is their stance on large-N vs. small-N research?
- How do they treat measurement validity — do they construct new measures or use established ones?

**Data and Evidence:**
- What types of data do they find most compelling? (survey / administrative / ethnographic / archival / experimental)
- How do they handle missing data, selection bias, or confounding?
- What is their standard for "enough evidence" to support a claim?

**Theory-Data Relationship:**
- Do they test existing theory, build new theory, or both?
- How do they treat null findings?
- What do they say about statistical significance vs. practical significance?

```
Output format:
discipline_specific (empirical_social_science):
  causal_inference_standard: [description]
  preferred_evidence_types: [list]
  theory_data_relationship: [statement] (source, evidence, confidence)
```

---

### 📜 Interpretive / Qualitative Social Sciences (Anthropology, Ethnography, Qualitative Sociology, STS)

**Fieldwork and Positionality:**
- How do they handle researcher positionality and reflexivity?
- What is their standard for fieldwork depth / duration?
- How do they treat the relationship between researcher and informant?

**Generalization:**
- Do they value analytic generalization, thick description, or theoretical generalization?
- How do they respond to "but is this case typical?"
- What is their stance on comparison across cases?

**Writing and Representation:**
- Do they use first person? How do they handle the authority of the ethnographic voice?
- How do they present contradictory evidence from fieldwork?

```
Output format:
discipline_specific (interpretive_social_science):
  positionality_stance: [description]
  generalization_standard: [statement] (source, evidence, confidence)
  representation_approach: [description]
```

---

### ⚗️ Natural Sciences and Engineering (Physics, Biology, Chemistry, CS, Engineering)

**Experimental Standards:**
- What do they require for a result to be "publishable"? (replication / statistical power / effect size / mechanistic explanation)
- How do they treat negative results?
- What is their stance on computational / simulation evidence vs. experimental evidence?

**Modeling and Theory:**
- Do they prefer minimal / parsimonious models, or models that capture full complexity?
- How do they validate models against empirical data?
- What is their stance on interpretability vs. performance in computational work?

**Reproducibility:**
- Do they require code / data to be published alongside results?
- How do they handle results that can't be independently reproduced?

```
Output format:
discipline_specific (natural_science_engineering):
  experimental_standard: [description]
  model_preference: [statement] (source, evidence, confidence)
  reproducibility_stance: [description]
```

---

### 📐 Formal / Theoretical Fields (Mathematics, Formal Linguistics, Theoretical CS, Logic)

**Proof and Rigor Standards:**
- What constitutes a valid proof for them? (constructive / non-constructive / probabilistic)
- How do they handle informal or sketch arguments?
- What is their stance on computer-assisted proofs?

**Scope of Claims:**
- How carefully do they circumscribe the conditions under which a theorem or result holds?
- How do they treat counterexamples — as fatal or as boundary conditions?

**Exposition:**
- Do they value elegant proofs over complete ones?
- How do they handle the gap between formal rigor and intuitive explanation?

```
Output format:
discipline_specific (formal_theoretical):
  proof_standard: [description]
  claim_scope_precision: [statement] (source, evidence, confidence)
  elegance_vs_completeness: [description]
```

---

### 🏥 Professional Fields (Law, Medicine, Public Policy, Clinical Psychology, Management)

**Practitioner-Scholar Tension:**
- How do they handle the tension between academic rigor and practical applicability?
- Do they value research that is immediately actionable, or are they comfortable with foundational work?

**Evidence Hierarchy:**
- What is their stance on randomized trials vs. observational evidence vs. case studies vs. expert judgment?
- How do they treat professional guidelines, precedent, or regulation as evidence?

**Audience and Impact:**
- Do they write primarily for academic peers, policymakers, practitioners, or all three?
- How do they define "impact" in their field?

```
Output format:
discipline_specific (professional_field):
  practice_rigor_balance: [description]
  evidence_hierarchy: [statement] (source, evidence, confidence)
  impact_definition: [description]
```

---

## Output Format

Return structured YAML-style output with all eight universal dimensions plus the applicable discipline-specific section. For each item, include:

- The extracted statement (concise but precise)
- Source type: `paper` / `book` / `lecture` / `interview` / `preface` / `review`
- Evidence strength: `direct` (explicitly stated) / `inferred` (pattern observed)
- Confidence: `high` (appears in 3+ sources or very explicit) / `medium` / `low` (single instance or indirect)

Example:

```yaml
research_problem_sense:
  - statement: "Prefers problems that expose contradictions between theoretical expectation and empirical pattern"
    source: paper
    evidence: direct
    confidence: high

  - statement: "Skeptical of problems framed purely around 'gaps in the literature' without independent motivation"
    source: lecture
    evidence: inferred
    confidence: medium
```

---

## Insufficiency Handling

For any dimension with fewer than one item of evidence:

```yaml
literature_judgment_rules:
  - statement: "(insufficient material — recommend adding: annotated bibliographies, course syllabi, book reviews)"
    source: none
    evidence: none
    confidence: none
```

Do not fill gaps by guessing. The builder stage handles inference; this stage records only what the materials say.
