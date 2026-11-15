# NTFS Forensics Investigation

**Investigation:** 001 – NTFS Disk Image Examination
**Status:** Practical Tasks 1–5 completed; documentation and evidence organization in progress
**Primary evidence image:** `forensic_image.dd`

## 1. Investigation Scope

This investigation examines the supplied NTFS disk image, explores NTFS metadata and allocation structures, identifies deleted entries, and performs file recovery and integrity verification.

This README serves as the running guide and task record for the NTFS investigation. Findings are documented after the relevant tasks have been performed and supported by actual command output or screenshots.

## 2. Evidence and Lab Files

The Task 1 laboratory directory listing showed the following files:

| Filename               | Size shown by `ls -lh` | Role                                                   |
| ---------------------- | -----------------------: | ------------------------------------------------------ |
| `forensic_image.dd`  |                    50 MB | NTFS investigation image                               |
| `fat32_forensic.dd`  |                    50 MB | Reserved for the FAT32 investigation                   |
| `corrupted_drive.dd` |                    50 MB | Supplied lab image; role to be established if required |
| `M2_lab.dd`          |                    29 MB | Supplied lab image; role to be established if required |
| `carve_jpg.py`       |                   1.8 KB | Supplied Python script                                 |
| `carvepng.py`        |                   2.0 KB | Supplied Python script                                 |
| `file_carver.py`     |                   1.9 KB | Supplied Python script                                 |

The sizes above are the values displayed by the Task 1 `ls -lh` output, not forensic measurements of the underlying evidence.

## 3. Laboratory Environment

The actual environment used was:

| Component                   | Observed value                      |
| --------------------------- | ----------------------------------- |
| Host                        | Kali Linux                          |
| Analysis environment        | Ubuntu-based Docker container       |
| Docker image                | `machokadee/forensics-lab:latest` |
| Container working directory | `/home/student/Forensics`         |
| Container user              | `root`                            |
| Sleuth Kit                  | 4.12.1                              |
| Package version             | `4.12.1+dfsg-1.1ubuntu2`          |

**Environment clarification:** The task sheet describes launching an Ubuntu VM in VirtualBox. The recorded practical session instead used an Ubuntu-based Docker container on a Kali host. This investigation does not describe the Docker environment as a VirtualBox VM.

## 4. Task Log

### Task 1 – Laboratory Environment Preparation

**Status:** Practical setup completed.

**Objective:** Launch the supplied analysis environment, navigate to the forensic materials directory, and verify the availability of The Sleuth Kit tools.

#### Environment launch

The Docker image was pulled:

```bash
docker pull machokadee/forensics-lab:latest
```

The corrected command successfully launched the container:

```bash
docker run -it --rm --privileged machokadee/forensics-lab:latest
```

The first launch attempt contained a spelling error in the `--privileged` option and failed. The corrected command worked successfully.

#### User and working directory verification

Commands executed:

```bash
id
whoami
pwd
```

Observed results:

```text
uid=0(root) gid=0(root) groups=0(root)
root
/home/student/Forensics
```

#### Forensic materials inspection

```bash
ls -lh
```

The output showed the supplied disk images and Python scripts listed in Section 2.

#### Sleuth Kit verification

The following version checks were executed:

```bash
fls -V
fsstat -V
dpkg-query -W sleuthkit
```

Observed version information:

```text
The Sleuth Kit ver 4.12.1
The Sleuth Kit ver 4.12.1
sleuthkit  4.12.1+dfsg-1.1ubuntu2
```

The package installation command was also executed:

```bash
apt update && apt install sleuthkit -y
```

The package manager reported that Sleuth Kit was already the newest version.

#### Task 1 outcome

The Docker-based analysis environment was launched successfully. The working directory was confirmed, the supplied forensic materials were listed, and The Sleuth Kit version 4.12.1 was verified.

### Task 2 – File System Identification and Metadata Collection

**Objective:** Identify the file system used by the supplied forensic disk image and collect essential NTFS metadata.

#### 2.1 Identify the file system

Command:

```bash
file forensic_image.dd
```

Key output:

```text
DOS/MBR boot sector
OEM-ID "NTFS"
sectors/cluster 8
NTFS
$MFT start cluster 4
$MFTMirror start cluster 6399
serial number 06fbf04657eaf9a0a
```

The output identified the image as containing an NTFS file system and provided initial information about the MFT, MFT Mirror, and volume serial number.

#### 2.2 Collect file system metadata

Command:

```bash
fsstat forensic_image.dd
```

#### 2.3 Findings

| Attribute                | Observed value       |
| ------------------------ | -------------------- |
| File system              | NTFS                 |
| Volume serial number     | `6FBF04657EAF9A0A` |
| Reported NTFS version    | Windows XP           |
| Sector size              | 512 bytes            |
| Cluster size             | 4096 bytes           |
| First MFT cluster        | 4                    |
| First MFT Mirror cluster | 6399                 |
| MFT entry size           | 1024 bytes           |
| Index record size        | 4096 bytes           |
| Root directory entry     | 5                    |
| Total cluster range      | 0–12798             |
| Total sector range       | 0–102398            |

#### 2.4 Technical interpretation

**Cluster size calculation**

The file system reports 8 sectors per cluster. Each sector is 512 bytes.

```text
Cluster size = Sectors per cluster × Sector size
             = 8 × 512
             = 4096 bytes
```

Each NTFS cluster therefore occupies 4096 bytes (4 KiB).

**Master File Table (MFT)**

The first MFT cluster is 4. The MFT stores file and directory metadata, including filenames, timestamps, attributes, and references to file content.

Assuming the file system volume begins at byte offset zero:

```text
MFT starting offset = MFT starting cluster × Cluster size
                    = 4 × 4096
                    = 16384 bytes
                    = 0x4000
```

**MFT Mirror**

The MFT Mirror begins at cluster 6399. NTFS maintains copies of selected critical MFT records at this location to support recovery of important file system metadata.

**Root Directory**

The root directory is identified by MFT entry 5.

#### 2.5 Conclusion

The examination identified the supplied forensic image as an NTFS volume. The `fsstat` output established its sector and cluster sizes, MFT locations, MFT entry size, volume serial number, and root directory reference.

**Evidence:**

- `screenshots/02-filesystem-identification.png` — terminal evidence showing the `file` and `fsstat` commands and their output.

**Tools used:**

- `file` — initial file system identification.
- Sleuth Kit `fsstat` — file system metadata examination.

### Task 3 – Locate Deleted File Information

**Objective:** Identify deleted files in the NTFS disk image, examine their MFT metadata, and calculate the byte offsets required for subsequent manual file carving.

#### 3.1 List files in the disk image

Command:

```bash
fls -r forensic_image.dd
```

Finding:

```text
-/r * 64-128-2: IMG_3046.jpg
```

The output also identified an orphan-files directory containing entries 16–23.

**Interpretation:**

- `-/r` identifies a regular file entry.
- `*` indicates that the file has been deleted.
- `64-128-2` identifies the file's metadata address:
  - `64` — MFT entry number.
  - `128` — attribute type, representing `$DATA`.
  - `2` — attribute identifier.

The deleted file `IMG_3046.jpg` therefore retained an identifiable MFT record that could be examined further.

#### 3.2 Extract deleted file metadata

Command:

```bash
istat forensic_image.dd 64-128-2
```

Key findings:

| Attribute                              | Observed value   |
| -------------------------------------- | ---------------- |
| File name                              | `IMG_3046.jpg` |
| MFT entry                              | 64               |
| Sequence number                        | 2                |
| Allocation status                      | Not Allocated    |
| Parent MFT entry                       | 5                |
| Data attribute                         | `$DATA`        |
| Data attribute size                    | 10,626,782 bytes |
| Allocated size                         | 10,629,120 bytes |
| Actual size reported in `$FILE_NAME` | 0 bytes          |
| First storage cluster                  | 6912             |
| Last storage cluster                   | 9506             |

**Timestamps reported by `istat` (UTC):**

| Timestamp     | Value                         |
| ------------- | ----------------------------- |
| Created       | 2025-03-06 18:33:21.359054700 |
| File Modified | 2025-03-06 18:33:21.994406000 |
| MFT Modified  | 2025-03-06 18:33:21.994406000 |
| Accessed      | 2025-03-06 18:33:21.359054700 |

The output does not provide an explicit deletion timestamp. These timestamps should not be interpreted as the time the file was deleted.

#### 3.3 Interpret the metadata

**Allocation status**

The MFT entry is reported as `Not Allocated`. This indicates that the file's MFT record is no longer marked as allocated, consistent with the deleted-file entry identified by `fls`.

**File size**

The `$DATA` attribute reports a logical data size of 10,626,782 bytes. The `$FILE_NAME` attribute separately reports an allocated size of 10,629,120 bytes and an actual size of zero.

For the byte-offset calculation, the `$DATA` attribute size of **10,626,782 bytes** is used.

**Storage clusters**

The non-resident `$DATA` attribute lists storage clusters beginning at cluster 6912 and ending at cluster 9506. The listed cluster numbers are consecutive, indicating that the file's data run is contiguous in this image.

#### 3.4 Calculate the file's byte offsets

The cluster size established during Task 2 was 4096 bytes.

**Start of file:**

```text
Starting cluster × Cluster size

6912 × 4096 = 28,311,552 bytes
```

Convert the decimal offset to hexadecimal:

```bash
printf "%x\n" 28311552
```

Output:

```text
1b00000
```

Therefore:

```text
Start offset = 0x1B00000
```

**End of file (exclusive offset):**

Add the `$DATA` attribute size to the starting byte offset:

```text
Start offset + Data size

28,311,552 + 10,626,782 = 38,938,334 bytes
```

Convert the result to hexadecimal:

```bash
printf "%x\n" 38938334
```

Output:

```text
25226de
```

Therefore:

```text
Exclusive end offset = 0x25226DE
```

The last byte occupied by the file is at offset `0x25226DD`, because the calculated ending offset points to the byte immediately after the file's data.

#### 3.5 Conclusion

The examination identified `IMG_3046.jpg` as a deleted file whose MFT entry remained available for analysis.

The starting and exclusive ending byte offsets were calculated as:

- **Start offset:** `0x1B00000`
- **Exclusive end offset:** `0x25226DE`
- **Logical data size:** 10,626,782 bytes

These findings established the file's metadata and data location for the subsequent recovery activities.

**Evidence:**

- `screenshots/03-list-of-deleted-files.png` — deleted-file enumeration using `fls`.
- `screenshots/04-extracted-file-metadata.png` — MFT metadata and storage cluster information obtained using `istat`.

**Tools used:**

- Sleuth Kit `fls` — recursive file listing and deleted-file identification.
- Sleuth Kit `istat` — MFT entry and file metadata examination.
- `printf` — decimal-to-hexadecimal offset conversion.

### Task 4 – Recover Deleted Files

**Objective:** Recover the deleted `IMG_3046.jpg` file using two approaches:

1. Sleuth Kit's `icat` utility, using the NTFS metadata address.
2. The DiskTrace Python file-carving utility, using calculated byte offsets.

#### 4.1 Method 1: Recover using `icat`

The deleted file was recovered using its MFT metadata address:

```bash
icat forensic_image.dd 64-128-2 > recovered.jpg
```

The output was inspected using:

```bash
file recovered.jpg
```

The `file` utility identified the recovered output as JPEG image data.

| Property                      | Result              |
| ----------------------------- | ------------------- |
| Format                        | JPEG                |
| Dimensions                    | 3024 × 4032        |
| Camera model in EXIF metadata | Apple iPhone 13 Pro |
| JPEG type                     | Baseline            |

#### 4.2 Method 2: Recover using the DiskTrace Python carver

The improved DiskTrace utility, `file_carver2.py`, was used to extract the file using the start and end byte offsets calculated in Task 3.

The offsets were stored in `offsets.txt`:

```text
# start_offset_hex,end_offset_hex,output_filename
1B00000,25226DE,carved.jpg
```

The carver was executed using:

```bash
python3 file_carver2.py
```

Batch mode was selected, and `offsets.txt` was supplied.

The utility successfully extracted the specified byte range.

#### 4.3 Extraction results

| Field                  | Result                    |
| ---------------------- | ------------------------- |
| Source image           | `forensic_image.dd`     |
| Start offset           | `0x1B00000`             |
| End offset             | `0x25226DE` (exclusive) |
| Bytes extracted        | 10,626,782                |
| Output file            | `carved.jpg`            |
| Successful extractions | 1                         |
| Failed extractions     | 0                         |

**SHA-256 of Python-carved output:**

```text
c22411c0175a240ab2f96257d6babaa1c6068a3a653ed346ec86444dc8c146c9
```

#### 4.4 Recovery observations

The initial carver version did not correctly handle the comment line in the offsets file. An improved version, `file_carver2.py`, was used to complete the extraction successfully.

Both recovery approaches produced output files for the same deleted JPEG.

The MD5 comparison performed in Task 5 subsequently confirmed that the two recovered outputs had matching contents.

#### 4.5 Conclusion

The deleted JPEG was successfully extracted using both metadata-based recovery with `icat` and byte-offset carving with the DiskTrace Python utility.

**Evidence:**

- `screenshots/05-icat-file-recovery.png` — recovery using `icat` and JPEG identification.
- `screenshots/06-python-file-carving.png` — Python carver execution and extraction results.

**Tools used:**

- Sleuth Kit `icat`
- `file`
- Python 3
- DiskTrace `file_carver2.py`

### Task 5 – Verify File Integrity (MD5 Hash Comparison)

**Objective:** Verify the integrity of the recovered file by comparing its MD5 checksum against the reference checksum provided in the practical exercise.

#### 5.1 Generate MD5 hashes

The following command was executed:

```bash
md5sum carved.jpg recovered.jpg
```

#### 5.2 Actual results

```text
bfc40fd6b8adf2e7745d833de36b4bc0  carved.jpg
bfc40fd6b8adf2e7745d833de36b4bc0  recovered.jpg
```

#### 5.3 Reference MD5

The practical exercise provided the following reference checksum:

```text
bfc40fd6b8adf2e7745d833de36b4bc0
```

#### 5.4 Analysis

Both recovered files produced identical MD5 checksums. Their checksums also match the reference value supplied in the exercise.

This confirms that the `icat` extraction and the Python-based carving operation produced identical file contents and match the supplied reference checksum.

**Note:** The reference checksum was supplied by the exercise. It was not independently calculated from a separate original copy of `IMG_3046.jpg`.

#### 5.5 Conclusion

The integrity verification was successful. Both recovery methods produced matching outputs according to the MD5 comparison.

**Evidence:**

- `screenshots/08-md5-integrity-verification.png` — MD5 checksums of `carved.jpg` and `recovered.jpg`.

**Tool used:**

- `md5sum` — MD5 checksum generation and comparison.

## 5. Screenshots Directory

Task evidence is stored in:

```text
investigations/ntfs/screenshots/
```

Current task evidence includes:

| Screenshot                            | Evidence                         |
| ------------------------------------- | -------------------------------- |
| `01-environment-setup.png`          | Laboratory environment setup     |
| `02-filesystem-identification.png`  | NTFS identification and metadata |
| `03-list-of-deleted-files.png`      | Deleted-file enumeration         |
| `04-extracted-file-metadata.png`    | Deleted file MFT metadata        |
| `05-icat-file-recovery.png`         | Metadata-based file recovery     |
| `06-python-file-carving.png`        | Python-based file carving        |
| `08-md5-integrity-verification.png` | MD5 integrity comparison         |

Only include screenshots that contain actual captured lab output. Do not recreate or fabricate terminal evidence.

Before committing, check screenshots for sensitive information, unrelated terminal content, and accidental display of recovered personal files.

## 6. Scripts Directory

Place NTFS-specific scripts in:

```text
investigations/ntfs/scripts/
```

Only add scripts after reviewing and understanding their behaviour. Document their inputs, outputs, limitations, and execution instructions.

## 7. Investigation Report

The completed NTFS investigation report is stored in:

```text
investigations/ntfs/report/
```

The report summarizes the investigation scope, NTFS metadata findings, deleted-file identification, recovery methods, and integrity verification.

The report is based on completed tasks and observed evidence rather than planned activities.

## 8. Related Project Documentation

- [DiskTrace project README](../../README.md)
- [Project overview](../../documentation/project-overview.md)
- [Methodology](../../documentation/methodology.md)
- [Evidence handling](../../documentation/evidence-handling.md)
