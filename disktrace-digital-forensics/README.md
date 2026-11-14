
# DiskTrace – Digital Forensics & Data Recovery Laboratory

DiskTrace is a practical digital forensics learning and portfolio project. It documents structured investigations of disk images, file-system metadata, deleted-file recovery, raw data examination, and selected forensic automation.

The investigations will be completed in this order:

1. **NTFS Forensics** – examine the supplied NTFS image and document each task as it is performed.
2. **FAT32 Forensics** – examine the supplied FAT32 image and compare its structures and recovery process with NTFS.
3. **Raw Disk Forensics** – investigate raw data and file carving techniques that do not depend primarily on file-system metadata.

> **Progress rule:** This repository is a working record, not a claim that all investigations are complete. Only procedures actually performed and outputs actually observed should be marked complete. Screenshots should be captured during each task and added before committing that task.

## Project objectives

- Identify disk-image and file-system formats.
- Examine file-system structures and metadata.
- Locate deleted, orphaned, and potentially recoverable file entries.
- Explore recovery using established forensic utilities.
- Develop Python utilities for selected forensic tasks.
- Record hashes and validate extraction results appropriately.
- Maintain clear evidence handling, reproducibility, and investigative reporting.

## Investigation roadmap

| Investigation                                | Evidence image        | Status                                                               |
| -------------------------------------------- | --------------------- | -------------------------------------------------------------------- |
| [NTFS](investigations/ntfs/README.md)         | `forensic_image.dd` | Task 1: environment preparation documented; subsequent tasks pending |
| [FAT32](investigations/fat32/README.md)       | `fat32_forensic.dd` | Not started                                                          |
| [Raw disk](investigations/raw-disk/README.md) | To be confirmed       | Not started                                                          |

## Repository layout

```text
documentation/       Shared methodology and evidence-handling guidance
investigations/      Separate investigation workspaces
  ntfs/              NTFS tasks, notes, screenshots, and scripts
  fat32/             FAT32 tasks, notes, screenshots, and scripts
  raw-disk/          Raw disk examination and carving
reports/             Final investigation reports
media/               Shared diagrams and supporting media
```

Each investigation has its own README. Its README is updated as work progresses; planned work must remain labelled as planned.

## Working methodology

Each task should follow this sequence:

1. Read the task and identify its objective.
2. Execute the commands in the lab.
3. Inspect and understand the actual output.
4. Capture screenshots showing the relevant terminal output.
5. Record observations, findings, and limitations.
6. Update the investigation documentation.
7. Commit the completed task and its supporting screenshots.

Do not skip ahead or document results that have not yet been observed.

## Evidence handling

- Preserve original disk images and do not perform analysis that modifies them.
- Store extracted or recovered files separately from source evidence.
- Record the commands, offsets, sizes, and hashes used during recovery.
- Treat a matching hash between two outputs as evidence that those outputs are byte-identical; it does not by itself prove authenticity against an original pre-deletion file.
- Distinguish confirmed observations from assumptions, inferences, attempted actions, and unverified results.
- Do not upload original `.dd` images or potentially sensitive recovered files to this public repository.

## Laboratory environment note

The first NTFS environment-preparation task was carried out using a Kali Linux host and an Ubuntu-based Docker container (`machokadee/forensics-lab:latest`). It was not performed inside VirtualBox. This distinction is recorded to keep the project documentation faithful to the environment actually used. If a later task explicitly requires VirtualBox, follow that requirement or document an approved alternative.

## Tools

Tools will be listed in the relevant investigation README as they are actually used. The initial NTFS environment confirmed The Sleuth Kit version 4.12.1.

## Disclaimer

DiskTrace is an educational and portfolio project using supplied or simulated forensic images in a controlled laboratory. The project does not claim that recovered files are necessarily complete, authentic, or legally admissible. Conclusions are limited to the evidence and methods documented in each investigation.

## Author

**Eugen Nyongesa**
GitHub: [captainx-dcode](https://github.com/captainx-dcode)
