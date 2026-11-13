#!/usr/bin/env python3
"""Append a hash-linked JSONL investigation event."""
import argparse
import hashlib
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

def canonical_bytes(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--operator", required=True)
    parser.add_argument("--event-type", required=True,
        choices=["case","evidence","acquisition","hashing","partition_analysis","filesystem_analysis",
                 "metadata_analysis","recovery","validation","reporting","quality_review","other"])
    parser.add_argument("--action", required=True)
    parser.add_argument("--status", required=True,
        choices=["planned","started","completed","failed","partial","not_validated","blocked"])
    parser.add_argument("--evidence-id")
    parser.add_argument("--tool")
    parser.add_argument("--tool-version")
    parser.add_argument("--command")
    parser.add_argument("--input-reference")
    parser.add_argument("--output-reference")
    parser.add_argument("--notes")
    parser.add_argument("--log", default="activity.jsonl")
    args = parser.parse_args()

    log_path = Path(args.log)
    previous_hash = None
    if log_path.exists() and log_path.stat().st_size:
        last_line = log_path.read_text(encoding="utf-8").splitlines()[-1]
        previous_hash = json.loads(last_line)["event_hash"]

    event = {
        "event_id": str(uuid.uuid4()),
        "case_id": args.case_id,
        "evidence_id": args.evidence_id,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "operator": args.operator,
        "event_type": args.event_type,
        "action": args.action,
        "tool": args.tool,
        "tool_version": args.tool_version,
        "command": args.command,
        "input_reference": args.input_reference,
        "output_reference": args.output_reference,
        "status": args.status,
        "notes": args.notes,
        "previous_event_hash": previous_hash
    }
    event["event_hash"] = hashlib.sha256(canonical_bytes(event)).hexdigest()

    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(event, ensure_ascii=False) + "\n")
    print(f'Appended event {event["event_id"]}')
    print(f'Event hash: {event["event_hash"]}')

if __name__ == "__main__":
    main()
