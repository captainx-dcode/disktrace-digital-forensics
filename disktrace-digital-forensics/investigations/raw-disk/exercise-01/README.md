# Raw Disk Forensics – Exercise 1

**Investigation:** 003 – Raw Disk Image Examination
**Exercise:** 01
**Status:** In Progress
**Evidence image:** `corrupted_drive.dd`

## 1. Investigation Overview

This investigation examines a supplied raw disk image to identify recognizable file structures, investigate potentially recoverable data, and evaluate file-carving techniques.

The examination uses filesystem analysis, file-signature identification, hexadecimal inspection, and file-carving tools. Recovered data will be assessed carefully to distinguish between signature detection, extraction, and successful file validation.

## 2. Investigation Objectives

- Establish the characteristics and structure of the supplied raw disk image.
- Examine recognizable filesystem and file signatures.
- Identify potentially recoverable files.
- Apply file-carving techniques using forensic tools and Python.
- Validate extracted files using file identification, metadata inspection, and cryptographic hashes.
- Document findings, limitations, and recovery outcomes.

## 3. Environment Preparation

### 3.1 Environment Details

The investigation environment was accessed through a containerized forensic lab.

| Item              | Observed result                    |
| ----------------- | ---------------------------------- |
| OS release        | Ubuntu 24.04.4 LTS                 |
| Kernel            | Kali Linux kernel 7.1.5+kali-amd64 |
| Architecture      | x86_64                             |
| Python            | 3.12.3                             |
| Current user      | root                               |
| Working directory | `/home/student/Forensics`        |

**Environment note:** Although the OS release information identifies Ubuntu 24.04.4, the running kernel identifies itself as a Kali kernel. The investigation is being conducted in a containerized environment, and the shell is running as `root`.

### 3.2 Tool Availability Verification

The following tools were checked before beginning the investigation.

| Tool      | Availability | Path                   |
| --------- | ------------ | ---------------------- |
| Foremost  | Available    | `/usr/bin/foremost`  |
| Binwalk   | Available    | `/usr/bin/binwalk`   |
| xxd       | Available    | `/usr/bin/xxd`       |
| file      | Available    | `/usr/bin/file`      |
| fdisk     | Available    | `/usr/sbin/fdisk`    |
| fls       | Available    | `/usr/bin/fls`       |
| fsstat    | Available    | `/usr/bin/fsstat`    |
| mmls      | Available    | `/usr/bin/mmls`      |
| istat     | Available    | `/usr/bin/istat`     |
| icat      | Available    | `/usr/bin/icat`      |
| sha256sum | Available    | `/usr/bin/sha256sum` |
| md5sum    | Available    | `/usr/bin/md5sum`    |
| stat      | Available    | `/usr/bin/stat`      |

### 3.3 Version Checks

| Tool     | Verification result                                                |
| -------- | ------------------------------------------------------------------ |
| Foremost | Version 1.5.7                                                      |
| Binwalk  | Executable present; version not reported by the attempted commands |
| xxd      | Version information reported: 2023-10-25                           |
| Python   | 3.12.3                                                             |

**Note:** The attempted Binwalk version commands did not return version information. The executable was nevertheless confirmed to be installed and available at `/usr/bin/binwalk`.

### 3.4 Environment Readiness

All tools included in the availability check were found. No installation was required during this verification stage.

The environment is ready to proceed with the preliminary examination of the evidence image.

## 4. Investigation Stages

1. Environment preparation
2. Evidence identification and preliminary examination
3. Filesystem and raw-data examination
4. File-signature analysis
5. File recovery and carving
6. Recovery validation
7. Findings and conclusion

## 5. Evidence Inventory

Evidence details will be recorded after preliminary examination.

## 6. Findings

Findings will be added as the investigation progresses.

## 7. Screenshots

Screenshots documenting the examination stages will be added as the investigation progresses.

No screenshot is required for the environment preparation stage.

## 8. Limitations

Technical limitations, tool behaviour, and any uncertainties affecting the examination will be documented.

## 9. Conclusion

The conclusion will be completed after the examination and validation stages.
