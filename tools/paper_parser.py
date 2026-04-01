"""
paper_parser.py

Parse academic papers and book chapters to extract functionally-typed segments
for use by method_analyzer.md.

Supports plain text (.txt), Markdown (.md), PDF (via pdfminer or pypdf),
and Word documents (.docx via python-docx).

Usage:
    from tools.paper_parser import parse_paper
    segments = parse_paper("path/to/paper.pdf")
"""

import re
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class Segment:
    text: str
    source_file: str
    section_heading: str = ""
    # Likely functional type based on heuristics
    candidate_types: list[str] = field(default_factory=list)
    page_number: int | None = None


FUNCTION_PATTERNS = {
    "problem_framing": [
        r"\bresearch (question|problem|puzzle)\b",
        r"\bwhy (does|do|is|are)\b",
        r"\bremains (unclear|understudied|unexplained|contested)\b",
        r"\bthis paper (argues|examines|investigates|asks)\b",
        r"\bthe central (question|puzzle|problem)\b",
        # CJK patterns
        r"本文(认为|旨在|试图|探讨|分析|研究)",
        r"笔者(认为|以为|认识到|发现)",
        r"研究(问题|目的|意义|方法|表明)",
        r"(尚未|仍然|目前)(明确|清晰|解决|阐明)",
        r"(核心|主要|关键)(问题|议题|矛盾)",
    ],
    "conceptual_definition": [
        r"\bI (define|use|mean) ['\"]?\w",
        r"\bby ['\"]?\w+['\"]? I mean\b",
        r"\bthe (term|concept|notion) of\b",
        r"\bshould (not )?be confused with\b",
        r"\bdistinguish between\b",
        # CJK patterns
        r"(本文|笔者)(将|把|所)(说的|使用的|定义的)",
        r"区别于",
        r"所谓[\"'「『]?\w",
        r"(概念|术语|定义)(是指|指的是|包括)",
        r"(不同于|有别于|区分)",
    ],
    "literature_critique": [
        r"\bexisting (work|literature|scholarship|studies)\b",
        r"\bprevious (work|research|scholars)\b",
        r"\b(overlooks|neglects|fails to|ignores|misses)\b",
        r"\bhowever,\s+(this|these|such)\b",
        r"\bdespite (its|their|this)\b",
        # CJK patterns
        r"(已有|现有|既有)(研究|文献|成果|学者)",
        r"(忽视了|忽略了|未能|没有)(关注|考虑|解释|说明)",
        r"(然而|但是|不过)[，,](这|这些|此)",
        r"尽管(如此|这样)",
        r"(前人|前期|已有)(研究|工作)(的|存在)(不足|局限|缺陷)",
    ],
    "method_explanation": [
        r"\b(I|we) (conducted|collected|analyzed|interviewed|observed)\b",
        r"\bmy (method|approach|data|analysis)\b",
        r"\bcase stud(y|ies)\b",
        r"\b(qualitative|quantitative|ethnograph|survey|experiment)\b",
        r"\bdata (were|was|are) (collected|drawn|derived)\b",
        # CJK patterns
        r"(本文|笔者|我们)(采用|运用|使用|选取)(了)?",
        r"(研究方法|分析方法|数据收集)",
        r"(访谈|问卷|田野|案例)(调查|研究|分析)",
        r"(定性|定量|混合)(研究|方法|分析)",
        r"(数据|资料)(来源|来自|收集|整理)",
    ],
    "theoretical_positioning": [
        r"\b(drawing on|building on|departing from|following)\b.*\b(theory|framework|tradition)\b",
        r"\bI (argue|contend|claim) that\b",
        r"\bin contrast to\b",
        r"\bthis (approach|framework|perspective)\b",
        # CJK patterns
        r"(借鉴|援引|运用|基于)(.*?)(理论|框架|视角|传统)",
        r"(本文|笔者)(认为|主张|坚持|强调)",
        r"与(.*?)相比|相对于(.*?)而言",
        r"(本文|这一)(视角|框架|取径)",
    ],
    "conclusion_judgment": [
        r"\bthis (suggests|implies|shows|demonstrates|reveals)\b",
        r"\bthe (finding|result|implication)\b",
        r"\bwe (can|should|must) (conclude|note|recognize)\b",
        r"\bin sum\b",
        r"\btaken together\b",
        # CJK patterns
        r"(这|此)(表明|说明|揭示|显示|意味着)",
        r"(研究|分析)(发现|结果|结论|启示)",
        r"(综上所述|总而言之|由此可见)",
        r"(我们|本文)(可以|应当|必须)(得出|认识到|注意到)",
    ],
}


def _count_cjk(text: str) -> int:
    """Count CJK (Chinese/Japanese/Korean) characters in text."""
    return sum(1 for c in text if "\u4e00" <= c <= "\u9fff")


def _is_cjk_dominant(text: str, threshold: float = 0.2) -> bool:
    """Return True if more than threshold fraction of chars are CJK."""
    if not text:
        return False
    return _count_cjk(text) / len(text) >= threshold


def parse_paper(filepath: str | Path, min_segment_words: int = 40, min_cjk_chars: int = 80) -> list[Segment]:
    """
    Parse a paper into labeled segments.
    Returns a list of Segment objects.

    For CJK-dominant text, uses character count (min_cjk_chars) instead of
    word count (min_segment_words) to determine segment length threshold.
    """
    filepath = Path(filepath)
    suffix = filepath.suffix.lower()

    if suffix == ".pdf":
        text = _read_pdf(filepath)
    elif suffix in (".txt", ".md"):
        text = filepath.read_text(encoding="utf-8", errors="replace")
    elif suffix == ".docx":
        text = _read_docx(filepath)
    else:
        raise ValueError(f"Unsupported file type: {suffix}. Use .pdf, .txt, .md, or .docx")

    raw_segments = _split_into_segments(text)
    segments = []
    for heading, body in raw_segments:
        # Choose length check based on content type
        if _is_cjk_dominant(body):
            if _count_cjk(body) < min_cjk_chars:
                continue
        else:
            if len(body.split()) < min_segment_words:
                continue
        candidate_types = _classify_segment(body)
        segments.append(
            Segment(
                text=body.strip(),
                source_file=str(filepath),
                section_heading=heading,
                candidate_types=candidate_types,
            )
        )
    return segments


def _split_into_segments(text: str) -> list[tuple[str, str]]:
    """
    Split text into (heading, body) pairs by section headings.
    Falls back to paragraph-level splitting if no headings found.
    """
    # Try Markdown-style headings
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

    # Fall back: split by double newline (paragraphs)
    paragraphs = re.split(r"\n\s*\n", text)
    return [("", p.strip()) for p in paragraphs if p.strip()]


def _classify_segment(text: str) -> list[str]:
    """
    Return a list of likely functional types for a text segment.
    A segment may match multiple types.
    Uses re.UNICODE so CJK ranges work correctly.
    """
    matches = []
    text_lower = text.lower()
    for func_type, patterns in FUNCTION_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower, re.UNICODE):
                matches.append(func_type)
                break
    return matches or ["unclassified"]


def _read_pdf(filepath: Path) -> str:
    """
    Extract text from PDF. Tries pdfminer first, falls back to pypdf.
    """
    try:
        from pdfminer.high_level import extract_text
        return extract_text(str(filepath))
    except ImportError:
        pass

    try:
        import pypdf
        reader = pypdf.PdfReader(str(filepath))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except ImportError:
        pass

    raise ImportError(
        "PDF parsing requires pdfminer.six or pypdf. "
        "Install with: pip install pdfminer.six"
    )


def _read_docx(filepath: Path) -> str:
    """
    Extract text from a Word .docx file using python-docx.
    """
    try:
        from docx import Document
        doc = Document(str(filepath))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except ImportError:
        raise ImportError(
            "DOCX parsing requires python-docx. "
            "Install with: pip install python-docx"
        )


def segments_to_markdown(segments: list[Segment]) -> str:
    """
    Format parsed segments as Markdown for review or passing to method_analyzer.
    """
    lines = []
    for i, seg in enumerate(segments, 1):
        types_str = ", ".join(seg.candidate_types)
        lines.append(f"### Segment {i}")
        if seg.section_heading:
            lines.append(f"**Section:** {seg.section_heading}")
        lines.append(f"**Candidate types:** {types_str}")
        lines.append(f"**Source:** {seg.source_file}")
        lines.append("")
        lines.append(seg.text)
        lines.append("")
    return "\n".join(lines)
