
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
3. Automated file recovery
4. Manual file-signature analysis and carving
5. Recovery validation
6. Findings and conclusion

## 5. Evidence Inventory

The supplied evidence image is named `corrupted_drive.dd`.

The evidence image was located in:

`/home/student/Forensics`

## 6. Examination and Findings

### 6.1 Evidence File Identification

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

### 6.2 Disk Geometry and Partition Examination

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
- No partition entries were displayed.

**Interpretation:**

The command established the image's reported size and sector geometry. No partition entries were displayed, so a conventional partition layout was not identified by this examination.

The absence of displayed partition entries does not prove that the image contains no filesystem structures or file data.

### 6.3 Filesystem Listing and Entropy Observation

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

The command did not provide a filesystem directory listing. Further raw-data and file-signature analysis is necessary.

### 6.4 Automated File Recovery Using Foremost

**Command:**

```bash
foremost -i corrupted_drive.dd -o extracted_files
```

**Observed output:**

```text
Processing: corrupted_drive.dd
|*|
```

The output directory was inspected using:

```bash
ls extracted_files
```

**Observed output:**

```text
audit.txt  jpg
```

The extracted files were then identified using:

```bash
find extracted_files -type f -exec file {} \;
```

**Observed output:**

```text
extracted_files/jpg/00076540.jpg: JPEG image data, JFIF standard 1.02, resolution (DPI), density 72x72, segment length 16, Exif Standard: [TIFF image data, big-endian, direntries=14, manufacturer=Apple, model=iPhone 13 Pro, orientation=upper-left, xresolution=202, yresolution=210, resolutionunit=2, software=15.6.1, datetime=2023:10:18 13:14:26, hostcomputer=iPhone 13 Pro], baseline, precision 8, 3024x4032, components 3
extracted_files/audit.txt: ASCII text
```

The SHA-256 hash of the extracted JPEG was calculated:

```bash
find extracted_files -type f ! -name audit.txt -exec sha256sum {} \;
```

**Observed output:**

```text
c22411c0175a240ab2f96257d6babaa1c6068a3a653ed346ec86444dc8c146c9  extracted_files/jpg/00076540.jpg
```

**Observations:**

- Foremost identified and extracted one JPEG file.
- The extracted file is named `00076540.jpg`.
- The image dimensions reported by `file` are 3024 × 4032 pixels.
- EXIF metadata identifies an Apple iPhone 13 Pro.
- The reported image timestamp is 2023:10:18 13:14:26.
- The extracted JPEG's SHA-256 hash was recorded.

**Interpretation:**

Foremost successfully produced a file that its identification utility recognizes as a JPEG image. This establishes that a recognizable JPEG data structure was extracted. Further validation is required to establish whether the recovered file can be decoded and whether it is complete.

### 6.5 Automated File-Signature Analysis and Extraction Using Binwalk

The image was first examined using:

```bash
binwalk corrupted_drive.dd
```

**Observed output:**

```text
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
35414314      0x21C612A       PNG image, 3024 x 4032, 8-bit/color RGB, non-interlaced
35414740      0x21C62D4       TIFF image data, big-endian, offset of first image directory: 8
39188975      0x255F9EF       JPEG image data, JFIF standard 1.02
39189005      0x255FA0D       TIFF image data, big-endian, offset of first image directory: 8
```

An extraction attempt was made using:

```bash
binwalk --run-as=root -e corrupted_drive.dd
```

The signature scan reported the same four entries.

Because the extraction directory was not available after this attempt, extraction was retried using:

```bash
binwalk --run-as=root -D='.*' corrupted_drive.dd
```

The resulting directory was inspected:

```bash
ls _corrupted_drive.dd.extracted/
```

**Observed output:**

```text
21C612A  21C62D4  255F9EF  255FA0D
```

The extracted directory was examined in more detail:

```bash
ls -lah _corrupted_drive.dd.extracted/
```

**Observed output:**

```text
total 58M
drwxr-xr-x 2 root root 4.0K Nov 18 09:25 .
drwxr-xr-x 1 root root 4.0K Nov 18 09:25 ..
-rw-r--r-- 1 root root  17M Nov 18 09:25 21C612A
-rw-r--r-- 1 root root  17M Nov 18 09:25 21C62D4
-rw-r--r-- 1 root root  13M Nov 18 09:25 255F9EF
-rw-r--r-- 1 root root  13M Nov 18 09:25 255FA0D
```

**Observations:**

Binwalk identified four signatures at the following offsets:

| Detected signature | Decimal offset | Hexadecimal offset |
| ------------------ | -------------: | ------------------ |
| PNG                |     35,414,314 | `0x21C612A`      |
| TIFF               |     35,414,740 | `0x21C62D4`      |
| JPEG               |     39,188,975 | `0x255F9EF`      |
| TIFF               |     39,189,005 | `0x255FA0D`      |

Four data segments were extracted using the all-signatures extraction option.

**Interpretation:**

Binwalk identified recognizable PNG, TIFF, and JPEG signatures within the raw disk image.

The extracted files are named using their hexadecimal starting offsets. Their existence confirms that Binwalk produced data segments from the identified locations; it does not independently establish that all four segments are complete, standalone, valid files.

The TIFF signatures occur shortly after the PNG and JPEG signatures. These may represent embedded image metadata rather than separate standalone TIFF images. This requires further examination.

The PNG signature was detected and a corresponding data segment was extracted by the all-signatures extraction command. Its completeness and validity still require manual investigation.

### 6.6 Preliminary Automated Recovery Findings

| Reference | Tool                 | Result                                 |
| --------- | -------------------- | -------------------------------------- |
| F-05      | Foremost             | One JPEG extracted                     |
| F-06      | Foremost and file    | JPEG structure and metadata recognized |
| F-07      | Foremost and SHA-256 | Extracted JPEG hash recorded           |
| F-08      | Binwalk              | Four file signatures detected          |
| F-09      | Binwalk extraction   | Four data segments produced            |

## 7. Screenshots

| Screenshot                                  | Description                                                                                    |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `01-raw-disk-preliminary-examination.png` | File identification, disk geometry, and filesystem listing                                     |
| `02-automated-file-recovery.png`          | Foremost extraction, JPEG identification, SHA-256 result, and Binwalk detection and extraction |

## 8. Limitations

- The generic `file` identification result does not establish the absence of filesystem structures.
- The `fdisk` output did not display partition entries, but this does not rule out unpartitioned filesystem data or embedded file structures.
- The high-entropy warning is heuristic and cannot independently confirm encryption.
- Foremost's JPEG identification does not independently prove that the image is complete or fully decodable.
- Binwalk's signature detections do not prove that each detected signature represents an independent file.
- The completeness of the Binwalk-extracted data segments has not yet been established.
- The SHA-256 hash has been recorded, but no comparison against the earlier recovered JPEG has yet been documented.

## 9. Conclusion

The automated recovery stage identified potentially recoverable image data within the raw disk image.

Foremost extracted one JPEG file, and Binwalk identified four file signatures and produced four corresponding data segments using its all-signatures extraction option.

These results provide a basis for further manual carving and validation. The investigation will continue by examining the file signatures and determining the actual boundaries and completeness of the recovered data.

The investigation remains in progress.
