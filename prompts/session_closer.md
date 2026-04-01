# Session Closer

## Purpose

Extract what was learned in a session and write it back to `memory.md`.
Runs at the end of every `/mentor {slug}` session.

---

## Input

You will receive:
1. The full session transcript (or a summary of what was discussed)
2. The current contents of `memory.md` for this mentor/student pair

---

## Extraction Tasks

### 1. Stage Update

Did the student's stage change this session? Possible stage transitions:
- `pre-proposal` → `proposal writing`
- `proposal writing` → `literature review`
- `literature review` → `chapter drafting`
- `chapter drafting` → `revision`
- `revision` → `near submission`
- Or any custom stage that more accurately describes their position

If stage changed: update `current_stage`.
If not: leave unchanged.

---

### 2. Recurring Issues

Scan the session for problems that have appeared before in `previous_feedback`:

- If a previously logged issue appeared again: update its `status` to `unresolved` (if it was `partial` or `resolved`) and increment a recurrence note
- If a new issue appeared for the first time: add it to `previous_feedback` with `status: unresolved`
- If a previously logged issue was resolved this session: update to `status: resolved`

**Important:** Only log issues that are genuine weaknesses, not one-off errors. The signal is recurrence.

---

### 3. Task Update

- Mark any tasks in `current_tasks` that were completed this session as `status: completed`
- Add any new tasks assigned this session with:
  - `task` — description of what the student must produce
  - `assigned_date` — today
  - `due_date` — as specified (usually "next session")
  - `status: pending`
- Move completed tasks to session history; do not accumulate stale completed tasks in current_tasks

---

### 4. Deliverables Update

- Remove deliverables that were produced and discussed
- Add any new deliverables mentioned ("bring your revised introduction", "email me the outline")

---

### 5. Mentor Emphases

Did the mentor repeat a principle or warning that has appeared before?
- If yes: it belongs in `mentor_emphases` (add if not already there)
- These are the things that define this mentor's supervision — what they return to across multiple sessions

---

### 6. Session History Entry

Add one entry to `session_history`:

```yaml
- date: {today's date}
  mode: diagnose | review | advance | other
  summary: {one sentence — what was the main thing that happened}
  key_outputs:
    - {task assigned, or problem diagnosed, or draft reviewed}
```

Keep session history entries terse. They are navigation aids, not transcripts.

---

## Output

Write the complete updated `memory.md` file. Do not truncate or summarize existing entries — preserve all history.

Show a brief diff summary after writing:

```
Memory updated for {slug}:

  Stage:          {unchanged / updated to: X}
  Tasks:          {count} completed, {count} new assigned
  Issues:         {count} new, {count} recurred, {count} resolved
  Emphases:       {count} added
  Session logged: {date} — {one-sentence summary}
```

---

## Staleness Rules

When reading existing memory.md entries:

- Tasks older than 4 sessions with `status: pending` — flag as potentially stale, ask user to confirm or drop
- `recurring_issues` with no recent session activity — mark as `status: dormant` (not resolved, but not active)
- `mentor_emphases` list capped at 10 — if adding a new one would exceed 10, ask which is least relevant to drop

---

## Example: What a Good Memory Update Looks Like

**Before (sparse):**
```yaml
student_profile:
  research_topic: Migration and urban labor markets
  current_stage: literature review
  recurring_issues:
    - Conflates "migration" and "mobility" as interchangeable terms
```

**After one Advance session:**
```yaml
student_profile:
  research_topic: Migration and urban labor markets in secondary Chinese cities
  current_stage: literature review — stalled, likely problem-definition issue
  recurring_issues:
    - Conflates "migration" and "mobility" as interchangeable terms [recurred: session 3]
    - Cannot state the central argument in one sentence [new: session 3]

current_tasks:
  - task: Write one paragraph defining "migration" as used in this thesis, distinguishing it from "mobility"
    assigned_date: 2026-04-01
    due_date: next session
    status: pending

mentor_emphases:
  - "You have a topic. You do not yet have a problem."
  - "Define every load-bearing term before using it in a claim."

session_history:
  - date: 2026-04-01
    mode: advance
    summary: Student stalled; root cause is unsettled research problem, not writing block
    key_outputs:
      - Diagnosed stagnation as problem-definition stagnation
      - Assigned term-definition paragraph task
```
