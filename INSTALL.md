# Installation

## Requirements

- Claude Code (CLI or desktop app)
- Python 3.11+ (for parser tools)
- Git

---

## Install

### Option 1: Clone directly into your Claude skills directory

```bash
# macOS / Linux
git clone https://github.com/hanikasarfa94-max/Tutor-skill.git ~/.claude/skills/tutor-skill

# Windows
git clone https://github.com/hanikasarfa94-max/Tutor-skill.git %USERPROFILE%\.claude\skills\tutor-skill
```

### Option 2: Clone anywhere, then tell Claude Code where it is

```bash
git clone https://github.com/hanikasarfa94-max/Tutor-skill.git /path/of/your/choice
```

Then add the path to your Claude Code skills configuration.

---

## Python Dependencies (optional — only needed for parser tools)

```bash
cd tutor-skill
pip install -r requirements.txt
```

The parsers (`paper_parser.py`, `email_parser.py`, etc.) require `pdfminer.six` for PDF support.
You can use the skill without them — the parsers are optional preprocessing tools that format your materials before pasting into Claude.

---

## Verify Installation

Open Claude Code and run:

```
/list-mentors
```

You should see the example archetype:

```
Available mentors:

  slug                    name                              type        version
  example-archetype       Close-Reading Mentor (Archetype)  archetype   1.0.0
```

If you see this, the skill is installed and working.

---

## Quick Start: Use the Example Mentor

Try the included archetype immediately — no setup required:

```
/mentor example-archetype diagnose
```

Then describe your current research problem or confusion.

---

## Quick Start: Create Your First Mentor

```
/create-mentor
```

You'll be guided through a short intake. At minimum you need:
- A name or slug for the mentor
- Some idea of who they are (discipline, style)

Even without source materials, you can build a usable mentor from the intake questionnaire alone (confidence will be low, but it's a starting point you can correct over time).

---

## Upgrading

```bash
cd ~/.claude/skills/tutor-skill
git pull origin main
```

Generated mentor profiles in `mentors/generated/` are not tracked by git (see `.gitignore`), so your data is safe across upgrades.

---

## Privacy Note

Mentor profiles you generate from real source materials (emails, annotations, papers) are stored in `mentors/generated/` and `mentors/archives/`. These directories are gitignored by default. Do not commit them to a public repository.
