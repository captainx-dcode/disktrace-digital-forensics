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

### Task 3 onward – To be completed

Add one subsection per task as the investigation progresses. Keep the order of the assignment and do not pre-populate results.

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
