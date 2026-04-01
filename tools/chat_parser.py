"""
chat_parser.py

Parse instant-message conversation logs (WeChat, DingTalk, Telegram, WhatsApp, Slack, etc.)
exported as plain text to extract:
  - questioning patterns
  - rejection patterns
  - encouragement patterns
  - task assignment patterns

Supported formats:
  - WeChat PC export: "2024-01-01 10:00:00  张老师\n你的论文..." (timestamp + 2+ spaces + name, message on next line)
  - WeChat mobile export: "张老师  10:00\n你的论文..." (name + 2+ spaces + time, message on next line)
  - DingTalk: "[2024-01-01 10:00:00] 发送人: 内容"
  - WhatsApp / Telegram: "2024-01-01 10:00 Name: message"
  - Slack-style: "[timestamp] sender: message"
  - Simple: "Name: message"

Usage:
    from tools.chat_parser import parse_chat
    messages = parse_chat("path/to/chat.txt", mentor_name="张老师")
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
        # CJK question patterns
        r"[？?]\s*$",
        r"(吗|呢|吧)[？?]?\s*$",
        r"(你|您)(觉得|认为|想|看)(.*?)[？?]",
        r"(为什么|怎么|如何|有没有)(.*?)[？?]",
    ],
    "rejection": [
        r"\bno[,.]?\s",
        r"\bnot (quite|right|there yet|convincing)\b",
        r"\bI don'?t (think|see|follow|buy)\b",
        r"\bthat'?s not (the|right|what)\b",
        r"\bthat doesn'?t (work|hold|follow)\b",
        # CJK rejection patterns
        r"不对[，,。]",
        r"这里有问题",
        r"(这个|这里|这样)(不行|不对|有问题|不妥)",
        r"(我认为|我觉得)(这里|这个|这样)(不对|有问题|欠妥)",
        r"(不太|不够)(对|准确|正确|清楚)",
    ],
    "encouragement": [
        r"\b(good|nice|yes|exactly|right|well done|this is (good|strong|clear))\b",
        r"\bkeep (going|it up)\b",
        r"\byou'?re (on the right|making progress|getting there)\b",
        # CJK encouragement patterns
        r"(很好|不错|做得好|写得好)[！!。，,]?",
        r"(继续|保持)(努力|加油|这个方向)",
        r"(这部分|这里|这个)(很好|不错|清楚|准确)",
        r"(你|您)(做得|写得)(很好|不错|出色)",
    ],
    "task_assignment": [
        r"\bplease (read|write|revise|prepare|send|look at)\b",
        r"\bcan you (read|write|prepare|send|look at|think about)\b",
        r"\bI'?d like (you to|to see)\b",
        r"\bby (Thursday|next week|our meeting|Friday|tomorrow)\b",
        r"\bfor (next time|our next meeting|Thursday)\b",
        # CJK task assignment patterns
        r"(下周|下次|下回)",
        r"(把|将).{1,20}(发给|交给|给我)",
        r"(请你|请您)(阅读|撰写|修改|准备|发给我|看一下)",
        r"(在|于)(周[一二三四五六日]|下周|月底)(之前|前)(完成|提交|发送)",
        r"(希望|要求)(你|您)(能|可以|在.*?前)(完成|提交|修改)",
    ],
    "clarification_demand": [
        r"\bwhat (exactly|do you mean by|is your)\b",
        r"\bI'?m not (sure|clear) (what|how|why|which)\b",
        r"\bcan you (clarify|explain|elaborate|be more specific)\b",
        r"\bwhat does ['\"]?\w+['\"]? mean (here|in this context)\b",
        # CJK clarification demand patterns
        r"(你说的|这里说的)(.*?)(什么意思|是指什么)",
        r"(能否|可以)(解释|说明)(一下|清楚)?[？?]?",
        r"(这里|这个)(是什么意思|指的是什么|怎么理解)",
    ],
    "approval": [
        r"\byes[,.]?\s",
        r"\bagree[d]?\b",
        r"\bcorrect\b",
        r"\bthat'?s (right|good|exactly (right|what I))\b",
        # CJK approval patterns
        r"(对|是的|没错)[，,。！!]",
        r"(同意|赞同|认可)(你|您|这个|这种)(观点|说法|做法)?",
        r"(就是|正是)(这样|这个意思|我想要的)",
    ],
    "pushback": [
        r"\bbut (wait|hold on|actually)\b",
        r"\bI (disagree|would push back)\b",
        r"\bnot so fast\b",
        r"\bhave you (considered|thought about) the alternative\b",
        # CJK pushback patterns
        r"(但是|然而|不过)(等等|先等一下|且慢)",
        r"(我(不同意|有不同看法))",
        r"(有没有|你有没有)(考虑过|想过)(另一种|其他)(可能|方法|角度)",
    ],
}

# WeChat PC export: "2024-01-01 10:00:00  张老师" (timestamp + 2+ spaces + name)
_WECHAT_PC_RE = re.compile(
    r"^(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s{2,}(.+)$",
    re.MULTILINE | re.UNICODE,
)

# WeChat mobile export: "张老师  10:00" (name + 2+ spaces + time)
_WECHAT_MOBILE_RE = re.compile(
    r"^(.+?)\s{2,}(\d{1,2}:\d{2})\s*$",
    re.MULTILINE | re.UNICODE,
)

# DingTalk: "[2024-01-01 10:00:00] 发送人: 内容"
_DINGTALK_RE = re.compile(
    r"^\[(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}(?::\d{2})?)\]\s+(.+?):\s+(.+)$",
    re.MULTILINE | re.UNICODE,
)


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
    identifiers = list(mentor_identifiers or [])
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
    # Format 1: WeChat PC export — timestamp + 2+ spaces + name on one line,
    # message on the following line(s)
    pc_matches = list(_WECHAT_PC_RE.finditer(text))
    if len(pc_matches) > 3:
        results = []
        for i, m in enumerate(pc_matches):
            sender = m.group(2).strip()
            # Message body: lines between this header and the next header
            body_start = m.end()
            body_end = pc_matches[i + 1].start() if i + 1 < len(pc_matches) else len(text)
            body = text[body_start:body_end].strip()
            if body:
                results.append((sender, body))
        if results:
            return results

    # Format 2: WeChat mobile export — name + 2+ spaces + time on one line,
    # message on the following line(s)
    mobile_matches = list(_WECHAT_MOBILE_RE.finditer(text))
    if len(mobile_matches) > 3:
        results = []
        for i, m in enumerate(mobile_matches):
            sender = m.group(1).strip()
            body_start = m.end()
            body_end = mobile_matches[i + 1].start() if i + 1 < len(mobile_matches) else len(text)
            body = text[body_start:body_end].strip()
            if body:
                results.append((sender, body))
        if results:
            return results

    # Format 3: DingTalk — "[timestamp] sender: message"
    dt_matches = list(_DINGTALK_RE.finditer(text))
    if len(dt_matches) > 3:
        results = []
        for i, m in enumerate(dt_matches):
            sender = m.group(2).strip()
            body_start_inline = m.group(3)
            # Collect continuation lines until next match
            body_end = dt_matches[i + 1].start() if i + 1 < len(dt_matches) else len(text)
            continuation = text[m.end():body_end].strip()
            body = body_start_inline + (" " + continuation if continuation else "")
            results.append((sender, body))
        return results

    # Format 4: WhatsApp / older WeChat style: "2024-01-01 10:00 Name: message"
    wechat_old_re = re.compile(
        r"^(?:\d{4}[-/]\d{2}[-/]\d{2}\s+\d{2}:\d{2}(?::\d{2})?\s+)?(.+?):\s+(.+)$",
        re.MULTILINE | re.UNICODE,
    )
    matches = list(wechat_old_re.finditer(text))
    if len(matches) > 3:
        results = []
        for i, m in enumerate(matches):
            sender = m.group(1).strip()
            body_start = m.end()
            body_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            body = text[body_start:body_end].strip()
            full_body = m.group(2) + (" " + body if body else "")
            results.append((sender, full_body))
        return results

    # Format 5: Slack-style "[timestamp] sender: message"
    slack_re = re.compile(r"^\[.+?\]\s+(.+?):\s+(.+)$", re.MULTILINE | re.UNICODE)
    matches = list(slack_re.finditer(text))
    if len(matches) > 3:
        return [(m.group(1).strip(), m.group(2).strip()) for m in matches]

    # Format 6: Simple "Name: message" per line (ASCII names only to avoid false positives)
    simple_re = re.compile(r"^([A-Za-z][^:\n]{0,40}):\s+(.+)$", re.MULTILINE | re.UNICODE)
    matches = list(simple_re.finditer(text))
    if len(matches) > 3:
        return [(m.group(1).strip(), m.group(2).strip()) for m in matches]

    # Fallback: treat each paragraph as an undifferentiated message
    return [("unknown", p.strip()) for p in re.split(r"\n\s*\n", text) if p.strip()]


def _is_mentor_message(sender: str, identifiers: list[str]) -> bool:
    if not identifiers:
        return False
    sender_lower = sender.lower()
    return any(ident.lower() in sender_lower or ident in sender for ident in identifiers)


def _extract_patterns(text: str) -> list[str]:
    text_lower = text.lower()
    found = []
    for pattern_name, patterns in MENTOR_MESSAGE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower, re.UNICODE) or re.search(pattern, text, re.UNICODE):
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
            lines.append(f"  -> patterns: {', '.join(msg.patterns)}")
    return "\n".join(lines)
