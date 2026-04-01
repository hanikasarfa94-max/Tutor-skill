# Research Mentor Skill

## Research Mentor Skill

A Claude Code skill for distilling research mentors — capturing their academic method, mentoring style, and guidance logic into a correctable, iterative, and long-term usable mentor system.

---

## What This Skill Does

This skill runs in two phases:

1. **Create Mentor Skill** — distill a specific mentor (or mentor archetype) from source materials and generate a structured mentor profile.
2. **Use Mentor Skill** — interact with the generated mentor to receive feedback aligned with that mentor's academic method and mentoring style.

The generated mentor is not a chatbot that mimics tone. It is a working system that can:
- Diagnose whether a research problem is well-formed
- Review papers, outlines, and drafts with ranked issue prioritization
- Guide literature reading and research path
- Decompose tasks and manage stage progression
- Track a student's recurring weaknesses and pending items across sessions

---

## Commands

### Create & Manage

| Command | Description |
|---------|-------------|
| `/create-mentor` | Start distilling a new mentor from source materials |
| `/update-mentor {slug}` | Add new materials or correct an existing mentor profile |
| `/list-mentors` | Show all generated mentor skills |
| `/mentor-rollback {slug} {version}` | Revert a mentor to a previous version |
| `/delete-mentor {slug}` | Remove a mentor skill |

### Use

| Command | Description |
|---------|-------------|
| `/mentor {slug}` | Activate a mentor for an ongoing session |
| `/mentor {slug} diagnose` | Enter Diagnose mode — clarify and sharpen a research problem |
| `/mentor {slug} review` | Enter Review mode — critique an outline, draft, or literature review |
| `/mentor {slug} advance` | Enter Advance mode — diagnose stagnation and set next-step tasks |

---

## How `/create-mentor` Works

The creation pipeline has five stages:

```
intake → analyze (method + persona + bridge) → build → preview → write
```

1. **intake** — collect mentor identity, material list, and user description
2. **method_analyzer** — extract academic method from papers, books, lectures
3. **mentoring_style_analyzer** — extract mentoring persona from emails, annotations, chats
4. **bridge_analyzer** — connect method to student-facing expression via lectures and talks
5. **mentor_builder** — integrate all layers and generate the final mentor skill files

Generated files are written to `mentors/generated/{slug}/`:
- `meta.json` — mentor identity and version info
- `method.md` — academic method, research problem sense, judgment rules
- `persona.md` — mentoring style, interaction patterns, tone
- `memory.md` — guidance memory: student stage, tasks, recurring issues

---

## How `/mentor {slug}` Works

When a mentor is activated, the system:

1. Loads `method.md`, `persona.md`, and `memory.md` for `{slug}`
2. Enters the specified mode (or asks which mode to use)
3. Applies the mentor's academic method and mentoring style to every response
4. Updates `memory.md` at the end of the session with new observations

### Three Default Modes

**Mode: Diagnose**
Suitable for: unclear problems, unstable topics, confused research direction.
Output structure:
1. What your real problem is
2. Why it is not yet well-formed
3. What prerequisites are missing
4. What you should do next
5. What you should not do yet

**Mode: Review**
Suitable for: outlines, drafts, paragraphs, literature reviews.
Output structure:
1. The most central problem
2. Severe defects
3. Secondary defects
4. Revision priority order
5. Actionable revision suggestions

**Mode: Advance**
Suitable for: procrastination, stagnation, stage management.
Output structure:
1. Current stage diagnosis
2. Root cause of stagnation
3. Minimal next-step action for this week
4. Expected deliverable format
5. Next checkpoint

---

## Runtime Behavior Rules

The mentor must follow these rules unconditionally:

1. **Diagnose first, answer later.** Default behavior is not to immediately provide conclusions. First identify whether the problem is well-formed, whether multiple tasks are conflated, and whether the user is at the right stage.
2. **Rank issues.** During review, never present a flat list of problems. Separate severe defects from secondary ones.
3. **Always give a next step.** Each response must include at least one concrete, actionable next step — not only abstract evaluation.
4. **Preserve academic discipline.** Do not sacrifice conceptual rigor to sound agreeable.
5. **Do not invent views.** When evidence from source materials is weak, reduce assertion strength explicitly.

---

## Directory Structure

```
tutor-skill/
├── SKILL.md                    ← you are here
├── README.md
├── prompts/
│   ├── intake.md               ← intake script
│   ├── method_analyzer.md      ← academic method extraction
│   ├── mentoring_style_analyzer.md  ← mentoring persona extraction
│   ├── bridge_analyzer.md      ← bridge material processing
│   ├── mentor_builder.md       ← integration and generation
│   ├── merger.md               ← incremental material merge
│   └── correction_handler.md  ← correction and update
├── tools/
│   ├── paper_parser.py
│   ├── annotation_parser.py
│   ├── email_parser.py
│   ├── lecture_parser.py
│   ├── chat_parser.py
│   ├── skill_writer.py
│   └── version_manager.py
├── mentors/
│   ├── generated/              ← active mentor profiles
│   └── archives/               ← versioned snapshots
├── docs/
│   └── schema.md
└── requirements.txt
```

---

## Correction and Evolution

After using a mentor, you may find it misrepresents the target. Use `/update-mentor {slug}` to enter correction mode.

Supported correction types:
- **Local correction** — "This specific response does not sound like them"
- **Overwrite correction** — "Replace this rule entirely with: ..."
- **Incremental addition** — "They also consistently do X when Y"
- **Stylistic correction** — "They would never phrase it this way"

Each correction is logged in `meta.json` with a version note. Use `/mentor-rollback` to revert if a correction makes things worse.
