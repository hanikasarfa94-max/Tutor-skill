"""
skill_writer.py

Writes generated mentor skill files to disk.
Handles creating the mentor directory, writing the three core files
(method.md, persona.md, memory.md), and updating meta.json.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path


MENTORS_DIR = Path(__file__).parent.parent / "mentors" / "generated"
ARCHIVES_DIR = Path(__file__).parent.parent / "mentors" / "archives"


def _ensure_dirs():
    MENTORS_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVES_DIR.mkdir(parents=True, exist_ok=True)


def mentor_path(slug: str) -> Path:
    return MENTORS_DIR / slug


def write_mentor(
    slug: str,
    method_md: str,
    persona_md: str,
    memory_md: str,
    meta: dict,
) -> Path:
    """
    Write all three mentor files and meta.json for a new mentor.
    Returns the mentor directory path.
    """
    _ensure_dirs()
    mentor_dir = mentor_path(slug)
    mentor_dir.mkdir(parents=True, exist_ok=True)

    (mentor_dir / "method.md").write_text(method_md, encoding="utf-8")
    (mentor_dir / "persona.md").write_text(persona_md, encoding="utf-8")
    (mentor_dir / "memory.md").write_text(memory_md, encoding="utf-8")

    meta.setdefault("version", "1.0.0")
    meta.setdefault("created_at", _now())
    meta["last_updated"] = _now()
    meta["correction_log"] = meta.get("correction_log", [])

    (mentor_dir / "meta.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    return mentor_dir


def update_mentor_file(slug: str, filename: str, content: str):
    """
    Overwrite a single file (method.md, persona.md, or memory.md) for an existing mentor.
    Also updates last_updated in meta.json.
    """
    mentor_dir = mentor_path(slug)
    if not mentor_dir.exists():
        raise FileNotFoundError(f"Mentor '{slug}' not found at {mentor_dir}")

    (mentor_dir / filename).write_text(content, encoding="utf-8")
    _touch_meta(mentor_dir)


def update_memory(slug: str, memory_md: str):
    """Convenience wrapper for updating memory.md after a session."""
    update_mentor_file(slug, "memory.md", memory_md)


def read_mentor(slug: str) -> dict:
    """
    Load all files for a mentor into a dict:
    {method, persona, memory, meta}
    """
    mentor_dir = mentor_path(slug)
    if not mentor_dir.exists():
        raise FileNotFoundError(f"Mentor '{slug}' not found at {mentor_dir}")

    return {
        "method": (mentor_dir / "method.md").read_text(encoding="utf-8"),
        "persona": (mentor_dir / "persona.md").read_text(encoding="utf-8"),
        "memory": (mentor_dir / "memory.md").read_text(encoding="utf-8"),
        "meta": json.loads((mentor_dir / "meta.json").read_text(encoding="utf-8")),
    }


def list_mentors() -> list[dict]:
    """
    Return a list of mentor summaries from all generated mentor directories.
    """
    _ensure_dirs()
    mentors = []
    for mentor_dir in sorted(MENTORS_DIR.iterdir()):
        if not mentor_dir.is_dir():
            continue
        meta_path = mentor_dir / "meta.json"
        if not meta_path.exists():
            continue
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        mentors.append(
            {
                "slug": mentor_dir.name,
                "name": meta.get("mentor_name", mentor_dir.name),
                "type": meta.get("mentor_type", "unknown"),
                "version": meta.get("version", "?"),
                "last_updated": meta.get("last_updated", "?"),
            }
        )
    return mentors


def delete_mentor(slug: str):
    """
    Remove a mentor's generated directory.
    Archives it first if archives directory exists.
    """
    mentor_dir = mentor_path(slug)
    if not mentor_dir.exists():
        raise FileNotFoundError(f"Mentor '{slug}' not found")

    import shutil
    archive_target = ARCHIVES_DIR / slug / "deleted"
    archive_target.mkdir(parents=True, exist_ok=True)
    shutil.copytree(mentor_dir, archive_target / _now_slug(), dirs_exist_ok=True)
    shutil.rmtree(mentor_dir)


def log_correction(slug: str, correction: dict):
    """
    Append a correction entry to meta.json's correction_log.
    correction should be a dict with keys: type, layer, dimension, change, reason.
    """
    mentor_dir = mentor_path(slug)
    meta_path = mentor_dir / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))

    correction["date"] = _now()
    correction["version"] = meta.get("version", "1.0.0")
    meta.setdefault("correction_log", []).append(correction)

    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")


def _touch_meta(mentor_dir: Path):
    meta_path = mentor_dir / "meta.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        meta["last_updated"] = _now()
        meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _now_slug() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
