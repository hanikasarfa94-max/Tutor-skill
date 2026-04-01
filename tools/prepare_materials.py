"""
prepare_materials.py

CLI preprocessing tool. Run this BEFORE /create-mentor.

Takes a directory of raw materials (PDFs, .txt, .md, .docx, email exports,
chat logs, HTML/web articles) and outputs a single structured markdown file
ready for the analyzer prompts.

Usage:
    python tools/prepare_materials.py --dir lzf/ --type papers --output lzf_ready.md
    python tools/prepare_materials.py --dir emails/ --type emails --output emails_ready.md
    python tools/prepare_materials.py --dir materials/ --type auto --output all_ready.md
    python tools/prepare_materials.py --dir web/ --type web --output web_ready.md

Then in Claude:
    /create-mentor
    (when asked for materials, paste the path to the output file or its contents)
"""

import argparse
import glob
import os
import sys
from pathlib import Path

# Add tools dir to path so we can import siblings
sys.path.insert(0, str(Path(__file__).parent))


def process_papers(input_dir: str, min_cjk: int = 800) -> str:
    """Extract and chunk all PDFs, text files, and Word documents as academic papers."""
    from paper_parser import parse_paper, segments_to_markdown

    input_path = Path(input_dir)
    files = (
        list(input_path.glob("*.pdf")) +
        list(input_path.glob("*.txt")) +
        list(input_path.glob("*.md")) +
        list(input_path.glob("*.docx"))
    )

    if not files:
        return f"[No files found in {input_dir}]\n"

    all_segments = []
    skipped = []

    for f in sorted(files):
        # Skip already-extracted .txt files if a PDF with same stem exists
        if f.suffix == ".txt":
            if (f.parent / (f.stem + ".pdf")).exists():
                continue

        try:
            segments = parse_paper(str(f))
            # Filter: only keep segments with enough CJK or Latin content
            good = [s for s in segments if _has_content(s.text, min_cjk)]
            all_segments.extend(good)
        except Exception as e:
            skipped.append(f"{f.name}: {e}")

    output = f"# Academic Papers — Preprocessed\n\n"
    output += f"Source directory: `{input_dir}`\n"
    output += f"Files processed: {len(files)}\n"
    output += f"Segments extracted: {len(all_segments)}\n"
    if skipped:
        output += f"\nSkipped ({len(skipped)}):\n"
        for s in skipped:
            output += f"  - {s}\n"
    output += "\n---\n\n"
    output += segments_to_markdown(all_segments)
    return output


def process_emails(input_dir: str) -> str:
    """Extract and filter all email files."""
    from email_parser import parse_emails, filter_advisory, filter_mentor_to_student, emails_to_markdown

    input_path = Path(input_dir)
    files = list(input_path.glob("*.txt")) + list(input_path.glob("*.eml")) + list(input_path.glob("*.mbox"))

    if not files:
        return f"[No email files found in {input_dir}]\n"

    all_emails = []
    for f in sorted(files):
        try:
            emails = parse_emails(str(f))
            # Prefer advisory + mentor-to-student; fall back to all
            advisory = filter_advisory(emails)
            all_emails.extend(advisory if advisory else emails)
        except Exception as e:
            pass

    output = f"# Emails — Preprocessed\n\n"
    output += f"Source: `{input_dir}` | Emails extracted: {len(all_emails)}\n\n---\n\n"
    output += emails_to_markdown(all_emails)
    return output


def process_chats(input_dir: str, mentor_name: str = "") -> str:
    """Extract and filter chat logs. Supports .txt and .csv WeChat exports."""
    from chat_parser import parse_chat, mentor_messages, chat_to_markdown, summarize_patterns

    input_path = Path(input_dir)
    files = list(input_path.glob("*.txt")) + list(input_path.glob("*.csv"))

    if not files:
        return f"[No chat files found in {input_dir}]\n"

    all_messages = []
    for f in sorted(files):
        try:
            # For CSV WeChat exports: read as text, the parser handles the format
            msgs = parse_chat(str(f), mentor_name=mentor_name or None)
            all_messages.extend(msgs)
        except Exception as e:
            pass

    summary = summarize_patterns(all_messages)
    output = f"# Chat Logs — Preprocessed\n\n"
    output += f"Source: `{input_dir}` | Total messages: {summary['total_messages']} | Mentor messages: {summary['total_mentor_messages']}\n"
    output += f"Pattern frequencies: {summary['pattern_frequencies']}\n\n---\n\n"
    output += chat_to_markdown(all_messages, mentor_only=True)
    return output


def process_lectures(input_dir: str) -> str:
    """Extract bridge-layer segments from lecture transcripts and meeting notes."""
    from lecture_parser import parse_lecture, lecture_to_markdown

    input_path = Path(input_dir)
    files = (
        list(input_path.glob("*.txt")) +
        list(input_path.glob("*.md")) +
        list(input_path.glob("*.docx"))
    )

    if not files:
        return f"[No lecture files found in {input_dir}]\n"

    all_segments = []
    for f in sorted(files):
        try:
            segs = parse_lecture(str(f))
            all_segments.extend(segs)
        except Exception as e:
            pass

    output = f"# Lecture Transcripts — Preprocessed\n\n"
    output += f"Source: `{input_dir}` | Bridge segments: {len(all_segments)}\n\n---\n\n"
    output += lecture_to_markdown(all_segments)
    return output


def process_web_articles(input_dir: str) -> str:
    """
    Process web articles (.html) and Markdown files from WeChat public accounts,
    Weibo posts, blogs, etc. Strips HTML tags and classifies as bridge material (Category C).
    """
    input_path = Path(input_dir)
    files = list(input_path.glob("*.html")) + list(input_path.glob("*.htm"))

    # Also include .md files that aren't already handled as papers
    md_files = list(input_path.glob("*.md"))
    files.extend(md_files)

    if not files:
        return f"[No web article files found in {input_dir}]\n"

    all_texts = []
    skipped = []

    for f in sorted(files):
        try:
            raw = f.read_text(encoding="utf-8", errors="replace")
            if f.suffix.lower() in (".html", ".htm"):
                text = _strip_html(raw)
            else:
                # Plain markdown: remove markdown syntax, keep text
                text = raw
            text = text.strip()
            if text:
                all_texts.append((f.name, text))
        except Exception as e:
            skipped.append(f"{f.name}: {e}")

    output = "# Web Articles — Preprocessed (Category C: Bridge Material)\n\n"
    output += f"Source: `{input_dir}` | Articles processed: {len(all_texts)}\n"
    if skipped:
        output += f"Skipped ({len(skipped)}): {', '.join(s.split(':')[0] for s in skipped)}\n"
    output += "\n---\n\n"

    for name, text in all_texts:
        output += f"### Article: {name}\n\n"
        output += text
        output += "\n\n---\n\n"

    return output


def _strip_html(html: str) -> str:
    """Strip HTML tags using BeautifulSoup, falling back to regex."""
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        # Remove script and style elements
        for tag in soup(["script", "style", "head", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator="\n")
    except ImportError:
        # Fallback: simple regex tag stripping
        text = re.sub(r"<[^>]+>", " ", html)
        text = re.sub(r"&[a-zA-Z]+;", " ", text)
        text = re.sub(r"\s{2,}", "\n", text)
        return text.strip()


def auto_detect(input_dir: str, mentor_name: str = "") -> str:
    """Auto-detect file types and run appropriate parsers."""
    import re as _re
    input_path = Path(input_dir)
    output_parts = []

    pdfs = list(input_path.glob("*.pdf"))
    docxs = list(input_path.glob("*.docx"))
    txts = list(input_path.glob("*.txt"))
    emls = list(input_path.glob("*.eml")) + list(input_path.glob("*.mbox"))
    htmls = list(input_path.glob("*.html")) + list(input_path.glob("*.htm"))

    # Heuristic: if we have PDFs or DOCX files, treat as papers
    if pdfs or docxs:
        output_parts.append(process_papers(input_dir))

    # If we have .eml or .mbox files, treat as emails
    if emls:
        output_parts.append(process_emails(input_dir))

    # If HTML files found, process as web articles
    if htmls:
        output_parts.append(process_web_articles(input_dir))

    # If .txt files without matching PDFs: could be chat or plain text papers
    lone_txts = [f for f in txts if not (f.parent / (f.stem + ".pdf")).exists()]
    if lone_txts:
        # Peek first file to guess type
        sample = lone_txts[0].read_text(encoding="utf-8", errors="replace")[:500]
        if _looks_like_chat(sample):
            output_parts.append(process_chats(input_dir, mentor_name))
        else:
            output_parts.append(process_papers(input_dir))

    if not output_parts:
        return f"[No processable files found in {input_dir}]\n"

    return "\n\n".join(output_parts)


def _has_content(text: str, min_cjk: int) -> bool:
    cjk = sum(1 for c in text if "\u4e00" <= c <= "\u9fff")
    if cjk >= min_cjk:
        return True
    # Also accept long English text
    if len(text.split()) >= 60:
        return True
    return False


def _looks_like_chat(sample: str) -> bool:
    import re
    chat_patterns = [
        r"\d{4}[-/]\d{2}[-/]\d{2}.*?:",  # date + sender
        r"^\[.*?\]",                       # [timestamp]
        r"^.{1,40}:\s",                    # "Name: message"
        # WeChat PC format: timestamp + 2+ spaces + name
        r"\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\s{2,}.+",
    ]
    for pat in chat_patterns:
        if re.search(pat, sample, re.MULTILINE):
            return True
    return False


import re  # noqa: E402  (used in _strip_html fallback)


def main():
    parser = argparse.ArgumentParser(
        description="Preprocess mentor source materials into analyzer-ready markdown."
    )
    parser.add_argument("--dir", required=True, help="Directory containing source materials")
    parser.add_argument(
        "--type",
        choices=["papers", "emails", "chats", "lectures", "web", "auto"],
        default="auto",
        help="Material type (default: auto-detect)",
    )
    parser.add_argument("--output", default=None, help="Output file path (default: stdout)")
    parser.add_argument("--mentor-name", default="", help="Mentor's name for chat filtering")
    parser.add_argument("--min-cjk", type=int, default=300, help="Min CJK chars per segment (default: 300)")

    args = parser.parse_args()

    if not os.path.isdir(args.dir):
        print(f"Error: '{args.dir}' is not a directory", file=sys.stderr)
        sys.exit(1)

    if args.type == "papers":
        result = process_papers(args.dir, min_cjk=args.min_cjk)
    elif args.type == "emails":
        result = process_emails(args.dir)
    elif args.type == "chats":
        result = process_chats(args.dir, mentor_name=args.mentor_name)
    elif args.type == "lectures":
        result = process_lectures(args.dir)
    elif args.type == "web":
        result = process_web_articles(args.dir)
    else:
        result = auto_detect(args.dir, mentor_name=args.mentor_name)

    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
        print(f"Written to: {args.output}", file=sys.stderr)
        print(f"Size: {len(result):,} chars", file=sys.stderr)
    else:
        sys.stdout.buffer.write(result.encode("utf-8", errors="replace"))


if __name__ == "__main__":
    main()
