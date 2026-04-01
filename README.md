# tutor-skill

A Claude Code skill for distilling research mentors.

**Build a mentor skill** from papers, emails, lecture notes, and annotations.
**Use the mentor skill** for ongoing research guidance — diagnose problems, review drafts, advance stalled work.

---

## Quick Start

### Install

Clone this repository into your Claude Code skills directory:

```bash
git clone <this-repo> ~/.claude/skills/tutor-skill
```

Or place the directory wherever your Claude Code reads skills from.

### Create a Mentor

```
/create-mentor
```

Follow the intake prompts. You'll be asked for:
- A name/slug for the mentor
- The type (specific person / archetype / hybrid)
- Their discipline and research fields
- What source materials you have (papers, emails, annotations, etc.)
- A brief subjective description

The system will categorize your materials, run the appropriate analyzers, and generate a structured mentor profile.

### Use a Mentor

```
/mentor example-archetype
```

Or specify a mode directly:

```
/mentor example-archetype diagnose
/mentor example-archetype review
/mentor example-archetype advance
```

### Correct a Mentor

```
/update-mentor example-archetype
```

---

## Three Modes

| Mode | Use when | Output |
|------|----------|--------|
| **Diagnose** | Problem is vague, topic is unstable | What the real problem is, what's missing, what to do first |
| **Review** | You have a draft or outline | Ranked defects, revision priorities, specific suggestions |
| **Advance** | You're stuck or procrastinating | Stage diagnosis, root cause, concrete next step for this week |

---

## How It Works

The system uses a three-layer architecture:

1. **Method Layer** (`method.md`) — Academic standards: what counts as a well-formed problem, how to evaluate literature, what makes an argument hold.
2. **Persona Layer** (`persona.md`) — Mentoring behavior: how they deliver feedback, how they question, how they assign tasks, what they'd never say.
3. **Memory Layer** (`memory.md`) — Accumulated knowledge of the student's history: recurring issues, current stage, pending tasks.

These are kept separate and processed through distinct pipelines to avoid contamination (academic writing style bleeding into supervision tone, or vice versa).

---

## Directory Structure

```
tutor-skill/
├── SKILL.md                         ← Claude Code entry point
├── README.md
├── prompts/
│   ├── intake.md                    ← intake script
│   ├── method_analyzer.md           ← extract academic method from Category A
│   ├── mentoring_style_analyzer.md  ← extract persona from Category B
│   ├── bridge_analyzer.md           ← connect method to voice via Category C
│   ├── mentor_builder.md            ← integrate and generate mentor files
│   ├── merger.md                    ← merge new materials into existing profile
│   └── correction_handler.md       ← handle user corrections
├── tools/
│   ├── paper_parser.py              ← segment papers by function type
│   ├── annotation_parser.py         ← extract behavioral signals from annotations
│   ├── email_parser.py              ← classify and extract patterns from emails
│   ├── chat_parser.py               ← extract patterns from chat logs
│   ├── lecture_parser.py            ← extract bridge-layer content from lectures
│   ├── skill_writer.py              ← read/write mentor profile files
│   └── version_manager.py          ← snapshot, rollback, version bump
├── mentors/
│   ├── generated/                   ← active mentor profiles
│   │   └── example-archetype/      ← example: close-reading archetype
│   └── archives/                    ← versioned snapshots for rollback
├── docs/
│   └── schema.md                    ← full schema reference
└── requirements.txt
```

---

## Example Mentor

An example archetype is included at `mentors/generated/example-archetype/`.

Try it:
```
/mentor example-archetype diagnose
```

Then give it your current research problem or confusion.

---

## Development Phases

- [x] **Phase 1**: Core pipeline skeleton — intake, analyzers, builder, writer, versioning
- [ ] **Phase 2**: Bridge layer + correction + merger polish
- [ ] **Phase 3**: Parser automation (paper, email, chat, lecture)
- [ ] **Phase 4**: Archetype templates (close-reading, methodology-focused, strict progress-driver)
- [ ] **Phase 5**: Long-term mentoring memory — cross-session feedback tracking

---

## Requirements

```
pip install pdfminer.six
```

Python 3.11+ recommended.
