# Correction Handler

## Purpose

Receive user corrections and update the mentor skill. Runs when the user invokes `/update-mentor {slug}` in correction mode.

---

## When Corrections Are Needed

After using a mentor, the user may find it misrepresents the target in specific ways:

- "This doesn't sound like them at all"
- "They would never phrase it that way"
- "They care far more about X than this profile suggests"
- "This is completely wrong — they actually do the opposite"
- "They are much harsher than this"
- "They would ask a question here, not give an answer"

---

## Correction Entry Flow

```
Which mentor are you correcting? ({slug})

What would you like to correct?
  1. A specific response felt wrong
  2. A general behavioral rule needs changing
  3. A new pattern I've observed should be added
  4. Something is completely wrong and should be deleted
  5. Stylistic correction — the voice/phrasing is off

(Type a number or describe)
```

---

## Correction Types

### Type 1: Response-Level Correction

The user pastes a mentor response that felt wrong and explains what should have been different.

Processing:
1. Identify which layer the problem is in: method / persona / voice
2. Identify which specific rule produced the wrong behavior
3. Propose a correction to that rule
4. Ask: "Does this correction capture what you mean?"

Output: add to Correction Log in `persona.md` or `method.md`.

---

### Type 2: Rule-Level Correction

The user identifies a specific rule in `persona.md` or `method.md` and wants to change it.

Processing:
1. Show the current rule
2. Ask the user what it should say instead
3. Confirm the replacement
4. Write the updated rule
5. Version bump

---

### Type 3: Addition

The user wants to add a new behavioral rule or method pattern.

Processing:
1. Identify which file and which dimension the addition belongs to
2. Tag it as: `source: user_correction`, `confidence: user-asserted`
3. Ask: "Is this based on something you observed, or is it a correction to what the profile got wrong?"
4. Write to the appropriate file

---

### Type 4: Deletion

The user wants to remove a rule that is clearly wrong.

Processing:
1. Show the rule to be deleted
2. Ask: "Do you want to delete this entirely, or replace it with something?"
3. If delete: archive the rule in `meta.json` under `correction_log` with reason
4. Remove from active file
5. Version bump

---

### Type 5: Stylistic Correction

The mentor's voice is off — not factually wrong, but doesn't sound like the person.

Processing:
1. Ask the user to provide an example of how the mentor actually sounds in this situation
2. Extract phrasing patterns from the example
3. Add to `common_phrasing_patterns` in `persona.md`
4. Add the wrong pattern to `forbidden_misrepresentations`
5. Version bump

---

## Merge Rules

When integrating corrections:

1. **User correction > original analysis.** Corrections always override the original analyzer output.
2. **User correction > inferred patterns.** Corrections always override patterns labeled `evidence: inferred`.
3. **User correction does NOT automatically override direct-evidence items** — instead, the conflict is flagged, and the user must confirm explicitly.
4. **New direct evidence > old inferred evidence.** If the user provides a quote from source material, it can upgrade a `confidence: low` item to `confidence: high`.
5. **Do not silently overwrite.** Every correction is logged.

---

## Correction Log Format

Every correction is appended to the Correction Log in the relevant file:

```markdown
## Correction Log

- Date: {date}
  Type: {rule_change / addition / deletion / stylistic}
  Layer: {method / persona / voice}
  Dimension: {which dimension}
  Change: {description of what changed}
  Reason: {user's stated reason, quoted if possible}
  Version: {new version number}
```

---

## Version Bump Rules

After any correction:

1. Increment the patch version in `meta.json`: `v1.0.0` → `v1.0.1`
2. Copy the previous version to `mentors/archives/{slug}/v{previous_version}/`
3. Write a version note: what changed and why
4. Update `last_updated` in all three files

For major corrections (multiple rule changes or a fundamental persona shift):
- Increment minor version: `v1.0.0` → `v1.1.0`
- Prompt the user: "This is a significant change. Do you want to tag this as a new version and keep the previous one for rollback?"

---

## Conflict Detection

When the user provides a correction that conflicts with existing high-confidence content:

```
⚠ Conflict detected

  Existing rule (confidence: high, direct evidence from {source}):
  "{existing rule}"

  Your correction:
  "{proposed correction}"

  These conflict. Options:
    1. Replace the existing rule entirely (the source material was misread)
    2. Add your correction alongside it (the mentor behaves differently in different contexts)
    3. Lower the existing rule's confidence and add a note

  What would you like to do?
```
