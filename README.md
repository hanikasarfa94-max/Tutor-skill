[English](./README.md) | [中文](./README_zh.md)

---

# There's a certain kind of person you only meet once, but whose questions stay with you forever

---

You know the feeling.

You've just finished explaining your idea — carefully, you thought.  
They're quiet for a moment.  
Then they ask one thing:

> *"What do you mean by 'identity' here?"*

You open your mouth. Nothing comes out.

Not because you don't know the word.  
Because you've never actually stopped to think about what you were using it to mean.

In that silence, something shifts — a strange mixture of embarrassment  
and something deeper.  
The feeling of being truly seen.

---

## A good mentor doesn't give you answers

What they do is make it impossible to keep deceiving yourself with vague language.

They make you realize that the thing you thought you'd been thinking about  
— you hadn't started thinking about yet.

They make you hear their voice at 2am, staring at a paragraph:  
*"Is that your argument, or your topic?"*

---

## But that kind of person is hard to find

Some people never meet one.  
Some do, then graduate, move away, lose touch.  
Some have advisors who only say "think more about it" — without telling you which direction.

Research is lonely. Not because there's no one around,  
but because the person who would ask exactly the right question at exactly the right moment  
is usually not there.

---

## What this skill is trying to do

Distill a real mentor's **academic judgment**, **questioning style**, and **supervision logic**  
into a system that can be used again and again.

Not an imitation of how they speak.  
An extraction of **how they see**.

When your research question dissolves into fog again —  
when your draft is finished but you can't say what it's arguing —  
when you haven't moved in three weeks —  
you can open it.

Like pushing open that office door.

---

# tutor-skill

A Claude Code skill for distilling research mentors.

**Build** a mentor skill from papers, emails, lecture notes, and annotations.  
**Use** the mentor for ongoing research guidance — diagnose problems, review drafts, advance stalled work — with memory that persists across sessions.

---

> **Language:** [English](./README.md) | [中文](./README_zh.md)

---

## Quick Start

### Install

```bash
# macOS / Linux / Windows (Git Bash)
git clone https://github.com/hanikasarfa94-max/Tutor-skill.git ~/.claude/skills/tutor-skill
```

```powershell
# Windows (PowerShell)
git clone https://github.com/hanikasarfa94-max/Tutor-skill.git "$env:USERPROFILE\.claude\skills\tutor-skill"
```

See [INSTALL.md](./INSTALL.md) for full setup instructions.

### Try the built-in example immediately

No materials needed (choose one):

```
/mentor example-archetype diagnose
/mentor methodology-archetype diagnose
/mentor strict-driver-archetype advance
```

Tell it your current research problem or confusion. See how it responds.

### Distill your own mentor

```
/create-mentor
```

You'll be guided through a short intake. The system will categorize your materials, run the appropriate analyzers, and generate a structured mentor profile.

---

## Three Modes

| Mode | Use when | Output structure |
|------|----------|-----------------|
| **Diagnose** | Problem is vague, topic unstable | What the real problem is / why it's not yet formed / what prerequisites are missing / what to do next / what not to do yet |
| **Review** | You have a draft, outline, or section to critique | Central problem / severe defects / secondary defects / revision priority order / one concrete revision suggestion |
| **Advance** | You're stuck, procrastinating, or lost on stage | Stage diagnosis / root cause of stagnation / minimal next-step task / deliverable format / next checkpoint |

---

## How It Works

Three layers, kept strictly separate:

```
Method Layer  (method.md)   ←  academic judgment: what makes a problem real,
                                an argument hold, a literature review adequate
    ↓
Persona Layer (persona.md)  ←  supervision behavior: how they question, push back,
                                assign tasks, deliver feedback — what they'd never say
    ↓
Memory Layer  (memory.md)   ←  your history: stage, recurring weaknesses, pending tasks
                                — grows across sessions
```

**Method layer** is extracted from papers, books, and lectures — capturing research problem sense, conceptual standards, methodological preferences, argument style.

**Persona layer** is extracted from emails, annotations, chat logs, and meeting notes — capturing interaction patterns, harshness level, task assignment style, encouragement and rejection forms.

**Memory layer** accumulates during use. It remembers what you're working on, where you're stuck, what you keep getting wrong, and what the mentor told you last time.

---

## Commands

### Create & manage

| Command | Description |
|---------|-------------|
| `/create-mentor` | Distill a new mentor from source materials |
| `/update-mentor {slug}` | Add materials or correct existing behavior |
| `/list-mentors` | Show all generated mentor skills |
| `/mentor-rollback {slug} {version}` | Revert to a previous version |
| `/delete-mentor {slug}` | Remove a mentor skill |

### Use

| Command | Description |
|---------|-------------|
| `/mentor {slug}` | Activate a mentor |
| `/mentor {slug} diagnose` | Start in Diagnose mode |
| `/mentor {slug} review` | Start in Review mode |
| `/mentor {slug} advance` | Start in Advance mode |

---

## Source Material Categories

| Category | Purpose | Examples |
|----------|---------|---------|
| **A — Academic thought** | Builds the Method layer | Papers, books, lectures, interviews, prefaces |
| **B — Mentoring behavior** | Builds the Persona layer | Emails, annotations, chat logs, meeting notes, student recollections |
| **C — Bridge** | Connects method to student-facing voice | Classroom transcripts, defense comments, recruitment talks |

No materials? The intake questionnaire can build a usable starting point — low confidence, but correctable over time.

---

## Correction and Iteration

First-generation profiles are rarely perfect. The system supports:

- **Response-level correction** — "that response didn't sound like them"
- **Rule replacement** — "change this behavioral rule to..."
- **Incremental addition** — "they also consistently do X when Y"
- **Stylistic correction** — "they would never phrase it this way"

Every correction is versioned. Roll back anytime with `/mentor-rollback`.

---

## Directory Structure

```
tutor-skill/
├── SKILL.md                              ←  Claude Code entry point
├── README.md                             ←  English (this file)
├── README_zh.md                          ←  Chinese / 中文
├── INSTALL.md
├── prompts/
│   ├── intake.md                         ←  /create-mentor: step 1
│   ├── method_analyzer.md                ←  extract academic method (Category A)
│   ├── mentoring_style_analyzer.md       ←  extract persona (Category B)
│   ├── bridge_analyzer.md                ←  bridge layer (Category C)
│   ├── mentor_builder.md                 ←  integrate and generate files
│   ├── use_mentor.md                     ←  /mentor runtime prompt
│   ├── session_closer.md                 ←  end-of-session memory update
│   ├── merger.md                         ←  add materials to existing profile
│   └── correction_handler.md            ←  correct behavior
├── tools/
│   ├── paper_parser.py
│   ├── annotation_parser.py
│   ├── email_parser.py
│   ├── chat_parser.py
│   ├── lecture_parser.py
│   ├── skill_writer.py
│   └── version_manager.py
├── mentors/
│   ├── generated/                        ←  your mentor profiles (gitignored)
│   │   └── example-archetype/           ←  try this first
│   └── archives/                         ←  version snapshots
└── docs/
    ├── schema.md
    └── intro_zh.md
```

---

## Development Phases

- [x] **Phase 1** — Core pipeline: intake, analyzers, builder, writer, versioning
- [x] **Phase 2** — Runtime: use-mentor prompt, session memory, correction, discipline-specific dimensions
- [x] **Phase 3** — Parser automation: paper, email, chat, lecture (PDF, DOCX, WeChat, DingTalk, HTML)
- [x] **Phase 4** — Archetype templates: close-reading, methodology-focused, strict progress-driver
- [x] **Phase 5** — Long-term memory: cross-session feedback tracking

---

## Requirements

```bash
pip install -r requirements.txt  # optional — only needed for parser tools
```

Python 3.11+. The parsers are optional preprocessing tools — the skill works without them. See [INSTALL.md](./INSTALL.md) for the full dependency table.

---

## Related Projects

This project's architecture is inspired by:
- [colleague-skill](https://github.com/titanwings/colleague-skill) — colleague distillation framework
- [ex-skill](https://github.com/therealXiaomanChu/ex-skill) — same framework pattern
