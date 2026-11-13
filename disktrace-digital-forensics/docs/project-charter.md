# Project Charter

## Project identity

- **Name:** DiskTrace — Digital Forensics & Data Recovery Laboratory
- **Project ID:** DTRACE
- **Version:** 0.1.0
- **Current phase:** Phase 1 — Initiation and Planning
- **Owner:** Project author

## Problem statement

Digital forensic examination requires more than running recovery tools. An investigator must preserve evidence, understand the storage structures being examined, apply suitable methods, validate recovered artifacts, maintain an auditable record of actions, and communicate findings and limitations clearly.

DiskTrace provides a repeatable practical environment to develop and demonstrate those capabilities.

## Objectives

1. Identify disk-image and partition structures.
2. Explain and examine NTFS, including the MFT.
3. Explain and examine FAT32, including allocation tables and cluster chains.
4. Examine unallocated space and apply file carving when justified.
5. Recover selected deleted artifacts from authorized training images.
6. verify recovered-file type, readability, and cryptographic hash.
7. Maintain structured case, evidence, activity, finding, and recovery records.
8. Produce a professional report that distinguishes evidence from interpretation.

## In scope

- Raw `.dd` disk images and partition analysis.
- NTFS and FAT32 examination.
- Metadata-based deleted-file analysis.
- File carving and recovery validation.
- SHA-256 hashing and evidence manifests.
- Python utilities for repeatable logging and validation.
- Investigation documentation and report generation.

## Out of scope for the initial release

- Live acquisition from third-party systems.
- Mobile-device, cloud-account, memory, and network forensics.
- Attribution of an individual to an action based solely on a filename or timestamp.
- Claims of legal admissibility or certification.
- Automated conclusions about intent or guilt.

## Stakeholders and intended audience

- Project author / examiner.
- Technical reviewers and cybersecurity hiring teams.
- Readers evaluating the methodology and reproducibility of the portfolio.

## Success criteria

- Each selected image has documented identity, size, hash, and examination status.
- File-system identification is supported by tool output and recorded offsets where applicable.
- NTFS and FAT32 concepts are demonstrated with actual observations.
- Recovery attempts and outcomes are recorded, including failures and partial recovery.
- Recovered artifacts are validated and their hashes recorded.
- Reports include scope, methods, evidence references, findings, limitations, and conclusion.
- Public materials contain no sensitive evidence or personal data.

## Key risks

| Risk | Treatment |
|---|---|
| Original image modified | Keep originals read-only where practical; analyze verified copies |
| Incorrect partition offset | Record `mmls` output and document offset calculations |
| False recovery claim | Validate file signature, readability, size, and hash |
| Timestamp misinterpretation | Record source, timezone, filesystem semantics, and uncertainty |
| Sensitive data published | Keep evidence/recovery directories out of Git |
| Tool output not reproducible | Record tool versions, exact commands, and environment |
| Automated log altered | Use append-only workflow and hash-linked event records |

## Assumptions requiring validation

- The supplied lab images are authorized for this educational examination.
- The container has or can install the required tools.
- Image formats and partition layouts are not known until examined.
