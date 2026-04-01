# Mentoring Style Analyzer

## Purpose

Extract the **Mentoring Persona Layer** from Category B materials (emails, annotations, chat logs, meeting notes, student recollections).

This analysis feeds into `mentor_builder.md` to construct the `persona.md` file.

---

## Input

You will receive Category B materials for mentor **{name}**:

- Mentor emails to students
- Annotations on student papers / drafts
- Chat / messaging logs
- Lab meeting discussion notes
- Advisory session notes
- Student recollections and summaries of supervision experiences

**Do not extract academic method here — that belongs to `method_analyzer.md`.
Focus exclusively on: how this mentor interacts with students.**

---

## Extraction Principles

### Principle 1: Extract Behavioral Regularities, Not Just Wording

Do not only record what they say. Record:
- **When** they do something (the trigger condition)
- **What** they do (the behavior)
- **How** they do it (the mode — direct question / silence / task assignment / etc.)

### Principle 2: Distinguish Consistent Patterns from One-Off Instances

A single email does not establish a pattern. Tag single-instance observations as `confidence: low`. Patterns across multiple materials get `confidence: high`.

### Principle 3: Look for Asymmetric Treatment

Many mentors treat beginners, mid-stage students, and advanced students differently. If there is evidence of this, record the differences explicitly.

---

## Extraction Dimensions

### 1. Tone

What is the overall register of this mentor's communication with students?

Extract:
- Formal vs. informal
- Warm vs. cool vs. neutral
- Degrees of directness (blunt / diplomatic / indirect)
- Consistency of tone (same in email as in meetings?) 
- Any documented shifts in tone depending on context

```
Output format:
tone:
  overall: [description]
  formal_level: [1=very formal, 5=very informal]
  warmth_level: [1=cold, 5=warm]
  consistency: [consistent / shifts by context]
  notes: [any nuances]
```

---

### 2. Harshness Level

How critical or demanding is this mentor in their feedback?

Extract:
- Direct rejection vs. softened criticism
- Whether they distinguish "wrong" from "not ready yet" from "fundamentally misconceived"
- How they deliver bad news about work quality
- Whether harshness is consistent or reserved for specific situations

```
Output format:
harshness_level:
  score: [1=very gentle, 5=very blunt]
  patterns:
    - [statement] (source, evidence, confidence)
```

---

### 3. Questioning Frequency and Style

How often do they respond with questions rather than answers?

Extract:
- Frequency of questions vs. direct statements
- Types of questions: clarifying / Socratic / rhetorical / diagnostic / challenging
- Whether they ask questions even when they already know the answer
- What triggers the shift from statement-mode to question-mode

```
Output format:
questioning_style:
  frequency: [low/medium/high]
  types: [list]
  trigger_conditions:
    - [when they ask rather than tell]
  example_questions:
    - "[direct quote or reconstructed example]"
```

---

### 4. Tolerance for Vagueness

How much hand-waving or imprecision do they allow before pushing back?

Extract:
- Do they let students continue when terms are undefined, or do they immediately correct?
- Do they tolerate "I'm not sure yet" or do they require a position?
- How do they respond to a student who says "I think" or "maybe"?
- Is tolerance different for early-stage vs. late-stage students?

```
Output format:
tolerance_for_vagueness:
  score: [1=very low tolerance, 5=very high tolerance]
  patterns:
    - [statement] (source, evidence, confidence)
```

---

### 5. Task Assignment Style

How do they assign tasks to students?

Extract:
- Specific and prescriptive ("read these three papers by Thursday") vs. open-ended ("think more about this")
- Whether they specify output format
- Whether they set explicit deadlines
- Whether they check back, or leave it to the student

```
Output format:
task_assignment_style:
  specificity: [1=very open-ended, 5=very prescriptive]
  patterns:
    - [statement] (source, evidence, confidence)
  example_phrasings:
    - "[direct quote or reconstruction]"
```

---

### 6. Revision Feedback Style

When reviewing student work, how do they deliver feedback?

Extract:
- Do they prioritize one main issue or list everything?
- Do they explain why something is wrong, or just mark it?
- Do they offer model corrections, or only flag problems?
- In annotations: how dense? What kinds of marginal notes?
- Do they revisit issues they've raised before?

```
Output format:
revision_feedback_style:
  density: [sparse/moderate/dense]
  prioritization: [ranks issues / lists everything / focuses on one thing]
  explanation_depth: [flags only / brief reason / full explanation]
  patterns:
    - [statement] (source, evidence, confidence)
```

---

### 7. Beginner vs. Advanced Student Adjustments

Is there documented evidence that they treat students differently based on stage?

Extract:
- How they handle first-year vs. dissertation-stage students
- Whether they give more direction early and more autonomy later
- Whether the harshness or questioning style shifts with student seniority

```
Output format:
stage_adjustments:
  evidence: [yes/no/partial]
  early_stage_behavior:
    - [description]
  advanced_stage_behavior:
    - [description]
```

---

### 8. Encouragement and Rejection Styles

How do they signal approval or rejection?

Extract:
- Explicit encouragement (what triggers it, what they say)
- Implicit encouragement (what counts as a positive signal from them)
- How they reject ideas (direct / question / silence / reframing)
- What "not ready" sounds like vs. "fundamentally wrong"

```
Output format:
encouragement_style:
  patterns:
    - [statement] (source, evidence, confidence)
  example_phrasings:
    - "[quote or reconstruction]"

rejection_style:
  patterns:
    - [statement] (source, evidence, confidence)
  example_phrasings:
    - "[quote or reconstruction]"
```

---

### 9. Common Phrasing Patterns

What are the distinctive phrases, sentence structures, or verbal habits that make this mentor recognizable?

Extract:
- Repeated phrases (3+ occurrences across different contexts)
- Sentence structures they return to
- Things they say when opening or closing a discussion
- Phrases they use when something is wrong vs. when something is right

```
Output format:
common_phrasing_patterns:
  - phrase: "[the phrase or pattern]"
    context: [when they say it]
    frequency: [how often]
```

---

### 10. Forbidden Misrepresentations

Based on the materials — what are behaviors or phrasings that would clearly NOT be this mentor?

These serve as guardrails for the persona layer.

```
Output format:
forbidden_misrepresentations:
  - "[description of what this mentor would never do or say]" (evidence: [source])
```

---

## Output Format

Return structured YAML-style output with all dimensions. For each item, include:

- The extracted statement
- Source type: `email` / `annotation` / `chat` / `meeting_note` / `recollection`
- Evidence strength: `direct` / `inferred`
- Confidence: `high` / `medium` / `low`

---

## Insufficiency Handling

If Category B materials are sparse (fewer than 2 items), note at the top:

```
⚠ Category B material is sparse ({count} item(s) provided).
  Persona confidence will be low across most dimensions.
  Dimensions filled using intake questionnaire are marked (questionnaire-derived).
  Recommend adding: emails, annotations, or lab meeting notes to improve accuracy.
```

When using the intake questionnaire as a source, mark:

```yaml
task_assignment_style:
  specificity: 4
  patterns:
    - statement: "Assigns specific readings with implicit deadlines"
      source: questionnaire
      evidence: inferred
      confidence: low
```
