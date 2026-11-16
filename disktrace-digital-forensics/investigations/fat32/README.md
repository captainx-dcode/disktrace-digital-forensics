
# FAT32 Forensics Investigation

**Investigation:** 002 – FAT32 Disk Image Examination
**Status:** In Progress
**Evidence image:** `fat32_forensic.dd`

## 1. Investigation scope

This investigation examines the supplied FAT32 disk image following the NTFS investigation.

The examination covers the FAT32 boot sector, volume metadata, File Allocation Table, directory entries, cluster chains, deleted-file identification, and file recovery.

The investigation is conducted using The Sleuth Kit and custom Python file-carving scripts. Commands, observations, screenshots, findings, and recovery results are documented as each task is completed.

## 2. Task log

### Task 1: Environment Setup and Tool Verification

**Objective:** Prepare the forensic environment and verify the availability of the required forensic tools.

**Environment:**

- Host operating system: Kali Linux
- Container platform: Docker
- Docker image: `machokadee/forensics-lab:latest`
- Container working directory: `/home/student/Forensics`
- Execution user: `root`
- Forensic toolkit: The Sleuth Kit 4.12.1 (verify against the current session output)

**Commands used:**

Pull and launch the forensic lab:

```bash
docker pull machokadee/forensics-lab:latest
docker run -it --rm --privileged machokadee/forensics-lab:latest
```

Verify the environment:

```bash
whoami
id
pwd
ls -lh
```

Update package information and install or verify Sleuth Kit:

```bash
apt update
apt install sleuthkit -y
```

Verify the installed Sleuth Kit utilities:

```bash
fls -V
fsstat -V
```

**Observations:**

- The forensic container was successfully launched.
- The working directory was `/home/student/Forensics`.
- The FAT32 evidence image, `fat32_forensic.dd`, was available.
- The required Sleuth Kit utilities were available for examination.

**Screenshot:** `screenshots/01-fat32-environment-setup.png`

### Task 2: File-System Identification and Metadata Analysis

**Objective:** Identify the file-system type and examine its structural metadata.

**Commands used:**

```bash
file fat32_forensic.dd
fsstat fat32_forensic.dd
```

**Findings:**

The `file` utility identified the image as a DOS/MBR boot-sector image containing a FAT32 file system.

The `fsstat` output confirmed the FAT32 file-system type and provided the following metadata:

| Property               | Observed value       |
| ---------------------- | -------------------- |
| File-system type       | FAT32                |
| OEM name               | `mkfs.fat`         |
| Volume ID              | `0xa742e8f9`       |
| Volume label           | `NO NAME`          |
| Sector size            | 512 bytes            |
| Cluster size           | 512 bytes            |
| Root directory cluster | 2                    |
| Root directory sector  | 1608                 |
| Reserved sector range  | 0–31                |
| FAT 0                  | Sectors 32–819      |
| FAT 1                  | Sectors 820–1607    |
| Data area              | Sectors 1608–102399 |
| Total sector range     | 0–102399            |
| Total cluster range    | 2–100793            |

**Observations:**

- The image uses FAT32.
- Each cluster contains one 512-byte sector.
- The root directory is associated with cluster 2 and is located at sector 1608.
- Two File Allocation Tables are present.
- The data area begins at sector 1608.

**Screenshot:** `screenshots/02-fat32-filesystem-identification.png`

### Remaining examination areas

The following tasks will be documented as the investigation progresses:

- Listing allocated and deleted directory entries.
- Examining deleted-file metadata.
- Identifying file locations and cluster information.
- Recovering deleted files using Sleuth Kit.
- Performing Python-based file carving using calculated offsets.
- Verifying recovered files through file identification and hash comparison.

## 3. Screenshots

Store genuine terminal screenshots and other investigation evidence in:

```text
screenshots/
```

Current screenshot evidence:

- `01-fat32-environment-setup.png` – Environment setup and tool verification.
- `02-fat32-filesystem-identification.png` – FAT32 identification and structural metadata.

## 4. Scripts

Place reviewed FAT32-specific scripts in:

```text
scripts/
```

Python carving utilities and supporting offset files should be documented with their purpose and usage.

## 5. Reports

Final investigation reports will be stored under:

```text
reports/fat32/
```

## Related documentation

- [Project README](../../README.md)
- [NTFS investigation](../ntfs/README.md)
- [Raw disk investigation](../raw-disk/README.md)
