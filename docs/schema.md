# Schema Reference

This document defines the canonical schemas for all data structures used in the tutor-skill system.

---

## 1. meta.json

Stored at `mentors/generated/{slug}/meta.json`.

```json
{
  "slug": "prof-zhang",
  "mentor_name": "Prof. Zhang",
  "mentor_type": "specific | archetype | hybrid",
  "discipline": "Sociology",
  "research_fields": ["qualitative methods", "urban inequality", "migration"],
  "core_stance_summary": "One-sentence summary of this mentor's academic positioning",
  "primary_use_cases": ["review", "diagnose", "advance"],
  "version": "1.0.0",
  "created_at": "2026-04-01T00:00:00Z",
  "last_updated": "2026-04-01T00:00:00Z",
  "material_sources": {
    "category_a": ["3 papers (PDF)", "1 book chapter"],
    "category_b": ["40 emails", "6 lab meeting notes"],
    "category_c": ["lecture transcript (Spring 2023)"]
  },
  "confidence": {
    "method_layer": "high | medium | low",
    "persona_layer": "high | medium | low",
    "bridge_used": true
  },
  "correction_log": [
    {
      "date": "2026-04-10T00:00:00Z",
      "type": "rule_change | addition | deletion | stylistic | rollback",
      "layer": "method | persona | voice",
      "dimension": "questioning_style",
      "change": "Changed harshness score from 3 to 4",
      "reason": "User observed they are consistently blunter in person",
      "version": "1.0.1"
    }
  ]
}
```

---

## 2. method.md — Method Layer Schema

Canonical fields in the YAML section of method.md:

```yaml
research_problem_sense:
  - statement: string
    source: paper | book | lecture | interview | preface | review
    evidence: direct | inferred
    confidence: high | medium | low

concept_discipline:
  - statement: string
    source: ...
    evidence: ...
    confidence: ...

literature_judgment_rules:
  - statement: string
    ...

methodology_preferences:
  - statement: string
    ...

theoretical_stance:
  - statement: string
    ...

argument_style:
  - statement: string
    ...

critique_patterns:
  - statement: string
    ...

student_work_expectations:
  - statement: string
    ...
```

---

## 3. persona.md — Persona Layer Schema

Canonical fields in the YAML section of persona.md:

```yaml
tone:
  overall: string
  formal_level: 1-5   # 1=very formal, 5=very informal
  warmth_level: 1-5   # 1=cold, 5=warm
  consistency: consistent | shifts_by_context

harshness_level:
  score: 1-5          # 1=very gentle, 5=very blunt
  patterns:
    - statement: string
      source: email | annotation | chat | meeting_note | recollection | questionnaire
      evidence: direct | inferred
      confidence: high | medium | low

questioning_style:
  frequency: low | medium | high
  types: [clarifying, socratic, rhetorical, diagnostic, challenging]
  trigger_conditions:
    - string
  example_questions:
    - string

tolerance_for_vagueness:
  score: 1-5          # 1=very low tolerance, 5=very high
  patterns:
    - statement: string
      ...

task_assignment_style:
  specificity: 1-5    # 1=very open-ended, 5=very prescriptive
  patterns:
    - statement: string
      ...
  example_phrasings:
    - string

revision_feedback_style:
  density: sparse | moderate | dense
  prioritization: ranks_issues | lists_everything | focuses_on_one_thing
  explanation_depth: flags_only | brief_reason | full_explanation
  patterns:
    - statement: string
      ...

stage_adjustments:
  evidence: yes | no | partial
  early_stage_behavior:
    - string
  advanced_stage_behavior:
    - string

encouragement_style:
  patterns:
    - statement: string
      ...
  example_phrasings:
    - string

rejection_style:
  patterns:
    - statement: string
      ...
  example_phrasings:
    - string

common_phrasing_patterns:
  - phrase: string
    context: string
    frequency: string

forbidden_misrepresentations:
  - string
```

---

## 4. memory.md — Guidance Memory Schema

```yaml
student_profile:
  research_topic: string
  current_stage: string  # e.g. "early literature review", "dissertation writing", "proposal stage"
  strengths:
    - string
  recurring_issues:
    - string

current_tasks:
  - task: string
    assigned_date: ISO date string
    due_date: ISO date string | null
    status: pending | in_progress | completed

pending_deliverables:
  - item: string
    context: string

previous_feedback:
  - date: ISO date string
    issue: string
    mentor_response: string
    status: unresolved | partial | resolved

mentor_emphases:
  - string   # things this mentor has stressed repeatedly across sessions

session_history:
  - date: ISO date string
    mode: diagnose | review | advance | other
    summary: string
    key_outputs:
      - string
```

---

## 5. Segment Metadata Schema

Used internally by parsers. Each extracted segment carries:

```yaml
text: string
source_file: string
source_type: paper | book | lecture | email | annotation | chat | meeting_note | recollection
role_weight: method | persona | bridge
candidate_types: [string]  # e.g. [problem_framing, literature_critique]
confidence: high | medium | low
evidence_strength: direct | inferred
section_heading: string
page_number: int | null
```

---

## 6. Correction Entry Schema

```yaml
date: ISO datetime
type: rule_change | addition | deletion | stylistic | rollback
layer: method | persona | voice
dimension: string  # which field was changed
change: string     # description of the change
reason: string     # user's stated reason
version: string    # version number after this correction
```
