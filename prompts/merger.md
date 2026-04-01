# Merger

## Purpose

Merge new source materials into an existing mentor profile. Runs when the user invokes `/update-mentor {slug}` with new materials to add (as opposed to explicit corrections).

---

## When to Use

The merger runs when:
- The user has found new emails, papers, or annotations they hadn't included before
- The user wants to inject additional materials after initial build
- The user is upgrading an archetype-based mentor with specific personal materials

---

## Merge Flow

```
You're adding new materials to {slug}.

What type of materials are you adding?
  A — Academic thought (papers, books, lectures)
  B — Mentoring behavior (emails, annotations, chats)
  C — Bridge (teaching transcripts, defense comments)

(You can add multiple types at once)
```

After the user provides the materials:
1. Run the appropriate analyzer(s) on the new materials only
2. Compare the new analysis output with the existing content in `method.md` or `persona.md`
3. Merge using the rules below

---

## Merge Rules

### Rule 1: Preserve Existing Structure

Do not reorganize or rename dimensions when merging. New items go into the existing dimension slots.

### Rule 2: Direct Evidence Outranks Inferred Evidence

If the existing profile has an item marked `evidence: inferred` and the new material provides `evidence: direct` for the same or similar point:
- Upgrade the item to `evidence: direct`
- Update the confidence level
- Log the source upgrade in the item

### Rule 3: Direct Evidence Outranks User Assertion

If the existing profile has a user-asserted correction and new material (direct evidence) conflicts with it:
- Flag the conflict to the user
- Do not silently overwrite
- Let the user decide

### Rule 4: New Evidence Does Not Automatically Override Old Evidence

If both old and new materials are direct evidence but they conflict:
- Keep both, tagged with their sources
- Flag the conflict with a note: `[conflicting evidence — see sources]`
- Let the user review and resolve

### Rule 5: Never Blindly Average

Do not produce a "blended" output that loses the signal from either source. Preserve specificity. If two emails show different behavior, record both with their contexts rather than averaging.

---

## Merge Output

After merging, show a diff summary:

```
Merge complete for {slug}:

  Method layer:
    {dimension}: {count} new items added, {count} items updated, {count} conflicts flagged

  Persona layer:
    {dimension}: {count} new items added, {count} items updated, {count} conflicts flagged

  Conflicts requiring review:
    1. [description of conflict]
    2. [description of conflict]

  New version: {version}

  Would you like to resolve the conflicts now?
```

---

## Conflict Resolution in Merge

For each flagged conflict:

```
Conflict in {dimension}:

  Existing item (from {source}, confidence: {level}):
  "{existing statement}"

  New item (from {new source}, confidence: {level}):
  "{new statement}"

  These appear to contradict each other. Options:
    1. Keep both (the mentor behaves differently depending on context — describe the contexts)
    2. Replace old with new (the old source was lower quality or misread)
    3. Keep old, discard new (the new source is an outlier)
    4. Flag for later review

  What would you like to do?
```
