"""
paper_parser.py

Parse academic papers and book chapters to extract functionally-typed segments
for use by method_analyzer.md.

Supports plain text (.txt), Markdown (.md), and PDF (via pdfminer or pypdf).

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
    ],
    "conceptual_definition": [
        r"\bI (define|use|mean) ['\"]?\w",
        r"\bby ['\"]?\w+['\"]? I mean\b",
        r"\bthe (term|concept|notion) of\b",
        r"\bshould (not )?be confused with\b",
        r"\bdistinguish between\b",
    ],
    "literature_critique": [
        r"\bexisting (work|literature|scholarship|studies)\b",
        r"\bprevious (work|research|scholars)\b",
        r"\b(overlooks|neglects|fails to|ignores|misses)\b",
        r"\bhowever,\s+(this|these|such)\b",
        r"\bdespite (its|their|this)\b",
    ],
    "method_explanation": [
        r"\b(I|we) (conducted|collected|analyzed|interviewed|observed)\b",
        r"\bmy (method|approach|data|analysis)\b",
        r"\bcase stud(y|ies)\b",
        r"\b(qualitative|quantitative|ethnograph|survey|experiment)\b",
        r"\bdata (were|was|are) (collected|drawn|derived)\b",
    ],
    "theoretical_positioning": [
        r"\b(drawing on|building on|departing from|following)\b.*\b(theory|framework|tradition)\b",
        r"\bI (argue|contend|claim) that\b",
        r"\bin contrast to\b",
        r"\bthis (approach|framework|perspective)\b",
    ],
    "conclusion_judgment": [
        r"\bthis (suggests|implies|shows|demonstrates|reveals)\b",
        r"\bthe (finding|result|implication)\b",
        r"\bwe (can|should|must) (conclude|note|recognize)\b",
        r"\bin sum\b",
        r"\btaken together\b",
    ],
}


def parse_paper(filepath: str | Path, min_segment_words: int = 40) -> list[Segment]:
    """
    Parse a paper into labeled segments.
    Returns a list of Segment objects.
    """
    filepath = Path(filepath)
    suffix = filepath.suffix.lower()

    if suffix == ".pdf":
        text = _read_pdf(filepath)
    elif suffix in (".txt", ".md"):
        text = filepath.read_text(encoding="utf-8", errors="replace")
    else:
        raise ValueError(f"Unsupported file type: {suffix}. Use .pdf, .txt, or .md")

    raw_segments = _split_into_segments(text)
    segments = []
    for heading, body in raw_segments:
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
    """
    matches = []
    text_lower = text.lower()
    for func_type, patterns in FUNCTION_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
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
