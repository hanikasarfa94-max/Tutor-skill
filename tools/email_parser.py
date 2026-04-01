"""
email_parser.py

Parse mentor emails to extract task instructions, judgment tone, pacing requirements,
and advisory content for use by mentoring_style_analyzer.md.

Input: plain text file with one or more emails, or a .mbox file.
Each email should ideally include a From:/To: header to identify direction.

Usage:
    from tools.email_parser import parse_emails
    emails = parse_emails("path/to/emails.txt")
"""

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Email:
    subject: str
    body: str
    source_file: str
    direction: str = "unknown"   # mentor_to_student / student_to_mentor / unknown
    email_type: str = "unknown"  # advisory / administrative / social / unclear
    signals: list[str] = field(default_factory=list)
    # Signals: task_assignment, deadline_mention, praise, criticism,
    #          clarification_request, emotional_register, progress_check


ADMIN_KEYWORDS = [
    "schedule", "calendar", "meeting", "appointment", "rescheduled",
    "zoom link", "room", "logistics", "travel", "submit", "deadline",
    "registration", "enrollment",
]

ADVISORY_KEYWORDS = [
    "read", "write", "revise", "think about", "your argument", "your draft",
    "the problem", "your research", "your paper", "chapter", "thesis",
    "literature", "method", "theory", "approach", "question",
]

SIGNAL_PATTERNS = {
    "task_assignment": [
        r"\bplease (read|write|revise|send|prepare|look at)\b",
        r"\bfor (next week|our meeting|Thursday)\b",
        r"\bby (Monday|Tuesday|Wednesday|Thursday|Friday|the end of)\b",
        r"\bI('d| would) like (you to|to see)\b",
        r"\bcan you (send|write|prepare|look at)\b",
    ],
    "deadline_mention": [
        r"\bby (the end of|next|this)\b.*(week|month|Friday|Thursday)",
        r"\bdeadline\b",
        r"\bdue (date|by)\b",
    ],
    "praise": [
        r"\b(good|well done|nice|this is (strong|clear|good|excellent))\b",
        r"\bI (like|enjoyed|appreciate|was impressed by)\b",
        r"\bexactly (right|what I had in mind)\b",
    ],
    "criticism": [
        r"\b(not (clear|quite right|there yet|convincing))\b",
        r"\bstill (needs|requires|lacks)\b",
        r"\bI (don't|do not|didn't|did not) (think|see|understand|follow)\b",
        r"\bthe (problem|issue|concern) (here|with this|is that)\b",
    ],
    "clarification_request": [
        r"\bwhat do you mean by\b",
        r"\bcan you (clarify|explain|elaborate)\b",
        r"\bI'?m (not sure|unclear) (what|how|why)\b",
    ],
    "progress_check": [
        r"\bhow (is|are|has) (it|the|your) (going|progressed|been)\b",
        r"\bwhere are you (with|on)\b",
        r"\bany (progress|updates|news)\b",
    ],
    "emotional_register": [
        r"\bdon't worry\b",
        r"\bkeep going\b",
        r"\bI know (this|it) (is|can be) (hard|difficult|challenging)\b",
        r"\byou're (doing|making) (well|progress|good work)\b",
    ],
}


def parse_emails(filepath: str | Path) -> list[Email]:
    """
    Parse an email file into a list of Email objects.
    Supports plain text with standard headers or simple delimiter format.
    """
    filepath = Path(filepath)
    text = filepath.read_text(encoding="utf-8", errors="replace")

    raw_emails = _split_emails(text)
    result = []
    for raw in raw_emails:
        subject = _extract_header(raw, "Subject") or _extract_header(raw, "Re") or ""
        body = _strip_headers(raw)
        direction = _infer_direction(raw)
        email_type = _classify_email_type(body)
        signals = _extract_signals(body)
        result.append(
            Email(
                subject=subject,
                body=body.strip(),
                source_file=str(filepath),
                direction=direction,
                email_type=email_type,
                signals=signals,
            )
        )
    return result


def _split_emails(text: str) -> list[str]:
    # mbox format: each email starts with "From " (note: no colon)
    if re.match(r"^From ", text, re.MULTILINE):
        parts = re.split(r"\nFrom ", text)
        return [p.strip() for p in parts if p.strip()]

    # Delimiter format: emails separated by "---" or "==="
    parts = re.split(r"\n[-=]{5,}\n", text)
    if len(parts) > 1:
        return [p.strip() for p in parts if p.strip()]

    # Single email
    return [text.strip()]


def _extract_header(text: str, name: str) -> str:
    match = re.search(rf"^{name}:\s*(.+)$", text, re.MULTILINE | re.IGNORECASE)
    return match.group(1).strip() if match else ""


def _strip_headers(text: str) -> str:
    # Remove standard headers block at the top
    lines = text.split("\n")
    header_re = re.compile(r"^(From|To|CC|Subject|Date|Re|Fwd):.*$", re.IGNORECASE)
    body_start = 0
    for i, line in enumerate(lines):
        if not header_re.match(line) and line.strip():
            body_start = i
            break
    return "\n".join(lines[body_start:])


def _infer_direction(text: str) -> str:
    from_line = _extract_header(text, "From")
    to_line = _extract_header(text, "To")

    # Very rough heuristic: if From contains "prof", "dr", or common mentor roles
    mentor_indicators = ["prof", "professor", "dr.", "supervisor", "advisor"]
    from_lower = from_line.lower()
    if any(ind in from_lower for ind in mentor_indicators):
        return "mentor_to_student"
    if to_line:
        to_lower = to_line.lower()
        if any(ind in to_lower for ind in mentor_indicators):
            return "student_to_mentor"

    return "unknown"


def _classify_email_type(body: str) -> str:
    body_lower = body.lower()
    admin_hits = sum(1 for kw in ADMIN_KEYWORDS if kw in body_lower)
    advisory_hits = sum(1 for kw in ADVISORY_KEYWORDS if kw in body_lower)

    if advisory_hits > admin_hits:
        return "advisory"
    if admin_hits > 0 and advisory_hits == 0:
        return "administrative"
    return "unclear"


def _extract_signals(body: str) -> list[str]:
    body_lower = body.lower()
    signals = []
    for signal, patterns in SIGNAL_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, body_lower):
                signals.append(signal)
                break
    return signals


def filter_advisory(emails: list[Email]) -> list[Email]:
    """Return only emails classified as advisory (exclude administrative)."""
    return [e for e in emails if e.email_type == "advisory"]


def filter_mentor_to_student(emails: list[Email]) -> list[Email]:
    """Return only emails where the mentor is writing to the student."""
    return [e for e in emails if e.direction == "mentor_to_student"]


def emails_to_markdown(emails: list[Email]) -> str:
    """Format emails as Markdown for passing to mentoring_style_analyzer."""
    lines = []
    for i, email in enumerate(emails, 1):
        lines.append(f"### Email {i}")
        if email.subject:
            lines.append(f"**Subject:** {email.subject}")
        lines.append(f"**Direction:** {email.direction}")
        lines.append(f"**Type:** {email.email_type}")
        if email.signals:
            lines.append(f"**Signals:** {', '.join(email.signals)}")
        lines.append("")
        lines.append(email.body)
        lines.append("")
    return "\n".join(lines)
