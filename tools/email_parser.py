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
    # CJK admin keywords
    "会议", "安排", "时间", "提交", "截止", "报名", "地点",
]

ADVISORY_KEYWORDS = [
    "read", "write", "revise", "think about", "your argument", "your draft",
    "the problem", "your research", "your paper", "chapter", "thesis",
    "literature", "method", "theory", "approach", "question",
    # CJK advisory keywords
    "阅读", "修改", "论文", "研究", "问题", "方法", "理论", "文献", "导师", "同学", "撰写",
]

SIGNAL_PATTERNS = {
    "task_assignment": [
        r"\bplease (read|write|revise|send|prepare|look at)\b",
        r"\bfor (next week|our meeting|Thursday)\b",
        r"\bby (Monday|Tuesday|Wednesday|Thursday|Friday|the end of)\b",
        r"\bI('d| would) like (you to|to see)\b",
        r"\bcan you (send|write|prepare|look at)\b",
        # CJK task assignment patterns
        r"请(你|您)(阅读|撰写|修改|发送|准备|看一下)",
        r"(下周|下次|我们开会)(前|时)(请|需要|要)",
        r"(在|于)(周[一二三四五六日]|下周|月底)(前|之前)(提交|发送|完成)",
        r"(希望|请|要求)(你|您)(能|可以)?",
    ],
    "deadline_mention": [
        r"\bby (the end of|next|this)\b.*(week|month|Friday|Thursday)",
        r"\bdeadline\b",
        r"\bdue (date|by)\b",
        # CJK deadline patterns
        r"(截止|截稿)(日期|时间|日)?(是|为)?",
        r"(最晚|最迟|务必)(在|于)?.*?(前|之前)",
        r"(提交|上交)(截止|时间|日期)",
    ],
    "praise": [
        r"\b(good|well done|nice|this is (strong|clear|good|excellent))\b",
        r"\bI (like|enjoyed|appreciate|was impressed by)\b",
        r"\bexactly (right|what I had in mind)\b",
        # CJK praise patterns
        r"(写得|做得|分析得)(很好|不错|出色|到位)",
        r"(这部分|这一节|这个论点)(很好|不错|清晰|有力)",
        r"(非常|很)(好|不错|清楚|准确|到位)",
    ],
    "criticism": [
        r"\b(not (clear|quite right|there yet|convincing))\b",
        r"\bstill (needs|requires|lacks)\b",
        r"\bI (don't|do not|didn't|did not) (think|see|understand|follow)\b",
        r"\bthe (problem|issue|concern) (here|with this|is that)\b",
        # CJK criticism patterns
        r"(不够|还不够)(清楚|清晰|深入|完整|有力)",
        r"(仍然|还是)(需要|有|存在)(修改|问题|不足)",
        r"(这里|这部分)(有问题|不对|不清楚|需要改)",
        r"(我认为|感觉)(这里|这个)(有点|有些|比较)(问题|模糊|不对)",
    ],
    "clarification_request": [
        r"\bwhat do you mean by\b",
        r"\bcan you (clarify|explain|elaborate)\b",
        r"\bI'?m (not sure|unclear) (what|how|why)\b",
        # CJK clarification patterns
        r"(你说的|这里说的)(.*?)(是什么意思|指的是什么)",
        r"(能否|可以)(解释|说明|阐述)(一下|清楚)?",
        r"(我不太|我不)(明白|清楚|理解)(你|这里)(说的|的意思)",
    ],
    "progress_check": [
        r"\bhow (is|are|has) (it|the|your) (going|progressed|been)\b",
        r"\bwhere are you (with|on)\b",
        r"\bany (progress|updates|news)\b",
        # CJK progress check patterns
        r"(论文|研究|写作)(进展|进度)(如何|怎么样)?",
        r"(现在|目前)(写到|进行到|做到)(哪里|哪儿|什么程度)",
        r"(有什么|有没有)(进展|新进展|更新)",
    ],
    "emotional_register": [
        r"\bdon't worry\b",
        r"\bkeep going\b",
        r"\bI know (this|it) (is|can be) (hard|difficult|challenging)\b",
        r"\byou're (doing|making) (well|progress|good work)\b",
        # CJK emotional register patterns
        r"(不用|别)(担心|着急|焦虑)",
        r"(继续|坚持)(努力|下去|加油)",
        r"(我知道|我了解)(这|这个)(很难|不容易|有挑战)",
        r"(你做得|你的工作)(很好|不错|很努力)",
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

    # Mentor indicators: English titles and CJK honorifics
    mentor_indicators_en = ["prof", "professor", "dr.", "supervisor", "advisor"]
    # CJK mentor indicators in the From field
    mentor_indicators_cjk = ["教授", "老师", "导师"]

    from_lower = from_line.lower()
    # Check English indicators
    if any(ind in from_lower for ind in mentor_indicators_en):
        return "mentor_to_student"
    # Check CJK indicators (case-insensitive not needed for CJK, just substring check)
    if any(ind in from_line for ind in mentor_indicators_cjk):
        return "mentor_to_student"
    # Also check for "Prof" or "Dr" with capital (common in email display names)
    if re.search(r"\b(Prof|Dr)\b", from_line):
        return "mentor_to_student"

    if to_line:
        to_lower = to_line.lower()
        if any(ind in to_lower for ind in mentor_indicators_en):
            return "student_to_mentor"
        if any(ind in to_line for ind in mentor_indicators_cjk):
            return "student_to_mentor"
        if re.search(r"\b(Prof|Dr)\b", to_line):
            return "student_to_mentor"

    return "unknown"


def _classify_email_type(body: str) -> str:
    body_lower = body.lower()
    admin_hits = sum(1 for kw in ADMIN_KEYWORDS if kw in body_lower or kw in body)
    advisory_hits = sum(1 for kw in ADVISORY_KEYWORDS if kw in body_lower or kw in body)

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
            if re.search(pattern, body_lower, re.UNICODE) or re.search(pattern, body, re.UNICODE):
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
