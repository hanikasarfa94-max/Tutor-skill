"""
lecture_parser.py

Parse lecture transcripts, course notes, and classroom recordings (as text)
to extract bridge-layer content: how the mentor explains their academic method
to students.

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
    ],
    "student_advice": [
        r"\byou (should|need to|must|ought to)\b",
        r"\bthe (mistake|error|trap) (most|many|students) (make|fall into)\b",
        r"\bdon'?t (make the mistake|confuse|conflate|assume)\b",
        r"\bI (want|would like) (you|your work) to\b",
        r"\bwhat (good|strong|successful) (work|theses|papers) do\b",
    ],
    "self_description": [
        r"\bin my (work|research|approach|writing)\b",
        r"\bI (always|usually|tend to|try to)\b",
        r"\bwhen I (approach|analyze|read|write)\b",
        r"\bmy (argument|claim|position|method) (is|was|has been)\b",
    ],
    "method_demonstration": [
        r"\blet me (show you|demonstrate|walk you through)\b",
        r"\btake (this|the) (example|case|passage)\b",
        r"\blook at (how|what|why)\b",
        r"\bhere is (how|what|why|an example)\b",
    ],
    "standard_setting": [
        r"\ba (good|strong|successful) (paper|thesis|argument|claim)\b",
        r"\bwhat (makes|distinguishes) (good|strong|excellent) work\b",
        r"\bthe standard (I|we|this field) (use|apply|hold)\b",
        r"\byou (pass|succeed|fail) when\b",
    ],
    "warning_to_students": [
        r"\bcommon (mistake|error|trap|pitfall)\b",
        r"\bdon'?t (confuse|assume|jump to|skip)\b",
        r"\bstudents (often|frequently|tend to)\b",
        r"\bthe danger (here|of this) is\b",
        r"\bwhat (goes wrong|people get wrong)\b",
    ],
}


def parse_lecture(filepath: str | Path, min_segment_words: int = 30) -> list[LectureSegment]:
    """
    Parse a lecture text file into bridge-layer segments.
    """
    filepath = Path(filepath)
    text = filepath.read_text(encoding="utf-8", errors="replace")

    raw_segments = _split_into_segments(text)
    result = []
    for section, body in raw_segments:
        if len(body.split()) < min_segment_words:
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


def _split_into_segments(text: str) -> list[tuple[str, str]]:
    """Split by heading or speaker markers, fall back to paragraphs."""
    # Speaker transcript format: "PROFESSOR: ..." or "Q: ..."
    speaker_re = re.compile(r"^(?:PROFESSOR|PROF|INSTRUCTOR|DR\.?\s+\w+):\s*", re.MULTILINE | re.IGNORECASE)
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
            if re.search(pattern, text_lower):
                signals.append(signal)
                break
    return signals


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
