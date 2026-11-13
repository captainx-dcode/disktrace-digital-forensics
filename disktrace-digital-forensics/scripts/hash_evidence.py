#!/usr/bin/env python3
"""Calculate SHA-256 hashes for evidence files without modifying them."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", help="Evidence files to hash")
    parser.add_argument("--output", default="evidence-hashes.json", help="Manifest output path")
    args = parser.parse_args()

    records = []
    for name in args.files:
        path = Path(name)
        if not path.is_file():
            raise SystemExit(f"Not a regular file: {path}")
        stat = path.stat()
        records.append({
            "filename": path.name,
            "path": str(path.resolve()),
            "size_bytes": stat.st_size,
            "sha256": sha256_file(path),
            "hashed_at_utc": datetime.now(timezone.utc).isoformat()
        })

    output = Path(args.output)
    output.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(records)} record(s) to {output}")
    for record in records:
        print(f'{record["sha256"]}  {record["filename"]}')

if __name__ == "__main__":
    main()
