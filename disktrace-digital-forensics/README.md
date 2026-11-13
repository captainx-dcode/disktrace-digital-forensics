# DiskTrace — Digital Forensics & Data Recovery Laboratory

**Status:** Phase 1 — Initiation and Planning  
**Project type:** Independent cybersecurity / digital-forensics portfolio project  
**Repository:** `disktrace-digital-forensics`

## Purpose

DiskTrace is a structured digital-forensics laboratory for practicing and documenting the examination of disk images. It covers evidence preservation, disk and partition structures, NTFS and FAT32 analysis, deleted-file recovery, file carving, integrity validation, investigation logging, and professional reporting.

The project also develops a small automation layer that consumes structured investigation records and produces repeatable evidence manifests and report inputs.

> **Important:** This is an educational lab. Use only disk images you own or are explicitly authorized to examine. Do not publish original evidence images, personal data, recovered confidential files, credentials, or other sensitive material.

## Project goals

1. Preserve and identify forensic evidence using repeatable procedures.
2. Examine raw disk images and identify partition and file-system structures.
3. Analyze NTFS structures, including the Master File Table (MFT).
4. Analyze FAT32 structures, including FAT tables and cluster chains.
5. Recover deleted files using file-system metadata where possible and file carving where appropriate.
6. Validate recovered artifacts and document recovery limitations.
7. Maintain structured, machine-readable investigation logs.
8. Generate clear, evidence-based investigation reports.

## Important terminology

- **NTFS** and **FAT32** are file systems.
- The **MFT (Master File Table)** is a central NTFS metadata structure; it is not a separate file system.
- A **RAW `.dd` image** is a byte-for-byte disk-image representation. It is not itself a file system. It may contain a partition table and an NTFS/FAT32 volume, or a file system beginning directly at the start of the image.

## SDLC approach

| Phase | Focus | Exit evidence |
|---|---|---|
| 1. Initiation and planning | Problem, objectives, scope, risks | Approved project charter |
| 2. Requirements analysis | Functional and quality requirements | Requirements baseline |
| 3. Design | Architecture, evidence model, log schemas, report structure | Design review |
| 4. Implementation | Examination workflows and Python utilities | Version-controlled implementation |
| 5. Testing and validation | Test cases, repeatability, integrity checks | Test results |
| 6. Investigation and reporting | Case execution, findings, conclusions | Reviewed case report |
| 7. Deployment and documentation | Repository release and demonstrations | Public portfolio release |
| 8. Evaluation and maintenance | Lessons, limitations, improvements | Retrospective and backlog |

A phase is not considered complete merely because commands ran. Its exit criteria must be met and documented.

## Repository map

```text
disktrace-digital-forensics/
├── README.md
├── LICENSE
├── .gitignore
├── docs/
│   ├── project-charter.md
│   ├── sdlc-roadmap.md
│   ├── requirements.md
│   ├── architecture-and-data-design.md
│   ├── evidence-handling-procedure.md
│   ├── forensic-methodology.md
│   └── reporting-standard.md
├── schemas/
│   ├── investigation-event.schema.json
│   └── finding.schema.json
├── templates/
│   ├── case-intake.md
│   ├── investigation-report.md
│   ├── evidence-register.csv
│   ├── activity-log.csv
│   ├── findings-register.csv
│   └── recovery-register.csv
├── cases/
│   └── DFL-2026-001/
│       ├── case.json
│       ├── README.md
│       ├── logs/
│       ├── analysis/
│       ├── findings/
│       ├── reports/
│       └── screenshots/
├── scripts/
│   ├── hash_evidence.py
│   ├── log_event.py
│   └── validate_recovery.py
├── tests/
│   └── README.md
└── media/
    └── demonstration-plan.md
```

## Initial case

`DFL-2026-001` is a **training scenario** concerning suspected deletion of work-related documents. The scenario is fictional; actual evidence contents and findings must come from examination, not assumptions.

Candidate lab images previously identified:
- `forensic_image.dd`
- `fat32_forensic.dd`
- `corrupted_drive.dd`
- `M2_lab.dd`

These are candidates only. Their file-system types, contents, and suitability must be verified before assigning them to a case exhibit.

## Working principles

- Preserve originals; examine verified working copies.
- Record SHA-256 hashes and relevant acquisition details.
- Record commands, tool versions, timestamps, outputs, and operator observations.
- Separate confirmed observations from interpretations and hypotheses.
- Do not describe a file as successfully recovered until it has been validated.
- Record unsuccessful attempts and limitations as well as successful results.
- Never invent timestamps, file contents, evidence provenance, or findings.

## Getting started

See [`docs/sdlc-roadmap.md`](docs/sdlc-roadmap.md). We will work phase by phase and review each phase before proceeding.
