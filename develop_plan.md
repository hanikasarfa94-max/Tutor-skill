# Research Mentor Skill Development Document (Claude Code Version)

## 1. Project Overview

### 1.1 Project Name

**Research Mentor Skill**

### 1.2 Project Goal

Build a **research mentor-oriented Skill** that runs on the **Claude Code Skill framework** and is capable of distilling the following aspects of university research mentors (master's supervisors, PhD supervisors, academic mentors, methodology mentors, etc.):

1. **Academic thought and academic positioning**: research problem sense, conceptual framework, theoretical orientation, methodological preference, evaluation criteria.
2. **Mentoring style and interaction style**: ways of criticizing, questioning, assigning tasks, handling students at different stages, and linguistic style.
3. **Guidance memory and continuity**: persistent tracking of a student's historical issues, current stage, recurring weaknesses, and ongoing tasks.

This Skill is not meant to merely imitate a mentor's tone. It is meant to distill a reusable **mentor-like working system** capable of performing the following tasks:

* Research problem diagnosis
* Review of papers, outlines, and paragraphs
* Literature reading and research path guidance
* Task decomposition and stage progression
* Mentoring-style follow-up and review

---

## 2. Product Positioning

### 2.1 Core Positioning

This project is a **research mentor distiller + mentor Skill generator**.

It consists of two parts:

1. **Create Mentor Skill**: distill a specific mentor from source materials and generate a Skill.
2. **Use Mentor Skill**: let users interact with the generated mentor Skill and receive feedback close to that mentor's academic method and mentoring style.

### 2.2 Non-Goals

This project does **not** aim to:

* Fully replicate a real mentor's complete personality
* Function as a legal or social substitute for a real academic advisor
* Perform romance-style or emotional companion roleplay
* Fully automate material selection from the start
* Train model weights directly

The goal is to **generate a structured, correctable, and iterative research mentor Skill within the Claude Code Skill framework**.

---

## 3. Target Users and Use Cases

### 3.1 Target Users

1. Graduate students, senior undergraduates, and doctoral students
2. Users who need academic guidance, writing feedback, and research progression support
3. Developers and researchers who want to distill a supervisor, a mentor type, or a broader mentor archetype
4. Developers building academic reading agents or research assistance agents

### 3.2 Core Use Cases

#### Use Case A: Distilling a Specific Mentor

The user has access to a mentor's papers, books, lectures, emails, annotations, or supervision records, and wants to generate a Skill in that mentor's style.

#### Use Case B: Distilling a Mentor Archetype

The user does not have sufficient private materials from one specific mentor, but wants to construct templates such as a “close-reading mentor,” a “methodology-focused mentor,” or a “strict progress-driving mentor.”

#### Use Case C: Long-Term Research Guidance

The user wants the Skill to continuously track their research topic, task progress, recurring weaknesses, and stage goals, thereby creating continuity of mentorship.

---

## 4. Core Design Principles

### 4.1 Separate Method from Style

The system must explicitly distinguish between:

* **Academic Method**: the mentor's research problem sense, methodology, judgment criteria, and conceptual discipline.
* **Mentoring Style / Persona**: how the mentor speaks to students, pushes them forward, criticizes their work, and adjusts expectations.

### 4.2 Explicitly Model Material Heterogeneity

Different kinds of source material carry different signals:

* Papers and books are best for extracting academic method and positioning.
* Conversations, emails, and annotations are best for extracting mentoring style and interaction patterns.
* Lectures, teaching materials, and interviews often function as a bridge between method and student-facing explanation.

Therefore, all source materials should **not** be dumped into one prompt indiscriminately. They must be processed through separate analytical pipelines.

### 4.3 A Mentor Skill Is a Working System, Not a Single Prompt

The system must include:

* intake (material intake)
* analyzer (layered analysis)
* builder (Skill generation)
* correction (correction/update)
* versioning (archive and rollback)

### 4.4 Support Incremental Correction

The user must be able to say things like:

* “This does not sound like them.”
* “They care more about conceptual boundaries and would not conclude that quickly.”
* “They would not criticize in that tone.”
* “They care more about evidential grounding than superficial structure.”

The system must support **incremental merge**, not only full regeneration.

---

## 5. Overall Architecture

The project consists of three layers:

### 5.1 Method Layer

Responsible for extracting:

* research problem sense
* academic positioning
* methodological preferences
* literature evaluation criteria
* conceptual discipline
* argumentative progression style
* research-stage judgment logic

Primary material sources:

* papers
* books
* course lectures
* academic interviews
* book reviews
* prefaces / introductions / reflective summaries

### 5.2 Mentoring Persona Layer

Responsible for extracting:

* tone of interaction
* degree of harshness
* questioning frequency
* tolerance for vagueness
* task assignment style
* differences in how the mentor treats beginners versus advanced students
* review and revision habits
* forms of encouragement and rejection

Primary material sources:

* emails
* annotations
* chat logs
* lab meeting notes
* lecture transcripts
* student recollections and summaries

### 5.3 Guidance Memory Layer

Responsible for maintaining:

* the student's research topic
* current stage goals
* completed tasks
* recurring problems and repeated errors
* unresolved issues previously pointed out
* current draft status
* mentor emphases repeated across time

This layer is not fully distilled from mentor materials at build time. It is accumulated continuously during usage.

---

## 6. Data Sources and Distillation Strategy

### 6.1 Data Source Categories

#### Category A: Academic Thought Materials

Primarily used to distill the Method Layer.

Includes:

* academic papers
* books and monographs
* lecture notes
* academic talks
* public interviews
* introductions, prefaces, afterwords, book reviews

#### Category B: Mentoring Behavior Materials

Primarily used to distill the Persona Layer.

Includes:

* annotations on student papers
* mentor emails
* lab meeting discussion notes
* topic discussion records
* advisory feedback notes
* chat messages with students

#### Category C: Bridge Materials

Used to connect Method and Persona.

Includes:

* classroom teaching transcripts
* lecture transcriptions
* recruitment talks
* thesis defense comments
* student summaries of the mentor's supervision style

### 6.2 Core Distillation Principles

#### Principle 1: Do Not Dump Entire Books Blindly

Entire books should not be fed wholesale into a generator. Extraction should happen at the segment level.

#### Principle 2: Extract by Function

Papers and books should be segmented into functional units such as:

* problem-framing passages
* conceptual-definition passages
* literature-critique passages
* methodological self-explanations
* theoretical positioning passages
* clarifications of common misunderstandings
* judgment-heavy concluding passages

#### Principle 3: Extract Behavioral Regularities from Interaction Materials

Do not only extract wording patterns. Also extract:

* when the mentor questions
* when the mentor directly rejects a claim
* when the mentor demands more materials
* how the mentor judges that a student has “not thought it through”
* how the mentor assigns next-week tasks

#### Principle 4: Every Segment Must Be Tagged

Every extracted segment must include metadata such as:

* source_type: paper / book / lecture / email / annotation / chat / meeting_note / recollection
* role_weight: method / persona / bridge
* confidence: high / medium / low
* evidence_strength: direct / inferred

---

## 7. Target Capabilities

The generated mentor Skill should support at least the following capabilities:

### 7.1 Research Problem Diagnosis

Input: research idea, topic, vague confusion.
Output:

* what the real problem is
* why the problem is not yet well-formed
* what prerequisites are missing
* what should be done first
* what should not be done yet

### 7.2 Outline / Draft Review

Input: abstract, outline, paragraph, chapter draft.
Output:

* core defect
* severe problems
* secondary problems
* revision priority order
* actionable revision suggestions

### 7.3 Literature Guidance

Input: research topic, reading list, literature notes.
Output:

* what should be read
* what should be read first and later
* how notes should be taken
* which disputes are central
* what kind of reading task corresponds to the current blockage

### 7.4 Stage Progression

Input: current status, procrastination, stagnation, stage goal.
Output:

* diagnosis of current stage
* source of stagnation
* minimal next step
* this week's task
* next reporting requirement

### 7.5 Long-Term Mentoring

Input: multi-turn interaction history.
Output:

* feedback tailored to the user's history
* reminders about recurring unresolved issues
* consistency correction against prior advice

---

## 8. Interaction Mode Design

The generated Skill should support three primary modes:

### Mode 1: Diagnose

Suitable for unclear problems, unstable topics, and confused research direction.

Fixed output structure:

1. What your real problem is
2. Why it is not yet established
3. What prerequisites are missing
4. What you should do next
5. What you should not do yet

### Mode 2: Review

Suitable for reviewing outlines, papers, literature reviews, and paragraphs.

Fixed output structure:

1. The most central problem
2. Severe defects
3. Secondary defects
4. Revision priority order
5. Sample-level revision suggestions

### Mode 3: Advance

Suitable for procrastination, stagnation, and stage management.

Fixed output structure:

1. Current stage diagnosis
2. Root cause of stagnation
3. Minimal next-step action for this week
4. Deliverable format
5. Next checkpoint

---

## 9. Claude Code Skill Form

### 9.1 Suggested Project Structure

```text
create-mentor-skill/
├── SKILL.md
├── prompts/
│   ├── intake.md
│   ├── method_analyzer.md
│   ├── mentoring_style_analyzer.md
│   ├── bridge_analyzer.md
│   ├── mentor_builder.md
│   ├── merger.md
│   └── correction_handler.md
├── tools/
│   ├── paper_parser.py
│   ├── annotation_parser.py
│   ├── email_parser.py
│   ├── lecture_parser.py
│   ├── chat_parser.py
│   ├── skill_writer.py
│   └── version_manager.py
├── mentors/
│   ├── generated/
│   └── archives/
├── docs/
│   ├── PRD.md
│   ├── schema.md
│   └── examples.md
├── tests/
│   ├── intake_cases.md
│   ├── builder_cases.md
│   ├── correction_cases.md
│   └── regression_cases.md
└── requirements.txt
```

### 9.2 Directory Responsibilities

#### SKILL.md

The Claude Code entry file. Defines trigger behavior, scope, and execution flow.

#### prompts/

Stores prompt templates for each pipeline stage.

#### tools/

Contains material parsers, output writers, and versioning tools.

#### mentors/generated/

Stores generated mentor Skill files.

#### mentors/archives/

Stores historical versions for rollback.

---

## 10. Prompt Pipeline Design

### 10.1 intake.md

Responsibility: collect all information needed to create a mentor Skill.

Inputs should include:

* mentor name / mentor type
* target use case
* list of source materials
* user's subjective description of the mentor
* desired emphasis of the Skill (more review-oriented / more progression-oriented / more theory-oriented)

Outputs should include:

* material categorization result
* preliminary mentor profile
* missing information checklist
* assignment of follow-up analysis tasks

### 10.2 method_analyzer.md

Responsibility: extract Academic Method from papers, books, and lectures.

Target output fields:

* research_problem_sense
* concept_discipline
* literature_judgment_rules
* methodology_preferences
* theoretical_stance
* argument_style
* critique_patterns
* expectations_for_student_work

### 10.3 mentoring_style_analyzer.md

Responsibility: extract mentoring style from emails, annotations, chats, and meeting notes.

Target output fields:

* tone
* harshness_level
* questioning_frequency
* tolerance_for_vagueness
* task_assignment_style
* revision_feedback_style
* beginner_vs_advanced_adjustments
* encouragement_style
* rejection_style

### 10.4 bridge_analyzer.md

Responsibility: process materials such as lectures, public talks, and defense comments that sit between method and interaction.

Purpose:

* connect academic thought with student-facing expression
* identify how the mentor explains theory to students
* extract the mentor's way of explaining complex concepts

### 10.5 mentor_builder.md

Responsibility: integrate outputs from all analyzers and generate the final mentor Skill configuration.

Should generate:

* mentor profile
* method rules
* persona rules
* default interaction modes
* memory schema
* failure guardrails

### 10.6 correction_handler.md

Responsibility: receive user corrections and update the Skill.

Must support:

* local correction
* overwrite correction
* incremental supplementation
* stylistic correction
* version note recording

### 10.7 merger.md

Responsibility: merge new materials into previous analysis results.

Requirements:

* preserve existing structure
* avoid crude overwriting
* new evidence outweighs old inference
* direct evidence outranks indirect inference

---

## 11. Structured Schema Design

### 11.1 Mentor Profile Schema

```yaml
mentor_name: string
mentor_type: academic_supervisor | methodology_mentor | writing_mentor | template
discipline: string
research_fields: [string]
core_stance_summary: string
primary_use_cases: [string]
confidence_overall: high | medium | low
```

### 11.2 Method Schema

```yaml
research_problem_sense:
  - string
concept_discipline:
  - string
literature_judgment_rules:
  - string
methodology_preferences:
  - string
theoretical_stance:
  - string
argument_style:
  - string
critique_patterns:
  - string
student_work_expectations:
  - string
```

### 11.3 Persona Schema

```yaml
tone: string
harshness_level: 1-5
questioning_frequency: 1-5
tolerance_for_vagueness: 1-5
task_assignment_style:
  - string
revision_feedback_style:
  - string
encouragement_style:
  - string
rejection_style:
  - string
common_phrasing_patterns:
  - string
forbidden_misrepresentations:
  - string
```

### 11.4 Guidance Memory Schema

```yaml
student_profile:
  research_topic: string
  stage: string
  strengths: [string]
  recurring_issues: [string]
current_tasks:
  - string
pending_deliverables:
  - string
previous_feedback:
  - issue: string
    status: unresolved | partial | resolved
mentor_emphases:
  - string
```

---

## 12. Tool Module Design

### 12.1 paper_parser.py

Functions:

* parse papers and book text
* chunk by section / paragraph
* label document-style passages
* identify probable problem-framing, conceptual-definition, method-explanation, and conclusion-judgment segments

### 12.2 annotation_parser.py

Functions:

* parse mentor annotations
* extract criticism actions and revision instructions
* identify recurring review patterns

### 12.3 email_parser.py

Functions:

* extract task instructions, judgment tone, and pacing requirements from mentor emails
* distinguish administrative emails from advisory emails

### 12.4 lecture_parser.py

Functions:

* parse lecture notes / transcripts
* extract how the mentor explains complex concepts to students
* serve as bridge-layer material

### 12.5 chat_parser.py

Functions:

* parse instant-message conversations
* extract questioning patterns, rejection patterns, encouragement patterns, and task-assignment patterns

### 12.6 skill_writer.py

Functions:

* write structured results into generated mentor Skill files
* generate markdown / yaml / json outputs as needed

### 12.7 version_manager.py

Functions:

* save version numbers
* write update notes
* support rollback and archival

---

## 13. Runtime Behavior Rules

The generated mentor Skill must follow these behavior rules:

### 13.1 Diagnose First, Answer Later

The default behavior should not be to immediately provide conclusions. It should first identify:

* whether the problem is well-formed
* whether multiple tasks are being conflated
* whether the user is at the right stage for that problem

### 13.2 Distinguish Severe Problems from Secondary Problems

During review, the Skill must rank issues instead of presenting a flat list.

### 13.3 Always Try to Provide an Actionable Next Step

Each response should include at least one concrete next step, not only abstract evaluation.

### 13.4 Preserve the Mentor's Academic Discipline

The Skill must not sacrifice conceptual rigor merely to sound agreeable.

### 13.5 Avoid Inventing Views Not Supported by the Source Materials

When evidence is weak, the Skill should reduce assertion strength explicitly.

---

## 14. Failure Guardrails and Risk Control

### 14.1 Risk: Academic Writings Overwhelm Mentoring Style

Solution: analyze Method and Persona in separate pipelines and control weighting during the Builder stage.

### 14.2 Risk: Too Few Interaction Materials Lead to Persona Distortion

Solution: allow user-supplied mentor questionnaires and lower persona confidence when evidence is sparse.

### 14.3 Risk: Output Sounds Too Academic and Not Like Student-Facing Mentorship

Solution: use bridge materials such as lectures, talks, and defense comments to connect theory with student-facing expression.

### 14.4 Risk: Uneven Material Quality

Solution: tag each segment with confidence and evidence strength.

### 14.5 Risk: No Way to Correct After Initial Build

Solution: include correction + merger + versioning from the outset.

---

## 15. Development Phases

### Phase 1: Build the Skeleton

Goal: run the minimal end-to-end pipeline.

Tasks:

* set up Claude Code Skill directory structure
* write SKILL.md
* write intake / method_analyzer / mentoring_style_analyzer / mentor_builder
* implement a basic skill_writer

Deliverable:

* ability to construct a mentor Skill manually from summarized materials

### Phase 2: Add the Bridge Layer and Correction Mechanism

Tasks:

* write bridge_analyzer
* write correction_handler
* write merger
* write version_manager

Deliverable:

* support for incremental correction and version evolution

### Phase 3: Add Parsers

Tasks:

* implement paper_parser
* implement annotation_parser
* implement email/chat/lecture parsers

Deliverable:

* semi-automatic extraction of distillation segments from raw materials

### Phase 4: Support Mentor Templates

Tasks:

* add templates such as “close-reading mentor,” “methodology mentor,” and “strict progress-driving mentor”
* support instantiation from a template followed by personal material injection

Deliverable:

* ability to generate usable mentor Skills even without a full private corpus

### Phase 5: Strengthen Long-Term Mentoring

Tasks:

* improve Guidance Memory Schema
* strengthen feedback tracking and review across turns

Deliverable:

* persistent mentoring continuity after repeated use

---

## 16. Acceptance Criteria

The project is successful only if it satisfies at least the following:

1. It can extract stable academic method and academic positioning from papers and books.
2. It can extract stable mentoring style from emails, annotations, and interactions.
3. The generated mentor Skill can reliably perform diagnose, review, and advance tasks.
4. After user correction, the result clearly converges toward the target mentor.
5. After repeated use, the Skill remembers the student's stage, weaknesses, and pending tasks.
6. The output no longer feels like a generic chat assistant, but like a research mentor with academic judgment and mentoring logic.

---

## 17. Implementation Requirements for Opus

Please implement according to the following principles:

1. **Do not reduce this project to a single prompt.**
2. The system must use a **Method / Persona / Memory** three-layer architecture.
3. Materials must be processed through distinct pipelines, at minimum separating:

   * academic thought materials
   * mentoring behavior materials
   * bridge materials
4. The system must support correction and rollback.
5. Claude Code is the priority host environment, but the internal structure should remain as host-agnostic as possible for future migration.
6. v1 should first make the minimal generation flow work; do not over-prioritize complex parsers at the start.
7. The generated mentor Skill must support three default modes: diagnose / review / advance.

---

## 18. One-Sentence Summary

The essence of this project is not to “imitate how a mentor talks,” but to:

**distill a research mentor's academic method, academic positioning, mentoring style, and supervision logic into a correctable, iterative, and long-term usable Claude Code Skill.**


if confused, check and learn from this:
https://github.com/titanwings/colleague-skill
https://github.com/therealXiaomanChu/ex-skill