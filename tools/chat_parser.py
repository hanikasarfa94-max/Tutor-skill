"""
chat_parser.py

Parse instant-message conversation logs (WeChat, Telegram, WhatsApp, Slack, etc.)
exported as plain text to extract:
  - questioning patterns
  - rejection patterns
  - encouragement patterns
  - task assignment patterns

Usage:
    from tools.chat_parser import parse_chat
    messages = parse_chat("path/to/chat.txt", mentor_name="Prof. Zhang")
"""

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Message:
    sender: str
    text: str
    source_file: str
    is_mentor: bool = False
    patterns: list[str] = field(default_factory=list)
    # Patterns: question / rejection / encouragement / task_assignment /
    #           clarification_demand / approval / pushback / silence_implied


MENTOR_MESSAGE_PATTERNS = {
    "question": [
        r"\?$",
        r"\bwhat (do you|does|is|are)\b",
        r"\bwhy (did|do|is|are)\b",
        r"\bhow (do you|does|is)\b",
        r"\bhave you (thought|considered|read)\b",
    ],
    "rejection": [
        r"\bno[,.]?\s",
        r"\bnot (quite|right|there yet|convincing)\b",
        r"\bI don'?t (think|see|follow|buy)\b",
        r"\bthat'?s not (the|right|what)\b",
        r"\bthat doesn'?t (work|hold|follow)\b",
    ],
    "encouragement": [
        r"\b(good|nice|yes|exactly|right|well done|this is (good|strong|clear))\b",
        r"\bkeep (going|it up)\b",
        r"\byou'?re (on the right|making progress|getting there)\b",
    ],
    "task_assignment": [
        r"\bplease (read|write|revise|prepare|send|look at)\b",
        r"\bcan you (read|write|prepare|send|look at|think about)\b",
        r"\bI'?d like (you to|to see)\b",
        r"\bby (Thursday|next week|our meeting|Friday|tomorrow)\b",
        r"\bfor (next time|our next meeting|Thursday)\b",
    ],
    "clarification_demand": [
        r"\bwhat (exactly|do you mean by|is your)\b",
        r"\bI'?m not (sure|clear) (what|how|why|which)\b",
        r"\bcan you (clarify|explain|elaborate|be more specific)\b",
        r"\bwhat does ['\"]?\w+['\"]? mean (here|in this context)\b",
    ],
    "approval": [
        r"\byes[,.]?\s",
        r"\bagree[d]?\b",
        r"\bcorrect\b",
        r"\bthat'?s (right|good|exactly (right|what I))\b",
    ],
    "pushback": [
        r"\bbut (wait|hold on|actually)\b",
        r"\bI (disagree|would push back)\b",
        r"\bnot so fast\b",
        r"\bhave you (considered|thought about) the alternative\b",
    ],
}


def parse_chat(
    filepath: str | Path,
    mentor_name: str | None = None,
    mentor_identifiers: list[str] | None = None,
) -> list[Message]:
    """
    Parse a chat log into Message objects.

    Args:
        filepath: Path to the chat export file.
        mentor_name: The mentor's display name as it appears in the log.
        mentor_identifiers: List of substrings that identify the mentor as sender.
    """
    filepath = Path(filepath)
    text = filepath.read_text(encoding="utf-8", errors="replace")
    identifiers = mentor_identifiers or []
    if mentor_name:
        identifiers.append(mentor_name)

    raw_messages = _split_messages(text)
    result = []
    for sender, body in raw_messages:
        is_mentor = _is_mentor_message(sender, identifiers)
        patterns = _extract_patterns(body) if is_mentor else []
        result.append(
            Message(
                sender=sender,
                text=body.strip(),
                source_file=str(filepath),
                is_mentor=is_mentor,
                patterns=patterns,
            )
        )
    return result


def _split_messages(text: str) -> list[tuple[str, str]]:
    """
    Split a chat log into (sender, message) tuples.
    Tries several common export formats.
    """
    # Format 1: WeChat / WhatsApp style: "2024-01-01 10:00 Name: message"
    wechat_re = re.compile(
        r"^(?:\d{4}[-/]\d{2}[-/]\d{2}\s+\d{2}:\d{2}(?::\d{2})?\s+)?(.+?):\s+(.+)$",
        re.MULTILINE
    )
    matches = list(wechat_re.finditer(text))
    if len(matches) > 3:
        results = []
        for i, m in enumerate(matches):
            sender = m.group(1).strip()
            # Collect multi-line message until the next match
            body_start = m.end()
            body_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            body = text[body_start:body_end].strip()
            full_body = m.group(2) + (" " + body if body else "")
            results.append((sender, full_body))
        return results

    # Format 2: Slack-style "[timestamp] sender: message"
    slack_re = re.compile(r"^\[.+?\]\s+(.+?):\s+(.+)$", re.MULTILINE)
    matches = list(slack_re.finditer(text))
    if len(matches) > 3:
        return [(m.group(1).strip(), m.group(2).strip()) for m in matches]

    # Format 3: Simple "Name: message" per line
    simple_re = re.compile(r"^([A-Za-z][^:\n]{0,40}):\s+(.+)$", re.MULTILINE)
    matches = list(simple_re.finditer(text))
    if len(matches) > 3:
        return [(m.group(1).strip(), m.group(2).strip()) for m in matches]

    # Fallback: treat each paragraph as an undifferentiated message
    return [("unknown", p.strip()) for p in re.split(r"\n\s*\n", text) if p.strip()]


def _is_mentor_message(sender: str, identifiers: list[str]) -> bool:
    if not identifiers:
        return False
    sender_lower = sender.lower()
    return any(ident.lower() in sender_lower for ident in identifiers)


def _extract_patterns(text: str) -> list[str]:
    text_lower = text.lower()
    found = []
    for pattern_name, patterns in MENTOR_MESSAGE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                found.append(pattern_name)
                break
    return found


def mentor_messages(messages: list[Message]) -> list[Message]:
    """Filter to only mentor messages."""
    return [m for m in messages if m.is_mentor]


def summarize_patterns(messages: list[Message]) -> dict:
    """Aggregate pattern frequencies across mentor messages."""
    from collections import Counter
    counts: Counter = Counter()
    mentor_msgs = mentor_messages(messages)
    for msg in mentor_msgs:
        counts.update(msg.patterns)
    return {
        "total_mentor_messages": len(mentor_msgs),
        "total_messages": len(messages),
        "pattern_frequencies": dict(counts.most_common()),
    }


def chat_to_markdown(messages: list[Message], mentor_only: bool = False) -> str:
    """Format messages as Markdown for mentoring_style_analyzer."""
    lines = []
    for msg in messages:
        if mentor_only and not msg.is_mentor:
            continue
        role = "**[MENTOR]**" if msg.is_mentor else f"*[{msg.sender}]*"
        lines.append(f"{role}: {msg.text}")
        if msg.patterns:
            lines.append(f"  ↳ patterns: {', '.join(msg.patterns)}")
    return "\n".join(lines)
