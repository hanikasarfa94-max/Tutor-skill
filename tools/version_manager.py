"""
version_manager.py

Manages versioning for mentor skill files.
Supports snapshot, rollback, and version listing.
"""

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


MENTORS_DIR = Path(__file__).parent.parent / "mentors" / "generated"
ARCHIVES_DIR = Path(__file__).parent.parent / "mentors" / "archives"


def snapshot(slug: str, note: str = "") -> str:
    """
    Archive the current state of a mentor as a new version snapshot.
    Returns the version string of the snapshot.
    """
    mentor_dir = MENTORS_DIR / slug
    if not mentor_dir.exists():
        raise FileNotFoundError(f"Mentor '{slug}' not found")

    meta_path = mentor_dir / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    version = meta.get("version", "1.0.0")

    archive_dir = ARCHIVES_DIR / slug / version
    archive_dir.mkdir(parents=True, exist_ok=True)

    for filename in ["method.md", "persona.md", "memory.md", "meta.json"]:
        src = mentor_dir / filename
        if src.exists():
            shutil.copy2(src, archive_dir / filename)

    archive_meta = {
        "archived_version": version,
        "archived_at": _now(),
        "note": note,
    }
    (archive_dir / "archive_meta.json").write_text(
        json.dumps(archive_meta, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    return version


def bump_patch(slug: str) -> str:
    """Increment patch version (1.0.0 → 1.0.1). Returns new version string."""
    return _bump(slug, "patch")


def bump_minor(slug: str) -> str:
    """Increment minor version (1.0.0 → 1.1.0). Returns new version string."""
    return _bump(slug, "minor")


def bump_major(slug: str) -> str:
    """Increment major version (1.0.0 → 2.0.0). Returns new version string."""
    return _bump(slug, "major")


def rollback(slug: str, version: str):
    """
    Restore a mentor to a previously archived version.
    The current state is snapshotted before rollback.
    """
    mentor_dir = MENTORS_DIR / slug
    archive_dir = ARCHIVES_DIR / slug / version

    if not archive_dir.exists():
        available = list_versions(slug)
        raise FileNotFoundError(
            f"Version '{version}' not found for '{slug}'. "
            f"Available versions: {available}"
        )

    # Snapshot current state before overwriting
    try:
        current_meta = json.loads((mentor_dir / "meta.json").read_text(encoding="utf-8"))
        current_version = current_meta.get("version", "unknown")
        snapshot(slug, note=f"Pre-rollback snapshot (rolling back to {version})")
    except Exception:
        pass

    # Restore archived files
    for filename in ["method.md", "persona.md", "memory.md", "meta.json"]:
        archived = archive_dir / filename
        if archived.exists():
            shutil.copy2(archived, mentor_dir / filename)

    # Update meta to reflect rollback
    meta_path = mentor_dir / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta["last_updated"] = _now()
    meta.setdefault("correction_log", []).append(
        {
            "date": _now(),
            "type": "rollback",
            "change": f"Rolled back from {current_version} to {version}",
            "reason": "user-initiated rollback",
        }
    )
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")


def list_versions(slug: str) -> list[dict]:
    """
    List all archived versions for a mentor, most recent first.
    """
    slug_archive = ARCHIVES_DIR / slug
    if not slug_archive.exists():
        return []

    versions = []
    for version_dir in slug_archive.iterdir():
        if not version_dir.is_dir():
            continue
        archive_meta_path = version_dir / "archive_meta.json"
        if archive_meta_path.exists():
            archive_meta = json.loads(archive_meta_path.read_text(encoding="utf-8"))
            versions.append(
                {
                    "version": version_dir.name,
                    "archived_at": archive_meta.get("archived_at", "?"),
                    "note": archive_meta.get("note", ""),
                }
            )

    return sorted(versions, key=lambda v: v["archived_at"], reverse=True)


def _bump(slug: str, level: str) -> str:
    mentor_dir = MENTORS_DIR / slug
    meta_path = mentor_dir / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))

    version = meta.get("version", "1.0.0")
    parts = [int(x) for x in version.split(".")]
    while len(parts) < 3:
        parts.append(0)

    if level == "major":
        parts = [parts[0] + 1, 0, 0]
    elif level == "minor":
        parts = [parts[0], parts[1] + 1, 0]
    else:
        parts = [parts[0], parts[1], parts[2] + 1]

    new_version = ".".join(str(p) for p in parts)
    meta["version"] = new_version
    meta["last_updated"] = _now()
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    return new_version


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
