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

## 4. Investigation Stages

1. Environment preparation
2. Evidence identification and preliminary examination
3. Filesystem and raw-data examination
4. File-signature analysis
5. File recovery and carving
6. Recovery validation
7. Findings and conclusion

## 5. Evidence Inventory

The supplied evidence image is named `corrupted_drive.dd`.

The file was located in the forensic working directory:

`/home/student/Forensics`

### 5.1 Evidence File Identification

**Command:**

```bash
file corrupted_drive.dd
```

**Observed output:**

```text
corrupted_drive.dd: data
```

**Observation:**

The `file` utility identified the image as generic data rather than recognizing a specific filesystem or common file format from its initial signature.

**Interpretation:**

This result does not establish that the image contains no filesystem or recoverable files. Further examination using partition analysis, hexadecimal inspection, and file-signature scanning is required.

### 5.2 Disk Geometry and Partition Examination

**Command:**

```bash
fdisk -l corrupted_drive.dd
```

**Observed output:**

```text
Disk corrupted_drive.dd: 50 MiB, 52428800 bytes, 102400 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
```

**Observations:**

- Image size: 50 MiB.
- Total size in bytes: 52,428,800.
- Total sectors: 102,400.
- Sector size: 512 bytes.
- Logical and physical sector sizes: 512 bytes.
- No partition entries were displayed in the command output.

**Interpretation:**

The command established the image's reported size and sector geometry. No partition entries were displayed, so a conventional partition layout was not identified by this examination.

The absence of displayed partition entries does not prove that the image contains no filesystem structures or file data.

### 5.3 Filesystem Listing and Entropy Observation

**Command:**

```bash
fls -r corrupted_drive.dd
```

**Observed output:**

```text
Possible encryption detected (High entropy (8.00))
```

**Observation:**

The filesystem listing attempt returned a high-entropy warning instead of a directory or file listing.

**Interpretation:**

The reported entropy value of 8.00 indicates that the examined data appears highly random according to the tool's heuristic. This can be associated with encrypted or compressed data, but it is not proof of encryption.

The command did not provide a filesystem directory listing. Further raw-data and file-signature analysis is therefore necessary to investigate the image contents.

## 6. Findings

| Reference | Examination           | Finding                                                      |
| --------- | --------------------- | ------------------------------------------------------------ |
| F-01      | File identification   | Image identified as generic data                             |
| F-02      | Disk geometry         | 50 MiB image with 512-byte sectors                           |
| F-03      | Partition examination | No partition entries displayed by `fdisk`                  |
| F-04      | Filesystem listing    | High-entropy warning reported; no directory listing produced |

These are preliminary findings and will be supplemented by subsequent examination stages.

## 7. Screenshots

Screenshots documenting the examination stages will be added as the investigation progresses.

| Screenshot                                  | Description                                                        |
| ------------------------------------------- | ------------------------------------------------------------------ |
| `01-raw-disk-preliminary-examination.png` | File identification, disk geometry, and filesystem listing results |

## 8. Limitations

- The generic `file` identification result does not establish the absence of filesystem structures.
- The `fdisk` output did not display partition entries, but this does not rule out unpartitioned filesystem data or embedded file structures.
- The high-entropy warning is heuristic and cannot independently confirm encryption.
- The filesystem listing attempt did not produce a directory listing.

## 9. Conclusion

The preliminary examination established the basic characteristics of the supplied raw disk image. The image is 50 MiB in size, uses a reported sector size of 512 bytes, and did not display conventional partition entries through the initial `fdisk` examination.

The filesystem listing attempt reported high entropy rather than recognizable file entries. These observations justify proceeding with raw-data and file-signature analysis to identify potentially recoverable content.

The investigation remains in progress.
