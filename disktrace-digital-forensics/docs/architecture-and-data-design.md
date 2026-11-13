# Architecture and Data Design

## Logical workflow

```text
Case registration
      |
      v
Evidence registration ----> SHA-256 evidence manifest
      |
      v
Disk / partition identification
      |
      v
File-system examination (NTFS / FAT32 / other)
      |
      v
Deleted-entry analysis / carving
      |
      v
Recovery validation
      |
      v
Findings and examiner review
      |
      v
Investigation report
```

Every meaningful step should create a structured activity event. The event log is an input to later automation, not a substitute for examiner notes or original tool output.

## Core records

- **Case:** investigation identity, purpose, scope, dates, status.
- **Evidence:** unique exhibit ID, source filename, size, SHA-256, source/provenance notes, working-copy relationship.
- **Activity event:** timestamp, operator, action, tool, version, command, input/output references, status, notes, hash-chain fields.
- **Finding:** statement, classification, supporting evidence references, confidence/limitations, examiner.
- **Recovery record:** source evidence, recovery method, output artifact, validation status, hash, limitations.

## Event logging design

The primary event log is JSON Lines (`.jsonl`): one JSON object per line. This is convenient for Python automation and preserves individual event records.

Required principles:
- Use ISO 8601 UTC timestamps.
- Use stable case and evidence IDs.
- Store paths relative to the case directory where possible.
- Record exact commands as executed, but do not store passwords, tokens, or other secrets.
- Keep raw tool output separately and reference its path.
- Use controlled values for event type and status.
- Link each event to the previous event hash to make later modification detectable.

The hash chain is tamper-evident, not tamper-proof. It does not replace access controls, backups, signed records, or secure evidence storage.

## Automation opportunities

1. Verify evidence hashes against the evidence register.
2. Validate event records against the JSON schema.
3. Detect missing required fields or inconsistent IDs.
4. Summarize activity counts and failed/partial operations.
5. Build a findings/evidence cross-reference.
6. Populate report tables from structured records.

Automation must not infer intent, declare legal conclusions, or convert an unverified recovery attempt into a confirmed recovery.
