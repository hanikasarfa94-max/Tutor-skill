"""
annotation_parser.py

Parse mentor annotations on student papers.
Annotations may come from:
  - PDF comments exported as text (e.g. from Acrobat or Zotero)
  - Inline comments in a Word document exported as plain text
  - Manually typed annotation summaries

Usage:
    from tools.annotation_parser import parse_annotations
    annotations = parse_annotations("path/to/annotations.txt")
"""

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Annotation:
    text: str
    source_file: str
    annotation_type: str = "unknown"
    # Types: criticism / revision_instruction / question / praise / general_comment
    target_context: str = ""   # the student text being annotated, if available
    patterns: list[str] = field(default_factory=list)
    # Behavioral patterns extracted: e.g. "demands_clarification", "flags_vagueness"


ANNOTATION_TYPE_PATTERNS = {
    "criticism": [
        r"\b(wrong|incorrect|not right|misses the point|unclear|vague|weak|confused)\b",
        r"\bthis (doesn't|does not|isn't|is not)\b",
        r"\bno[,.]?\s",
        r"\bproblem (here|with this)\b",
    ],
    "revision_instruction": [
        r"\b(revise|rewrite|rephrase|cut|expand|clarify|add|remove|move)\b",
        r"\bshould (be|say|read)\b",
        r"\bneed(s)? to\b",
        r"\b(see|check|look at)\b",
    ],
    "question": [
        r"\?$",
        r"\bwhat (do you mean|is your|are you)\b",
        r"\bwhy (do you|is this|does this)\b",
        r"\bhow (do you|does this|is this)\b",
    ],
    "praise": [
        r"\b(good|well done|exactly|right|correct|nice|strong|clear)\b",
        r"\byes[,.]?\s",
        r"\bthis (works|is good|is right)\b",
    ],
    "general_comment": [],  # fallback
}

BEHAVIORAL_SIGNAL_PATTERNS = {
    "demands_clarification": [
        r"\bwhat do you mean\b",
        r"\bdefine\b",
        r"\bclarify\b",
        r"\bunclear\b",
    ],
    "flags_vagueness": [
        r"\btoo vague\b",
        r"\bhand.?waving\b",
        r"\bneed(s)? more precision\b",
        r"\bwhat exactly\b",
    ],
    "requests_evidence": [
        r"\bsource[?]?\b",
        r"\bevidence[?]?\b",
        r"\bcite\b",
        r"\bwhere (does|do) (this|you)\b",
    ],
    "pushes_deeper": [
        r"\bso what\b",
        r"\bwhat follows from this\b",
        r"\band\?\s*$",
        r"\bwhat does this (mean|imply|show)\b",
    ],
    "corrects_framing": [
        r"\bthe (real|actual|underlying) (question|issue|problem)\b",
        r"\bthat's not the (question|issue)\b",
        r"\bframe(d|ing) (this|it) (as|differently)\b",
    ],
    "assigns_task": [
        r"\bby (next|Thursday|the end)\b",
        r"\bfor (next week|our next meeting)\b",
        r"\bplease (read|write|send|revise)\b",
    ],
}


def parse_annotations(filepath: str | Path) -> list[Annotation]:
    """
    Parse an annotation file into a list of Annotation objects.
    """
    filepath = Path(filepath)
    text = filepath.read_text(encoding="utf-8", errors="replace")

    raw_annotations = _split_annotations(text)
    result = []
    for raw in raw_annotations:
        ann_type = _classify_annotation_type(raw)
        patterns = _extract_behavioral_signals(raw)
        result.append(
            Annotation(
                text=raw.strip(),
                source_file=str(filepath),
                annotation_type=ann_type,
                patterns=patterns,
            )
        )
    return result


def _split_annotations(text: str) -> list[str]:
    """
    Split annotation file into individual annotation units.
    Handles several common export formats.
    """
    # Format 1: numbered annotations like "1. [note text]" or "Comment 1: ..."
    numbered = re.split(r"\n(?=\d+[.)]\s|Comment\s+\d+[:.])", text)
    if len(numbered) > 3:
        return [a.strip() for a in numbered if a.strip()]

    # Format 2: separator lines like "---" or "==="
    separated = re.split(r"\n[-=]{3,}\n", text)
    if len(separated) > 3:
        return [a.strip() for a in separated if a.strip()]

    # Format 3: paragraph-level split
    paragraphs = re.split(r"\n\s*\n", text)
    return [p.strip() for p in paragraphs if p.strip()]


def _classify_annotation_type(text: str) -> str:
    text_lower = text.lower()
    for ann_type, patterns in ANNOTATION_TYPE_PATTERNS.items():
        if ann_type == "general_comment":
            continue
        for pattern in patterns:
            if re.search(pattern, text_lower):
                return ann_type
    return "general_comment"


def _extract_behavioral_signals(text: str) -> list[str]:
    text_lower = text.lower()
    signals = []
    for signal, patterns in BEHAVIORAL_SIGNAL_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                signals.append(signal)
                break
    return signals


def summarize_patterns(annotations: list[Annotation]) -> dict:
    """
    Aggregate behavioral signals across all annotations.
    Returns a frequency dict useful for persona analysis.
    """
    from collections import Counter
    type_counts = Counter(a.annotation_type for a in annotations)
    signal_counts: Counter = Counter()
    for a in annotations:
        signal_counts.update(a.patterns)

    return {
        "total_annotations": len(annotations),
        "type_distribution": dict(type_counts),
        "behavioral_signals": dict(signal_counts.most_common()),
    }


def annotations_to_markdown(annotations: list[Annotation]) -> str:
    """
    Format annotations as Markdown for passing to mentoring_style_analyzer.
    """
    lines = []
    for i, ann in enumerate(annotations, 1):
        lines.append(f"### Annotation {i}")
        lines.append(f"**Type:** {ann.annotation_type}")
        if ann.patterns:
            lines.append(f"**Behavioral signals:** {', '.join(ann.patterns)}")
        lines.append(f"**Source:** {ann.source_file}")
        lines.append("")
        lines.append(ann.text)
        lines.append("")
    return "\n".join(lines)
