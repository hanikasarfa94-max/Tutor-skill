# Mentor Intake Script

## Purpose

Collect all information needed to begin distilling a mentor. This runs when the user invokes `/create-mentor`.

---

## Opening

```
I'll help you distill a research mentor into a reusable skill.
Let me ask a few questions — you can skip any of them.
```

---

## Question Sequence

### Q1: Mentor Name / Slug

```
What should we call this mentor? (A name, abbreviation, or code — dashes for spaces)

Examples: prof-zhang, methodology-mentor, close-reading-archetype
```

- Accept any string
- Generate slug: lowercase, spaces → dashes, Chinese → pinyin-dashes
- Confirm the slug with the user before proceeding

---

### Q2: Mentor Type

```
What kind of mentor is this?

  1. Specific person — you have materials from a real mentor
  2. Archetype — no single person, building from a type (e.g. "strict progress-driving mentor")
  3. Hybrid — starting from an archetype, then injecting personal materials

(Type a number or describe in your own words)
```

Map to `mentor_type`:
- `specific` — a real person with source materials
- `archetype` — a constructed type without private materials
- `hybrid` — archetype as base, personal materials overlaid

---

### Q3: Discipline and Research Fields

```
What discipline does this mentor work in? What are their main research fields?

Example: Sociology; qualitative methods, urban inequality, migration studies
```

Extract:
- `discipline` — the broad field
- `research_fields` — list of specific areas

---

### Q4: Source Materials

```
What materials do you have? List anything you can share — papers, emails, books,
lecture notes, annotations, chat logs, meeting notes, student recollections.

For each item, roughly describe: what it is, how much there is, and the format.

Example:
- 3 of their papers (PDF)
- ~40 emails from my supervision sessions (text)
- My notes from 6 lab meetings
- A book chapter I scanned (PDF)
```

Categorize each item the user lists into:

| Category | Role | Examples |
|----------|------|---------|
| **A: Academic Thought** | Method layer | papers, books, lectures, interviews, prefaces |
| **B: Mentoring Behavior** | Persona layer | emails, annotations, chat logs, meeting notes, student recollections |
| **C: Bridge** | Connects method to student-facing expression | classroom transcripts, defense comments, recruitment talks |

After the user lists materials, show the categorization for confirmation:

```
Material categorization:

  Category A (Academic Method):
    - [item] → [why it's Category A]
    ...

  Category B (Mentoring Behavior):
    - [item] → [why it's Category B]
    ...

  Category C (Bridge):
    - [item] → [why it's Category C]
    ...

  ⚠ Missing / thin coverage:
    - [which layer has sparse material]
    - [what would help fill the gap]

Does this look right? (confirm / adjust)
```

---

### Q5: Subjective Description

```
In your own words — how would you describe this mentor's academic style and how they work with students?
There's no wrong answer. Include anything that feels distinctive: how they push back, what they care about,
how they respond to vague thinking, what they say in meetings.

(This is optional but greatly improves the result)
```

Flag key phrases for later use in persona construction.

---

### Q6: Skill Emphasis

```
What do you most want this mentor skill to be good at?

  1. Review — critique outlines, drafts, and papers
  2. Diagnose — sharpen research problems and directions
  3. Advance — manage task progression and overcome stagnation
  4. All three equally
  5. Something else (describe)
```

Store as `primary_use_cases` in the mentor profile.

---

## Intake Summary

After all questions, display:

```
Mentor intake summary:

  Name:        {name}
  Slug:        {slug}
  Type:        {mentor_type}
  Discipline:  {discipline}
  Fields:      {research_fields}
  Emphasis:    {primary_use_cases}

  Materials:
    Category A (Method):   {count} items — {brief list}
    Category B (Persona):  {count} items — {brief list}
    Category C (Bridge):   {count} items — {brief list}

  Coverage notes:
    {any warnings about sparse layers}

  Subjective description:
    "{user's description, truncated if long}"

Ready to proceed? (confirm / modify [field])
```

After confirmation, trigger the analysis pipeline in order:
1. `method_analyzer.md` — on Category A materials
2. `mentoring_style_analyzer.md` — on Category B materials
3. `bridge_analyzer.md` — on Category C materials
4. `mentor_builder.md` — integrate all outputs

---

## Missing Material Handling

If a layer has no materials at all:

- **No Category A (Method) materials**: warn the user. The method layer will be inferred from the subjective description and any bridge materials. Mark confidence as `low`. Suggest adding at least one paper or book excerpt.
- **No Category B (Persona) materials**: warn the user. The persona will be inferred from the subjective description and a standard questionnaire (see below). Mark persona confidence as `low`.
- **No Category C (Bridge) materials**: proceed without bridge analysis. The method-to-persona connection will rely on builder inference.

### Persona Questionnaire (when Category B materials are sparse)

If the user has fewer than 2 Category B items, offer this questionnaire:

```
Since we have limited direct mentoring interaction materials, let me ask a few quick questions
to help build the persona. Answer in your own words — skip anything you're not sure about.

1. When a student presents a vague or ill-formed idea, what does this mentor typically do?
2. How do they deliver critical feedback — directly, through questions, indirectly?
3. Do they have a low or high tolerance for hand-waving and vagueness?
4. How do they assign tasks — specific and detailed, or open-ended?
5. How do they respond when a student says "I don't know"?
6. What's a phrase they say often? What's something they'd never say?
7. How do they treat beginners differently from advanced students?
```
