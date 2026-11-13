#!/usr/bin/env python3
"""Create a basic validation manifest for recovered files."""
import argparse
import hashlib
import json
import mimetypes
from datetime import datetime, timezone
from pathlib import Path

def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("files", nargs="+")
    p.add_argument("--output", default="recovery-validation.json")
    args = p.parse_args()

    rows = []
    for name in args.files:
        path = Path(name)
        if not path.is_file():
            rows.append({"path": name, "validation_status": "failed", "reason": "not a regular file"})
            continue
        size = path.stat().st_size
        rows.append({
            "filename": path.name,
            "path": str(path.resolve()),
            "size_bytes": size,
            "mime_guess": mimetypes.guess_type(path.name)[0],
            "sha256": digest(path),
            "non_empty": size > 0,
            "validated_at_utc": datetime.now(timezone.utc).isoformat(),
            "validation_status": "basic_checks_only",
            "limitations": "MIME guess and non-empty check do not prove file completeness, authenticity, or successful opening."
        })
    Path(args.output).write_text(json.dumps(rows, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote validation manifest to {args.output}")

if __name__ == "__main__":
    main()
