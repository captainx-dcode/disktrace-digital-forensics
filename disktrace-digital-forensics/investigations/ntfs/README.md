# NTFS Forensics Investigation

**Investigation:** 001 – NTFS Disk Image Examination
**Status:** In progress
**Primary evidence image:** `forensic_image.dd`

## 1. Investigation scope

This investigation will examine the supplied NTFS disk image, explore NTFS metadata and allocation structures, identify deleted entries, and perform recovery exercises as directed by the task sequence.

This README is the running guide and task record for the NTFS investigation. It deliberately does not pre-fill later findings. Each task will be added after it has been performed, understood, and supported with screenshots.

## 2. Evidence and lab files

The lab directory listing during Task 1 showed these files:

| Filename               | Size shown by `ls -lh` | Role                                                          |
| ---------------------- | -----------------------: | ------------------------------------------------------------- |
| `forensic_image.dd`  |                    50 MB | NTFS investigation image (to be examined in subsequent tasks) |
| `fat32_forensic.dd`  |                    50 MB | Reserved for the FAT32 investigation                          |
| `corrupted_drive.dd` |                    50 MB | Supplied lab image; role to be established if required        |
| `M2_lab.dd`          |                    29 MB | Supplied lab image; role to be established if required        |
| `carve_jpg.py`       |                   1.8 KB | Supplied Python script                                        |
| `carvepng.py`        |                   2.0 KB | Supplied Python script                                        |
| `file_carver.py`     |                   1.9 KB | Supplied Python script                                        |

The sizes above are the values displayed by the Task 1 `ls -lh` output, not forensic measurements of the underlying evidence.

## 3. Laboratory environment

The actual environment used for Task 1 was:

| Component                   | Observed value                      |
| --------------------------- | ----------------------------------- |
| Host                        | Kali Linux                          |
| Analysis environment        | Ubuntu-based Docker container       |
| Docker image                | `machokadee/forensics-lab:latest` |
| Container working directory | `/home/student/Forensics`         |
| Container user              | `root`                            |
| Sleuth Kit                  | 4.12.1                              |
| Package version             | `4.12.1+dfsg-1.1ubuntu2`          |

**Environment clarification:** The task sheet describes launching an Ubuntu VM in VirtualBox. The recorded session instead used an Ubuntu-based Docker container on a Kali host. Do not describe this session as a VirtualBox VM. Confirm with the instructor whether the Docker-based environment is an accepted substitute if the VM requirement is strict.

## 4. Task log

### Task 1 – Laboratory environment preparation

**Status:** Practical setup completed; screenshots and final Git documentation still to be added.

**Objective:** Launch the supplied analysis environment, navigate to the forensic materials directory, and verify the availability of The Sleuth Kit tools.

#### Environment launch

The Docker image was pulled:

```bash
docker pull machokadee/forensics-lab:latest
```

The first container launch attempt contained a spelling error in the option (`--priileged`) and failed. The corrected command successfully launched the container:

```bash
docker run -it --rm --privileged machokadee/forensics-lab:latest
```

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

Command executed:

```bash
ls -lh
```

The output showed the supplied disk images and Python scripts listed in Section 2.

#### Sleuth Kit verification

The task sheet suggests `fls -v` and `fsstat -v` for checking versions. In The Sleuth Kit, uppercase `-V` displays the version, while lowercase `-v` enables verbose output. The following version checks were executed:

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

The Docker-based analysis environment was launched successfully. The working directory was confirmed as `/home/student/Forensics`, the supplied forensic materials were listed, and The Sleuth Kit version 4.12.1 was verified as installed.

This completes the practical environment checks recorded for Task 1. The screenshot evidence still needs to be captured and added to this repository.

#### Task 1 screenshots

Save actual terminal screenshots in `screenshots/` using these suggested filenames:

| Screenshot                                 | What it should show                                |
| ------------------------------------------ | -------------------------------------------------- |
| `01-docker-image-pull.png`               | Successful Docker image pull                       |
| `02-container-launch-and-identity.png`   | Corrected container launch and `id` / `whoami` |
| `03-working-directory-and-materials.png` | `pwd` and `ls -lh`                             |
| `04-sleuthkit-version.png`               | `fls -V`, `fsstat -V`, and package version     |

Do not recreate or fabricate terminal screenshots. Capture the real output from the lab. The failed `--priileged` attempt may be omitted from the evidence screenshots; the documentation records the typo for transparency.

## Task 2: File System Identification and Metadata Collection

### Objective

Identify the file system used by the supplied forensic disk image and collect essential NTFS metadata to support subsequent examination and recovery activities.

### 1. Identify the File System

The `file` utility was used to inspect the disk image and identify its file system characteristics.

**Command:**

```bash
file forensic_image.dd
```

**Key output:**

```text
DOS/MBR boot sector
OEM-ID "NTFS"
sectors/cluster 8
NTFS
$MFT start cluster 4
$MFTMirror start cluster 6399
serial number 06fbf04657eaf9a0a
```

The output identified the image as containing an NTFS file system. It also provided initial information about the location of the Master File Table (MFT), its mirror, and the volume serial number.

### 2. Collect File System Metadata

Sleuth Kit's `fsstat` utility was used to examine the file system metadata directly from the disk image.

**Command:**

```bash
fsstat forensic_image.dd
```

### 3. Findings

The following information was extracted from the `fsstat` output:

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

### 4. Technical Interpretation

**Cluster size calculation**

The file system reports 8 sectors per cluster. Each sector is 512 bytes.

```text
Cluster size = Sectors per cluster × Sector size
             = 8 × 512
             = 4096 bytes
```

This confirms that each NTFS cluster occupies 4096 bytes (4 KiB).

**Master File Table (MFT)**

The first MFT cluster is 4. The MFT stores file and directory metadata, including file names, timestamps, attributes, and references to file content.

Assuming the file system volume begins at byte offset zero:

```text
MFT starting offset = MFT starting cluster × Cluster size
                    = 4 × 4096
                    = 16384 bytes
                    = 0x4000
```

**MFT Mirror**

The MFT Mirror begins at cluster 6399. NTFS maintains copies of selected critical MFT records in this location to support recovery of important file system metadata.

**Root Directory**

The root directory is identified by MFT entry 5, a standard NTFS root directory reference.

### 5. Conclusion

The examination identified the supplied forensic image as an NTFS volume. The `fsstat` output established its sector and cluster sizes, MFT locations, MFT entry size, volume serial number, and root directory reference.

These findings provide the initial file system metadata required for subsequent NTFS investigation tasks.

### Evidence

- `screenshots/02-filesystem-identification.png` — consolidated terminal screenshot showing the `file` and `fsstat` commands and their output.

### Tools Used

- `file` — initial file system identification.
- Sleuth Kit `fsstat` — file system metadata examination.

## Task 3: Locate Deleted File Information

### Objective

Identify deleted files in the NTFS disk image, examine their Master File Table (MFT) metadata, and calculate the byte offsets required for subsequent manual file carving.

### 1. List Files in the Disk Image

The Sleuth Kit `fls` utility was used to recursively list files and directories in the forensic image, including deleted entries.

**Command:**

```bash
fls -r forensic_image.dd
```

**Finding:**

The output identified a deleted JPEG file:

```text
-/r * 64-128-2: IMG_3046.jpg
```

The output also identified an orphan-files directory containing entries 16–23.

**Interpretation:**

- `-/r` identifies a regular file entry.
- `*` indicates that the file has been deleted.
- `64-128-2` identifies the file's MFT metadata address:
  - `64` — MFT entry number.
  - `128` — attribute type, representing `$DATA`.
  - `2` — attribute identifier.

The deleted file `IMG_3046.jpg` therefore retains an identifiable MFT record that can be examined further.

### 2. Extract Deleted File Metadata

The `istat` utility was used to examine the metadata associated with the deleted file.

**Command:**

```bash
istat forensic_image.dd 64-128-2
```

**Key findings:**

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

The output does not provide an explicit deletion timestamp. The timestamps above should therefore not be interpreted as the time the file was deleted.

### 3. Interpret the Metadata

**Allocation status**

The MFT entry is reported as `Not Allocated`. This indicates that the file's MFT record is no longer marked as allocated, consistent with the deleted-file entry identified by `fls`.

**File size**

The `$DATA` attribute reports a logical data size of 10,626,782 bytes. The `$FILE_NAME` attribute separately reports an allocated size of 10,629,120 bytes and an actual size of zero.

For the byte-offset calculation below, the `$DATA` attribute size of **10,626,782 bytes** is used.

**Storage clusters**

The non-resident `$DATA` attribute lists storage clusters beginning at cluster 6912 and ending at cluster 9506.

The listed cluster numbers are consecutive, indicating that the file's data run is contiguous in this image.

### 4. Calculate the File's Byte Offsets

The cluster size established during Task 2 was 4096 bytes.

The first data cluster is 6912. To determine the byte offset at which the file's data begins, multiply the starting cluster by the cluster size.

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

Therefore, the starting byte offset is:

```text
0x1B00000
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

Therefore, the exclusive ending offset is:

```text
0x25226DE
```

The last byte occupied by the file is at offset `0x25226DD`, because the calculated ending offset points to the byte immediately after the file's data.

### 5. Conclusion

The examination identified `IMG_3046.jpg` as a deleted file whose MFT entry remains available for analysis.

The `istat` output provided its timestamps, allocation status, data attribute size, and storage cluster information. Using the cluster size established in Task 2, the starting and exclusive ending byte offsets were calculated as:

- **Start offset:** `0x1B00000`
- **Exclusive end offset:** `0x25226DE`
- **Logical data size:** 10,626,782 bytes

These findings establish the file's metadata and data location for the subsequent recovery and carving activities.

### Evidence

- `screenshots/03-list-of-deleted-files.png` — terminal evidence showing deleted-file enumeration using `fls`.
- `screenshots/04-extracted-file-metadata.png` — terminal evidence showing the MFT metadata and storage cluster information obtained using `istat`.

### Tools Used

- Sleuth Kit `fls` — recursive file listing and deleted-file identification.
- Sleuth Kit `istat` — MFT entry and file metadata examination.
- `printf` — decimal-to-hexadecimal offset conversion.

## 5. Screenshots directory

Place task evidence in:

```text
investigations/ntfs/screenshots/
```

Before committing, check screenshots for sensitive information, unrelated terminal content, and accidental display of recovered personal files.

## 6. Scripts directory

Place NTFS-specific scripts in:

```text
investigations/ntfs/scripts/
```

Only add scripts after reviewing and understanding their behaviour. Document their inputs, outputs, limitations, and execution instructions.

## 7. Reports

Investigation reports will be placed in the root `reports/ntfs/` directory. The report should be based on completed tasks and actual evidence, not on the planned roadmap.

## 8. Related project documentation

- [DiskTrace project README](../../README.md)
- [Project overview](../../documentation/project-overview.md)
- [Methodology](../../documentation/methodology.md)
- [Evidence handling](../../documentation/evidence-handling.md)
