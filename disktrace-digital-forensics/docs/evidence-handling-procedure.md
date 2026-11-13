# Evidence Handling Procedure

## 1. Before examination

- Confirm authority and scope for the training image.
- Assign a case ID and evidence ID.
- Record source filename, file size, acquisition/source information if known, date received, and handler.
- Do not assume that a filename establishes the image's contents or provenance.

## 2. Preserve and identify

- Keep the original image unchanged.
- Calculate SHA-256 for the original.
- Create a working copy where practical.
- Calculate SHA-256 for the working copy and compare it with the original.
- Record any mismatch and stop examination until resolved.

## 3. Examine

- Record tool name and version.
- Record exact command, parameters, timestamp, operator, and output location.
- Record partition offsets and explain their units.
- Do not mount an original evidence image read-write.
- Preserve tool output and relevant screenshots in the case directory.

## 4. Recover

- Record the source evidence ID and recovery method.
- Preserve recovery output separately from source evidence.
- Record whether recovery was complete, partial, failed, or not validated.
- Do not infer original filename or directory location from carved content unless supported by metadata.

## 5. Validate

Where applicable, record:
- File signature / detected type.
- File size.
- Whether the file opens or can be parsed.
- SHA-256 of recovered output.
- Comparison with a known original hash, if a legitimate known original exists.
- Corruption, truncation, or other limitations.

## 6. Close-out

- Ensure every finding references supporting evidence.
- Reconcile evidence and recovery registers.
- Record unresolved issues.
- Sanitize public copies before publication.
