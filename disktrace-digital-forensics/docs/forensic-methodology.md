# Forensic Methodology

## Examination sequence

1. Confirm case authority, scope, and evidence identity.
2. Hash and preserve source images.
3. Determine whether the image contains a partition table.
4. Identify partition start sectors and relevant offsets.
5. Identify the file system and record its properties.
6. Examine allocated and unallocated structures.
7. Examine metadata and deleted entries.
8. Apply recovery methods appropriate to the observed file system and evidence.
9. Validate outputs and document limitations.
10. Correlate observations into findings and report.

## Tool selection

| Task | Candidate tools | Notes |
|---|---|---|
| Image identity | `file`, `sha256sum`, Python | A file extension is not proof of format |
| Partition layout | `mmls` | Some images may not contain a partition table |
| File-system metadata | `fsstat` | May require a volume offset |
| File listing / deleted entries | `fls` | Record offset and flags |
| Metadata inspection | `istat`, `icat` | Applicable metadata address must be established |
| Unallocated-space extraction | `blkls` | Document block/sector interpretation |
| File carving | PhotoRec, controlled Python carver | Carving may lose filenames and directory context |
| GUI examination | Autopsy | Record version and ingest settings |

## Offset discipline

Do not guess an offset. First inspect the image layout. If a partition begins at sector `N`, calculate the byte offset using the sector size established from the image or tool output:

`byte_offset = start_sector × sector_size`

Record both the start sector and the calculated byte offset. Tool options may expect sector units rather than byte units; confirm the relevant tool's syntax before use.

## Interpretation discipline

- A deleted directory entry does not prove who deleted the file.
- A timestamp does not independently prove a person's action or intent.
- A carved file may be incomplete and may lack original path/name metadata.
- A matching SHA-256 confirms byte identity between compared files; it does not independently establish provenance or authorship.
