# NTFS Forensics Investigation

**Investigation:** 001 – NTFS Disk Image Examination  
**Status:** In progress  
**Primary evidence image:** `forensic_image.dd`

## 1. Investigation scope

This investigation will examine the supplied NTFS disk image, explore NTFS metadata and allocation structures, identify deleted entries, and perform recovery exercises as directed by the task sequence.

This README is the running guide and task record for the NTFS investigation. It deliberately does not pre-fill later findings. Each task will be added after it has been performed, understood, and supported with screenshots.

## 2. Evidence and lab files

The lab directory listing during Task 1 showed these files:

| Filename | Size shown by `ls -lh` | Role |
|---|---:|---|
| `forensic_image.dd` | 50 MB | NTFS investigation image (to be examined in subsequent tasks) |
| `fat32_forensic.dd` | 50 MB | Reserved for the FAT32 investigation |
| `corrupted_drive.dd` | 50 MB | Supplied lab image; role to be established if required |
| `M2_lab.dd` | 29 MB | Supplied lab image; role to be established if required |
| `carve_jpg.py` | 1.8 KB | Supplied Python script |
| `carvepng.py` | 2.0 KB | Supplied Python script |
| `file_carver.py` | 1.9 KB | Supplied Python script |

The sizes above are the values displayed by the Task 1 `ls -lh` output, not forensic measurements of the underlying evidence.

## 3. Laboratory environment

The actual environment used for Task 1 was:

| Component | Observed value |
|---|---|
| Host | Kali Linux |
| Analysis environment | Ubuntu-based Docker container |
| Docker image | `machokadee/forensics-lab:latest` |
| Container working directory | `/home/student/Forensics` |
| Container user | `root` |
| Sleuth Kit | 4.12.1 |
| Package version | `4.12.1+dfsg-1.1ubuntu2` |

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

| Screenshot | What it should show |
|---|---|
| `01-docker-image-pull.png` | Successful Docker image pull |
| `02-container-launch-and-identity.png` | Corrected container launch and `id` / `whoami` |
| `03-working-directory-and-materials.png` | `pwd` and `ls -lh` |
| `04-sleuthkit-version.png` | `fls -V`, `fsstat -V`, and package version |

Do not recreate or fabricate terminal screenshots. Capture the real output from the lab. The failed `--priileged` attempt may be omitted from the evidence screenshots; the documentation records the typo for transparency.

### Task 2 – To be completed

Do not add findings here until the next task has been performed. Record its objective, commands, actual output, screenshots, observations, and limitations.

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
