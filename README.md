[English](./README.md) | [涓枃](./README_zh.md)

---

# There's a certain kind of person you only meet once, but whose questions stay with you forever

---

You know the feeling.

You've just finished explaining your idea 鈥?carefully, you thought.  
They're quiet for a moment.  
Then they ask one thing:

> *"What do you mean by 'identity' here?"*

You open your mouth. Nothing comes out.

Not because you don't know the word.  
Because you've never actually stopped to think about what you were using it to mean.

In that silence, something shifts 鈥?a strange mixture of embarrassment  
and something deeper.  
The feeling of being truly seen.

---

## A good mentor doesn't give you answers

What they do is make it impossible to keep deceiving yourself with vague language.

They make you realize that the thing you thought you'd been thinking about  
鈥?you hadn't started thinking about yet.

They make you hear their voice at 2am, staring at a paragraph:  
*"Is that your argument, or your topic?"*

---

## But that kind of person is hard to find

Some people never meet one.  
Some do, then graduate, move away, lose touch.  
Some have advisors who only say "think more about it" 鈥?without telling you which direction.

Research is lonely. Not because there's no one around,  
but because the person who would ask exactly the right question at exactly the right moment  
is usually not there.

---

## What this skill is trying to do

Distill a real mentor's **academic judgment**, **questioning style**, and **supervision logic**  
into a system that can be used again and again.

Not an imitation of how they speak.  
An extraction of **how they see**.

When your research question dissolves into fog again 鈥? 
when your draft is finished but you can't say what it's arguing 鈥? 
when you haven't moved in three weeks 鈥? 
you can open it.

Like pushing open that office door.

---

# tutor-skill

A Claude Code skill for distilling research mentors.

**Build** a mentor skill from papers, emails, lecture notes, and annotations.  
**Use** the mentor for ongoing research guidance 鈥?diagnose problems, review drafts, advance stalled work 鈥?with memory that persists across sessions.

---

> **Language:** [English](./README.md) | [涓枃](./README_zh.md)

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
Method Layer  (method.md)   鈫?academic judgment: what makes a problem real,
                               an argument hold, a literature review adequate
        鈫?Persona Layer (persona.md)  鈫?supervision behavior: how they question, push back,
                               assign tasks, deliver feedback 鈥?what they'd never say
        鈫?Memory Layer  (memory.md)   鈫?your history: stage, recurring weaknesses, pending tasks
                               鈥?grows across sessions
```

**Method layer** is extracted from papers, books, and lectures 鈥?capturing research problem sense, conceptual standards, methodological preferences, argument style.

**Persona layer** is extracted from emails, annotations, chat logs, and meeting notes 鈥?capturing interaction patterns, harshness level, task assignment style, encouragement and rejection forms.

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
| **A 鈥?Academic thought** | Builds the Method layer | Papers, books, lectures, interviews, prefaces |
| **B 鈥?Mentoring behavior** | Builds the Persona layer | Emails, annotations, chat logs, meeting notes, student recollections |
| **C 鈥?Bridge** | Connects method to student-facing voice | Classroom transcripts, defense comments, recruitment talks |

No materials? The intake questionnaire can build a usable starting point 鈥?low confidence, but correctable over time.

---

## Correction and Iteration

First-generation profiles are rarely perfect. The system supports:

- **Response-level correction** 鈥?"that response didn't sound like them"
- **Rule replacement** 鈥?"change this behavioral rule to..."
- **Incremental addition** 鈥?"they also consistently do X when Y"
- **Stylistic correction** 鈥?"they would never phrase it this way"

Every correction is versioned. Roll back anytime with `/mentor-rollback`.

---

## Directory Structure

```
tutor-skill/
鈹溾攢鈹€ SKILL.md                              鈫?Claude Code entry point
鈹溾攢鈹€ README.md                             鈫?English (this file)
鈹溾攢鈹€ README_zh.md                          鈫?Chinese / 涓枃
鈹溾攢鈹€ INSTALL.md
鈹溾攢鈹€ prompts/
鈹?  鈹溾攢鈹€ intake.md                         鈫?/create-mentor: step 1
鈹?  鈹溾攢鈹€ method_analyzer.md                鈫?extract academic method (Category A)
鈹?  鈹溾攢鈹€ mentoring_style_analyzer.md       鈫?extract persona (Category B)
鈹?  鈹溾攢鈹€ bridge_analyzer.md                鈫?bridge layer (Category C)
鈹?  鈹溾攢鈹€ mentor_builder.md                 鈫?integrate and generate files
鈹?  鈹溾攢鈹€ use_mentor.md                     鈫?/mentor runtime prompt
鈹?  鈹溾攢鈹€ session_closer.md                 鈫?end-of-session memory update
鈹?  鈹溾攢鈹€ merger.md                         鈫?add materials to existing profile
鈹?  鈹斺攢鈹€ correction_handler.md            鈫?correct behavior
鈹溾攢鈹€ tools/
鈹?  鈹溾攢鈹€ paper_parser.py
鈹?  鈹溾攢鈹€ annotation_parser.py
鈹?  鈹溾攢鈹€ email_parser.py
鈹?  鈹溾攢鈹€ chat_parser.py
鈹?  鈹溾攢鈹€ lecture_parser.py
鈹?  鈹溾攢鈹€ skill_writer.py
鈹?  鈹斺攢鈹€ version_manager.py
鈹溾攢鈹€ mentors/
鈹?  鈹溾攢鈹€ generated/                        鈫?your mentor profiles (gitignored)
鈹?  鈹?  鈹斺攢鈹€ example-archetype/           鈫?try this first
鈹?  鈹斺攢鈹€ archives/                         鈫?version snapshots
鈹斺攢鈹€ docs/
    鈹溾攢鈹€ schema.md
    鈹斺攢鈹€ intro_zh.md
```

---

## Development Phases

- [x] **Phase 1** 鈥?Core pipeline: intake, analyzers, builder, writer, versioning
- [x] **Phase 2** 鈥?Runtime: use-mentor prompt, session memory, correction, discipline-specific dimensions
- [x] **Phase 3** 鈥?Parser automation: paper, email, chat, lecture (PDF, DOCX, WeChat, DingTalk, HTML)
- [x] **Phase 4** 鈥?Archetype templates: close-reading, methodology-focused, strict progress-driver
- [x] **Phase 5** 鈥?Long-term memory: cross-session feedback tracking

---

## Requirements

```bash
pip install -r requirements.txt  # optional 鈥?only needed for parser tools
```

Python 3.11+. The parsers are optional preprocessing tools 鈥?the skill works without them. See [INSTALL.md](./INSTALL.md) for the full dependency table.

---

## Related Projects

This project's architecture is inspired by:
- [colleague-skill](https://github.com/titanwings/colleague-skill) 鈥?colleague distillation framework
- [ex-skill](https://github.com/therealXiaomanChu/ex-skill) 鈥?same framework pattern


