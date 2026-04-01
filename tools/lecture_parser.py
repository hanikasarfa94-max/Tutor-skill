"""
lecture_parser.py

Parse lecture transcripts, course notes, classroom recordings (as text),
and conference/meeting notes to extract bridge-layer content: how the mentor
explains their academic method to students.

Supports .txt, .md, and .docx files.

Usage:
    from tools.lecture_parser import parse_lecture
    segments = parse_lecture("path/to/lecture.txt")
"""

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class LectureSegment:
    text: str
    source_file: str
    section: str = ""
    bridge_signals: list[str] = field(default_factory=list)
    # Bridge signals: concept_explanation / student_advice / self_description /
    #                 method_demonstration / standard_setting / warning_to_students


BRIDGE_SIGNAL_PATTERNS = {
    "concept_explanation": [
        r"\bwhat I mean (by|when I say)\b",
        r"\blet me (explain|unpack|clarify)\b",
        r"\bthink of it (as|like)\b",
        r"\bthe (idea|point|concept) (here|is that)\b",
        r"\bin other words\b",
        # CJK concept explanation patterns
        r"(我的意思是|也就是说|换句话说)",
        r"(这里|这个)(是指|指的是|的意思是)",
        r"(简单(来|地)说|通俗(来|地)讲)",
        r"(让我(来)?(解释|说明|澄清))",
        r"(用(另一种|更简单的)方式(来)?(说|理解))",
    ],
    "student_advice": [
        r"\byou (should|need to|must|ought to)\b",
        r"\bthe (mistake|error|trap) (most|many|students) (make|fall into)\b",
        r"\bdon'?t (make the mistake|confuse|conflate|assume)\b",
        r"\bI (want|would like) (you|your work) to\b",
        r"\bwhat (good|strong|successful) (work|theses|papers) do\b",
        # CJK student advice patterns
        r"(你(们)?应该|你(们)?需要|你(们)?要)(注意|了解|掌握|避免)",
        r"要注意[，,]",
        r"不要(犯|出现|重复)(这种|这个|同样的)(错误|问题|毛病)",
        r"(写论文|做研究|分析问题)(时|的时候)[，,](要|需要|应该)",
        r"(好的|优秀的)(论文|研究|工作)(应该|需要|必须)",
    ],
    "self_description": [
        r"\bin my (work|research|approach|writing)\b",
        r"\bI (always|usually|tend to|try to)\b",
        r"\bwhen I (approach|analyze|read|write)\b",
        r"\bmy (argument|claim|position|method) (is|was|has been)\b",
        # CJK self description patterns
        r"(我在(自己的)?研究中|我的(研究|工作|写作)中)",
        r"(我的做法是|我通常(会|是)|我一般(会|是))",
        r"(当我(分析|阅读|写作|处理)(.*?)时)",
        r"(我的(论点|主张|立场|方法)(是|在于))",
        r"(我(通常|一般|总是)(倾向于|会|先))",
    ],
    "method_demonstration": [
        r"\blet me (show you|demonstrate|walk you through)\b",
        r"\btake (this|the) (example|case|passage)\b",
        r"\blook at (how|what|why)\b",
        r"\bhere is (how|what|why|an example)\b",
        # CJK method demonstration patterns
        r"(让我(来)?(给你们?|向你们?)(展示|演示|说明))",
        r"(以这(个|篇|份)(例子|案例|文章|段落)(为例|来看))",
        r"(来看(一下|看)(这里|这个|这段)(如何|怎么))",
        r"(下面(我来|是)(一个|一种)(示例|演示|说明))",
    ],
    "standard_setting": [
        r"\ba (good|strong|successful) (paper|thesis|argument|claim)\b",
        r"\bwhat (makes|distinguishes) (good|strong|excellent) work\b",
        r"\bthe standard (I|we|this field) (use|apply|hold)\b",
        r"\byou (pass|succeed|fail) when\b",
        # CJK standard setting patterns
        r"(一篇|一份)(好的|优秀的|合格的)(论文|文章|研究)(应该|需要|必须)",
        r"(什么样的|怎样的)(工作|论文|研究)(才算|才是)(好的|优秀的|达标的)",
        r"(我们这个领域|学术界)(的标准|要求|规范)(是|在于)",
        r"(达到|符合)(要求|标准)(的)(论文|研究|工作)(需要|应该)",
    ],
    "warning_to_students": [
        r"\bcommon (mistake|error|trap|pitfall)\b",
        r"\bdon'?t (confuse|assume|jump to|skip)\b",
        r"\bstudents (often|frequently|tend to)\b",
        r"\bthe danger (here|of this) is\b",
        r"\bwhat (goes wrong|people get wrong)\b",
        # CJK warning patterns
        r"(常见的错误|常犯的错误|常见的问题)(是|包括|有)",
        r"(很多同学|许多学生|大部分同学)(会|容易|经常)(犯|出现|忽视)",
        r"(不要|别)(混淆|误解|想当然|跳过|忽略)",
        r"(这里(的|有个)|这个)(陷阱|误区|问题)(在于|是)",
        r"(大家(要|需要)注意|提醒(大家|同学们?))[，,]",
    ],
}

# Meeting/conference metadata line patterns
_MEETING_META_RE = re.compile(
    r"^(时间|地点|主题|议题|与会人员|主持人|记录人|日期)[：:]\s*.+$",
    re.MULTILINE | re.UNICODE,
)

# Speaker turn pattern for meeting notes (Chinese name/role followed by colon)
_SPEAKER_TURN_RE = re.compile(
    r"^([\u4e00-\u9fff]{1,10}(?:教授|老师|导师|同学|博士|研究员)?|[A-Za-z][A-Za-z\s\.]{0,30}(?:Prof\.?|Dr\.?)?)[：:]\s*",
    re.MULTILINE | re.UNICODE,
)


def parse_lecture(filepath: str | Path, min_segment_words: int = 30) -> list[LectureSegment]:
    """
    Parse a lecture text file into bridge-layer segments.
    Also handles conference/meeting notes format.
    Supports .txt, .md, and .docx files.
    """
    filepath = Path(filepath)
    suffix = filepath.suffix.lower()

    if suffix == ".docx":
        text = _read_docx(filepath)
    else:
        text = filepath.read_text(encoding="utf-8", errors="replace")

    # Detect if this is a meeting/conference notes format
    if _is_meeting_notes(text):
        raw_segments = _split_meeting_notes(text)
    else:
        raw_segments = _split_into_segments(text)

    result = []
    for section, body in raw_segments:
        if not _segment_long_enough(body, min_segment_words):
            continue
        signals = _extract_bridge_signals(body)
        if not signals:
            continue  # Only keep segments with at least one bridge signal
        result.append(
            LectureSegment(
                text=body.strip(),
                source_file=str(filepath),
                section=section,
                bridge_signals=signals,
            )
        )
    return result


def _segment_long_enough(body: str, min_words: int) -> bool:
    """Check length using word count for English, char count for CJK."""
    cjk_count = sum(1 for c in body if "\u4e00" <= c <= "\u9fff")
    if cjk_count > len(body) * 0.2:
        # CJK-dominant: require at least min_words * 2 CJK characters
        return cjk_count >= min_words * 2
    return len(body.split()) >= min_words


def _is_meeting_notes(text: str) -> bool:
    """Detect if the text looks like conference/meeting notes."""
    meta_hits = len(_MEETING_META_RE.findall(text))
    return meta_hits >= 2


def _split_meeting_notes(text: str) -> list[tuple[str, str]]:
    """
    Split meeting notes into speaker-turn segments.
    Detects lines beginning with a speaker name/role, groups following lines.
    """
    lines = text.split("\n")
    segments = []
    current_speaker = "会议记录"
    current_lines = []

    for line in lines:
        m = _SPEAKER_TURN_RE.match(line)
        if m:
            # Save accumulated block
            if current_lines:
                body = "\n".join(current_lines).strip()
                if body:
                    segments.append((current_speaker, body))
            current_speaker = m.group(1).strip()
            remainder = line[m.end():].strip()
            current_lines = [remainder] if remainder else []
        else:
            current_lines.append(line)

    if current_lines:
        body = "\n".join(current_lines).strip()
        if body:
            segments.append((current_speaker, body))

    # Fallback: if no speaker turns detected, paragraph split
    if not segments:
        paragraphs = re.split(r"\n\s*\n", text)
        return [("", p.strip()) for p in paragraphs if p.strip()]

    return segments


def _split_into_segments(text: str) -> list[tuple[str, str]]:
    """Split by heading or speaker markers, fall back to paragraphs."""
    # Speaker transcript format: "PROFESSOR: ..." or "Q: ..."
    speaker_re = re.compile(
        r"^(?:PROFESSOR|PROF|INSTRUCTOR|DR\.?\s+\w+):\s*",
        re.MULTILINE | re.IGNORECASE,
    )
    speaker_blocks = speaker_re.split(text)
    if len(speaker_blocks) > 3:
        return [("", block.strip()) for block in speaker_blocks if block.strip()]

    # Markdown headings
    heading_re = re.compile(r"^#{1,4}\s+(.+)$", re.MULTILINE)
    positions = [(m.start(), m.group(1)) for m in heading_re.finditer(text)]
    if len(positions) >= 2:
        segments = []
        for i, (pos, heading) in enumerate(positions):
            start = pos + len(f"# {heading}")
            end = positions[i + 1][0] if i + 1 < len(positions) else len(text)
            body = text[start:end].strip()
            if body:
                segments.append((heading, body))
        return segments

    # Paragraph fallback
    paragraphs = re.split(r"\n\s*\n", text)
    return [("", p.strip()) for p in paragraphs if p.strip()]


def _extract_bridge_signals(text: str) -> list[str]:
    text_lower = text.lower()
    signals = []
    for signal, patterns in BRIDGE_SIGNAL_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower, re.UNICODE) or re.search(pattern, text, re.UNICODE):
                signals.append(signal)
                break
    return signals


def _read_docx(filepath: Path) -> str:
    """Extract text from a .docx file. Delegates to paper_parser if available."""
    try:
        # Prefer paper_parser's implementation to avoid duplication
        import sys
        sys.path.insert(0, str(filepath.parent))
        from paper_parser import _read_docx as pp_read_docx
        return pp_read_docx(filepath)
    except ImportError:
        pass

    try:
        from docx import Document
        doc = Document(str(filepath))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except ImportError:
        raise ImportError(
            "DOCX parsing requires python-docx. "
            "Install with: pip install python-docx"
        )


def lecture_to_markdown(segments: list[LectureSegment]) -> str:
    """Format lecture segments as Markdown for bridge_analyzer."""
    lines = []
    for i, seg in enumerate(segments, 1):
        signals_str = ", ".join(seg.bridge_signals)
        lines.append(f"### Segment {i}")
        if seg.section:
            lines.append(f"**Section:** {seg.section}")
        lines.append(f"**Bridge signals:** {signals_str}")
        lines.append(f"**Source:** {seg.source_file}")
        lines.append("")
        lines.append(seg.text)
        lines.append("")
    return "\n".join(lines)
