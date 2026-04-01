"""
annotation_parser.py

Parse mentor annotations on student papers.
Annotations may come from:
  - PDF comments exported as text (e.g. from Acrobat or Zotero)
  - Inline comments in a Word document exported as plain text
  - Manually typed annotation summaries
  - Chinese/CJK annotations from any of the above

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
        # CJK criticism patterns
        r"(不对|有问题|不清楚|需要修改)[，,。！!]?",
        r"(这里|这个|这段)(不对|有问题|不清楚|不准确)",
        r"(论证|表述|分析)(有问题|不清楚|不够准确|存在错误)",
        r"(这(样|种)(说法|论点|表述)(不对|有问题|值得商榷))",
    ],
    "revision_instruction": [
        r"\b(revise|rewrite|rephrase|cut|expand|clarify|add|remove|move)\b",
        r"\bshould (be|say|read)\b",
        r"\bneed(s)? to\b",
        r"\b(see|check|look at)\b",
        # CJK revision instruction patterns
        r"(请修改|需要修改|应该修改)",
        r"(请(重新|再)写|重写|改写)(这(里|段|句))?",
        r"(需要|应该)(补充|删除|移动|调整|扩展|压缩)",
        r"(参考|查看|看一下)(文献|资料|例子|参考)",
        r"(这里)(需要|应该)(更(清楚|详细|具体|完整))",
    ],
    "question": [
        r"\?$",
        r"\bwhat (do you mean|is your|are you)\b",
        r"\bwhy (do you|is this|does this)\b",
        r"\bhow (do you|does this|is this)\b",
        # CJK question patterns — note: check original text for "？"
        r"[？?]\s*$",
        r"(这里|这个)(是什么意思|指的是什么|怎么理解)[？?]?",
        r"(为什么|怎么|如何)(这样(说|写|论证))[？?]?",
    ],
    "praise": [
        r"\b(good|well done|exactly|right|correct|nice|strong|clear)\b",
        r"\byes[,.]?\s",
        r"\bthis (works|is good|is right)\b",
        # CJK praise patterns
        r"(很好|准确|清晰)[！!。，,]?",
        r"(这(里|段|句|部分))(很好|不错|准确|清晰|有力)",
        r"(论证|表述|分析)(很好|准确|清晰|到位|有力)",
        r"(写得|分析得)(很好|不错|准确|清楚)",
    ],
    "general_comment": [],  # fallback
}

BEHAVIORAL_SIGNAL_PATTERNS = {
    "demands_clarification": [
        r"\bwhat do you mean\b",
        r"\bdefine\b",
        r"\bclarify\b",
        r"\bunclear\b",
        # CJK demands clarification patterns
        r"(什么意思)[？?]?",
        r"(你说的|这里说的)(.*?)(是什么|指的是什么|什么意思)",
        r"(请(说|解释)(清楚|明白|一下))",
        r"(含义不清|表述不明|语义模糊)",
    ],
    "flags_vagueness": [
        r"\btoo vague\b",
        r"\bhand.?waving\b",
        r"\bneed(s)? more precision\b",
        r"\bwhat exactly\b",
        # CJK flags vagueness patterns
        r"(太模糊|不够精确|不够具体|过于笼统)",
        r"(说清楚|说(得|地)更清楚|写(得|地)更清楚)",
        r"(这里(过于|太)(模糊|抽象|笼统))",
        r"(需要更(精确|具体|清晰)(的描述|的表述|地说明))",
    ],
    "requests_evidence": [
        r"\bsource[?]?\b",
        r"\bevidence[?]?\b",
        r"\bcite\b",
        r"\bwhere (does|do) (this|you)\b",
        # CJK requests evidence patterns
        r"(出处|依据|来源)[？?]",
        r"(哪里说的|哪里有这个|依据是什么)[？?]?",
        r"(请引用|需要(引用|注明)(来源|出处|文献))",
        r"(这(个|种)说法的)(依据|出处|来源)(是什么|在哪里)[？?]?",
    ],
    "pushes_deeper": [
        r"\bso what\b",
        r"\bwhat follows from this\b",
        r"\band\?\s*$",
        r"\bwhat does this (mean|imply|show)\b",
        # CJK pushes deeper patterns
        r"(所以呢|那又怎样|这说明什么)[？?]?",
        r"(这(意味着|说明|暗示)(什么|了什么))[？?]?",
        r"(进一步(说|分析|论证)(会|能)(发现|得出|看到))",
    ],
    "corrects_framing": [
        r"\bthe (real|actual|underlying) (question|issue|problem)\b",
        r"\bthat's not the (question|issue)\b",
        r"\bframe(d|ing) (this|it) (as|differently)\b",
        # CJK corrects framing patterns
        r"(真正的|实际的|核心的)(问题|议题|矛盾)(是|在于)",
        r"(这不是(真正的|核心的)问题)",
        r"(应该(换个|换一个|用不同的)(角度|视角|框架)(来看|来分析))",
        r"(问题(的实质|的关键|所在)(是|在于))",
    ],
    "assigns_task": [
        r"\bby (next|Thursday|the end)\b",
        r"\bfor (next week|our next meeting)\b",
        r"\bplease (read|write|send|revise)\b",
        # CJK assigns task patterns
        r"(下周|下次|月底)(前|之前)(提交|完成|修改|发送)",
        r"(请(你|您))(阅读|修改|撰写|发送|准备)",
        r"(在(我们)?下次(见面|开会)前)(完成|修改|提交)",
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
            # Try both lowercased (for English) and original (for CJK)
            if re.search(pattern, text_lower, re.UNICODE) or re.search(pattern, text, re.UNICODE):
                return ann_type
    return "general_comment"


def _extract_behavioral_signals(text: str) -> list[str]:
    text_lower = text.lower()
    signals = []
    for signal, patterns in BEHAVIORAL_SIGNAL_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower, re.UNICODE) or re.search(pattern, text, re.UNICODE):
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
