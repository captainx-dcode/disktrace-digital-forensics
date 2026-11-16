
# FAT32 Forensics Investigation

**Investigation:** 002 – FAT32 Disk Image Examination
**Status:** In Progress
**Evidence image:** `fat32_forensic.dd`
**Examination environment:** Kali Linux / Docker forensic lab
**Forensic toolkit:** The Sleuth Kit 4.12.1

---

## 1. Investigation Scope

This investigation examines the supplied FAT32 forensic disk image to identify deleted files, examine their associated file-system metadata, recover available file contents, and assess the integrity of recovered evidence.

The examination follows a structured digital forensic workflow. Each stage records the objective, commands, observations, findings, and supporting screenshots.

The investigation focuses on:

- Identification of the FAT32 file system and its structural metadata.
- Examination of directory entries and deleted-file indicators.
- Extraction and interpretation of file metadata.
- Identification of the sectors occupied by deleted files.
- Recovery using The Sleuth Kit and custom Python file-carving utilities.
- Validation of recovered files using file signatures and cryptographic hashes.

The evidence image is treated as a forensic source. Examination activities and generated recovery outputs are documented separately to maintain a clear distinction between source evidence and derived evidence.

## 2. Investigation Log

### Task 1: Forensic Environment Preparation

**Objective:** Establish a controlled environment with the necessary forensic utilities to examine the supplied disk image.

#### 1.1 Lab initialization

The forensic environment was prepared using a Docker container based on `machokadee/forensics-lab:latest`.

```bash
docker pull machokadee/forensics-lab:latest

docker run -it --rm --privileged machokadee/forensics-lab:latest
```

The container was checked using:

```bash
whoami
id
pwd
ls -lh
```

**Environment observations:**

- Host operating system: Kali Linux.
- Container image: `machokadee/forensics-lab:latest`.
- Execution account: `root`.
- Working directory: `/home/student/Forensics`.
- Evidence image available: `fat32_forensic.dd`.
- Additional supplied images included `forensic_image.dd`, `corrupted_drive.dd`, and `M2_lab.dd`.

#### 1.2 Sleuth Kit installation and verification

Package information was updated, and Sleuth Kit was installed or verified:

```bash
apt update
apt install sleuthkit -y
```

The required utilities were checked:

```bash
fls -V
fsstat -V
```

The tools provide the following capabilities:

| Utility    | Forensic purpose                                                 |
| ---------- | ---------------------------------------------------------------- |
| `fls`    | Lists file and directory entries, including deleted entries.     |
| `fsstat` | Examines file-system metadata and structural information.        |
| `istat`  | Displays metadata associated with a specified file-system entry. |
| `icat`   | Extracts file content using a file-system entry identifier.      |

**Observation:** The required Sleuth Kit utilities were available in the forensic environment.

**Evidence:** `screenshots/01-fat32-environment-setup.png`

---

### Task 2: File-System Identification and Structural Examination

**Objective:** Identify the file-system type and establish its structural characteristics before examining individual files.

#### 2.1 File-system identification

The `file` utility was used to inspect the supplied image:

```bash
file fat32_forensic.dd
```

The output identified a DOS/MBR boot-sector image with a FAT32 file system. The OEM identifier was `mkfs.fat`.

The file-system structure was then examined using:

```bash
fsstat fat32_forensic.dd
```

The output confirmed that the file system is FAT32.

#### 2.2 Structural findings

| Property               | Observed value       |
| ---------------------- | -------------------- |
| File-system type       | FAT32                |
| OEM name               | `mkfs.fat`         |
| Volume ID              | `0xa742e8f9`       |
| Volume label           | `NO NAME`          |
| Sector size            | 512 bytes            |
| Cluster size           | 512 bytes            |
| Sectors per cluster    | 1                    |
| Root directory cluster | 2                    |
| Root directory sector  | 1608                 |
| Reserved sectors       | 0–31                |
| FAT 0                  | Sectors 32–819      |
| FAT 1                  | Sectors 820–1607    |
| Data area              | Sectors 1608–102399 |
| Total sector range     | 0–102399            |
| Total cluster range    | 2–100793            |

**Interpretation:**

The image uses 512-byte sectors and 512-byte clusters. Consequently, each cluster contains one sector.

The root directory is associated with cluster 2 and is located at sector 1608. Two File Allocation Tables are present, occupying sectors 32–819 and 820–1607.

The data area begins at sector 1608.

These values establish the file-system layout used during subsequent deleted-file examination.

**Evidence:** `screenshots/02-fat32-filesystem-identification.png`

---

### Task 3: Deleted-File Identification

**Objective:** Identify deleted directory entries that may contain recoverable file metadata and content.

The recursive file listing utility was used:

```bash
fls -r fat32_forensic.dd
```

#### 3.1 Examination output

The relevant output was:

```text
r/r * 4:        IMG_2019.jpg
r/r * 6:        IMG_0117.png
```

The output identified two deleted file entries:

| Directory entry | Filename reported by `fls` | Allocation status       |
| --------------- | ---------------------------- | ----------------------- |
| 4               | `IMG_2019.jpg`             | Deleted / Not allocated |
| 6               | `IMG_0117.png`             | Deleted / Not allocated |

The asterisk (`*`) indicates that the entries are deleted or not allocated.

**Initial finding:** Two deleted image entries were identified in the FAT32 directory listing. Each entry will be examined independently to avoid mixing metadata, recovery results, and validation evidence.

**Evidence:** `screenshots/03-fat32-deleted-file-listing.png`

---

### Task 4: Individual Deleted-File Examination

#### Evidence Item 001 – IMG_2019.jpg

**Objective:** Examine the metadata associated with the first deleted file, establish its storage location, and determine whether its contents can be recovered.

##### 4.1 Metadata extraction

The directory entry identified during the previous task was examined using:

```bash
istat fat32_forensic.dd 4
```

The command returned the following metadata:

| Metadata field             | Observed value          |
| -------------------------- | ----------------------- |
| Directory entry            | 4                       |
| Allocation status          | Not Allocated           |
| File attributes            | File, Archive           |
| Name reported by `istat` | `_MG_2019.JPG`        |
| Size                       | 3,190,011 bytes         |
| Written timestamp          | 2036-01-01 07:59:58 UTC |
| Accessed timestamp         | 2025-03-07 00:00:00 UTC |
| Created timestamp          | 2025-03-07 22:08:29 UTC |
| First sector               | 32990                   |
| Last sector                | 39220                   |

**Filename observation:**

The earlier `fls` output reported the filename as `IMG_2019.jpg`, whereas `istat` reported `_MG_2019.JPG`.

Both names are recorded exactly as returned by the tools. The discrepancy is retained for further examination rather than assuming that one representation is correct.

**Timestamp observation:**

The Written timestamp is `2036-01-01 07:59:58 UTC`, which is later than the Created timestamp.

This is an anomalous timestamp and should be investigated. The available output does not establish why the timestamp has this value, so no conclusion about its cause is made at this stage.

##### 4.2 Storage location analysis

The metadata reports that the file occupies sectors 32990 through 39220.

The image has a sector size of 512 bytes.

The starting byte offset is calculated as:

```text
Starting sector × Sector size

32990 × 512 = 16,890,880 bytes
```

In hexadecimal:

```text
0x101B800
```

The file size reported by `istat` is 3,190,011 bytes.

The logical extraction range is therefore:

```text
Start offset:  16,890,880 bytes
File size:      3,190,011 bytes
End offset:    20,080,891 bytes (exclusive)
```

The file occupies 6,231 sectors, from sector 32990 through sector 39220 inclusive.

These values provide the storage location needed for an independent sector-based carving attempt.

##### 4.3 File recovery using The Sleuth Kit

The deleted file was extracted using `icat` with the recovery option:

```bash
icat -r fat32_forensic.dd 4 > recovered_IMG_2019.jpg
```

The resulting file was inspected:

```bash
ls -lh recovered_IMG_2019.jpg
file recovered_IMG_2019.jpg
```

The `file` utility identified the recovered content as:

- JPEG image data.
- JFIF standard 1.02.
- EXIF metadata present.
- Manufacturer: Apple.
- Device model: iPhone 13 Pro.
- Image dimensions: 3024 × 4032.
- 8-bit precision.
- Three components.

**Recovery finding:** The extraction produced a file that was recognized as a JPEG image. This establishes that the recovered output has a recognizable JPEG structure. It does not, by itself, establish that every byte of the original file was recovered correctly.

##### 4.4 Independent Python file carving

A second recovery approach was performed using the custom Python file-carving utility and an offset definition file.

The offset definition was derived from the metadata:

```text
101B800,1323BFB,recovered_IMG_2019.jpg
```

The carving utility was executed against the supplied image:

```bash
python3 file_carver.py
```

The source image `fat32_forensic.dd` and the offset file `offsets.txt` were provided when prompted.

The script reported that the file was successfully carved and saved.

**Observation:** The Python utility used the calculated byte range to extract the file independently of the `icat` command.

**Evidence:** `screenshots/04-fat32-img-2019-metadata.png`

**Evidence:** `screenshots/05-fat32-img-2019-icat-recovery.png`

**Evidence:** `screenshots/06-fat32-img-2019-python-carving.png`

##### 4.5 Recovery validation

The recovered file was recognized as JPEG image data by the `file` utility.

A cryptographic hash comparison between independently retained `icat` and Python-carved outputs is still required before claiming that both recovery methods produced identical contents.

**Validation status:** File format identified; hash comparison pending.

##### 4.6 Evidence and interpretation

The examination of directory entry 4 established that:

1. The entry is marked as not allocated.
2. The file metadata reports a logical size of 3,190,011 bytes.
3. Its recorded sector range is 32990–39220.
4. The metadata contains a discrepancy in the reported filename.
5. The Written timestamp is anomalous and requires cautious interpretation.
6. A JPEG file was extracted using `icat`.
7. The Python carving utility also reported a successful extraction.

The metadata and recovery results are retained as separate observations. No attribution, user identity, deletion time, or explanation for the timestamp anomaly is inferred from the available evidence.

---

### Task 5: Separate Examination of the Second Deleted File

**Evidence Item 002 – IMG_0117.png**

The second deleted entry is directory entry 6, reported by `fls` as `IMG_0117.png`.

It will be documented as a separate evidence examination, with its own metadata record, storage-location calculations, recovery procedure, validation results, and supporting screenshots.

Its findings must not be combined with Evidence Item 001.

---

## 3. Evidence Management and Screenshots

Screenshots and generated evidence are stored separately from the source forensic image.

Save genuine terminal screenshots under:

```text
screenshots/
```

Evidence filenames should identify the examination stage and the associated evidence item.

The source image should remain unchanged during examination. Recovered files, offset definitions, logs, and reports should be treated as derived investigation artefacts.

Where possible, retain separate outputs for each recovery method so that validation can compare independently generated files.

## 4. Scripts

Reviewed forensic scripts are stored under:

```text
scripts/
```

The investigation uses custom Python utilities for sector-based file carving.

Supporting offset definitions should be retained with the corresponding evidence item and documented with their calculation method.

## 5. Investigation Reports

The final investigation report will be stored under:

```text
reports/fat32/
```

The report will consolidate the examination methodology, findings, evidence references, recovery results, validation outcomes, limitations, and conclusions.

## 6. Investigation Limitations

- The examination is based on the supplied forensic image.
- The available material does not establish the original device owner or the circumstances of deletion.
- No deletion timestamp has been established for the examined file.
- The anomalous Written timestamp has not been explained.
- A recognizable file signature does not alone prove complete recovery.
- Hash comparison of independently retained recovery outputs is required before asserting identical recovered content.
- Original acquisition records and chain-of-custody documentation have not yet been supplied or independently verified.

## Related Documentation

- [Project README](../../README.md)
- [NTFS investigation](../ntfs/README.md)
- [Raw disk investigation](../raw-disk/README.md)
