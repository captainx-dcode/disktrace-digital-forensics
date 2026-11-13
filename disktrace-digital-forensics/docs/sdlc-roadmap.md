# SDLC Roadmap and Phase Gates

DiskTrace follows a lightweight, evidence-driven SDLC. Each phase produces artifacts and has explicit exit criteria.

## Phase 1 — Initiation and planning

**Activities**
- Define the problem, objectives, intended audience, boundaries, and risks.
- Select the initial training case and candidate images.
- Establish project naming, repository structure, and working principles.

**Deliverables**
- Project charter.
- SDLC roadmap.
- Initial risk register.

**Exit gate**
- Scope and exclusions are understood.
- Candidate evidence is clearly labelled as unverified.
- Evidence safety rules are agreed.

## Phase 2 — Requirements analysis

**Activities**
- Define functional requirements for image identification, examination, recovery, validation, logging, and reporting.
- Define quality requirements: integrity, traceability, repeatability, usability, and safe handling.
- Prioritize requirements and define acceptance criteria.

**Deliverables**
- Requirements baseline.
- Use cases and acceptance criteria.
- Traceability matrix.

**Exit gate**
- Every planned capability has a testable acceptance criterion.
- No unsupported capability is presented as completed.

## Phase 3 — System and data design

**Activities**
- Design the investigation workflow and repository layout.
- Define case, evidence, activity-event, finding, and recovery records.
- Define log integrity and report generation approach.
- Decide which steps require human review.

**Deliverables**
- Architecture and data-design document.
- JSON schemas and CSV templates.
- Report template.

**Exit gate**
- Required fields and relationships are defined.
- Logs can be consumed by scripts without ambiguous field meanings.
- Human approval points are clear.

## Phase 4 — Implementation

**Activities**
- Implement evidence hashing.
- Implement structured event logging.
- Implement recovered-file validation.
- Execute documented NTFS, FAT32, and raw-image workflows.

**Deliverables**
- Python scripts.
- Examination notes and tool outputs.
- Version-controlled code.

**Exit gate**
- Scripts pass their tests on controlled sample inputs.
- Commands and tool versions are recorded.
- No original evidence is overwritten.

## Phase 5 — Testing and validation

**Activities**
- Test hash consistency.
- Test event-log integrity and schema validity.
- Test validation against valid, mismatched, unreadable, and partial files.
- Repeat selected examination steps to assess reproducibility.

**Deliverables**
- Test plan and test results.
- Defect/limitation log.
- Verification records.

**Exit gate**
- Critical checks pass or unresolved failures are documented.
- Test evidence supports each claimed result.

## Phase 6 — Investigation and reporting

**Activities**
- Execute the case scope.
- Maintain evidence and activity registers.
- Create findings with evidence references.
- Draft, review, and finalize the report.

**Deliverables**
- Case file.
- Findings register.
- Recovery register.
- Investigation report.

**Exit gate**
- Every finding is traceable to evidence.
- Confirmed facts are separated from interpretations.
- Limitations and alternative explanations are documented.

## Phase 7 — Deployment and documentation

**Activities**
- Sanitize screenshots and demonstrations.
- Review repository for sensitive data.
- Publish README, procedures, reports, and demo recordings.

**Deliverables**
- Public Git repository.
- Demonstration videos.
- Release notes.

**Exit gate**
- No original images, recovered private files, credentials, or personal data are committed.
- Setup and reproduction instructions are tested.

## Phase 8 — Evaluation and maintenance

**Activities**
- Review what worked and what did not.
- Identify methodological gaps.
- Prioritize future improvements.

**Deliverables**
- Retrospective.
- Improvement backlog.
- Versioned project update.

**Exit gate**
- Lessons and future work are recorded honestly.
