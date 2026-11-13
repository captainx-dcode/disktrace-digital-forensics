# Requirements Baseline

**Status:** Draft — to be reviewed in Phase 2.

## Functional requirements

| ID | Requirement | Acceptance evidence | Priority |
|---|---|---|---|
| FR-01 | Register each evidence image with a unique evidence ID | Evidence register contains required metadata | Must |
| FR-02 | Calculate SHA-256 for each source image | Hash manifest is generated and repeatable | Must |
| FR-03 | Identify partition layout where present | `mmls` output and interpretation are recorded | Must |
| FR-04 | Identify file-system properties | `fsstat` output and limitations are recorded | Must |
| FR-05 | Examine NTFS metadata and MFT records | Relevant metadata observations are documented | Must |
| FR-06 | Examine FAT32 structures | FAT32 metadata and cluster allocation observations are documented | Must |
| FR-07 | Record deleted-file recovery attempts | Each attempt has method, tool, output, and status | Must |
| FR-08 | Validate recovered artifacts | Type, size, readability, and SHA-256 are recorded | Must |
| FR-09 | Record investigation activities in structured form | Events validate against schema and can be parsed | Must |
| FR-10 | Record findings with evidence references | Each finding points to one or more evidence items | Must |
| FR-11 | Generate report inputs from structured records | Case data can populate report sections | Should |
| FR-12 | Produce a sanitized demonstration | Public demo contains no sensitive evidence | Should |

## Non-functional requirements

- **Integrity:** original evidence is preserved and hashes are recorded.
- **Traceability:** every action and finding can be linked to a case and evidence item.
- **Repeatability:** procedures record commands, tool versions, and relevant parameters.
- **Clarity:** logs use controlled status values and timestamps in UTC.
- **Safety:** sensitive artifacts are excluded from public version control.
- **Auditability:** event records are append-only in normal operation and hash-linked.
- **Human oversight:** automated output is treated as an aid, not an examiner's conclusion.

## Requirement change control

New requirements must include a reason, impact, priority, and acceptance criterion. A feature is not accepted merely because it is technically possible.
