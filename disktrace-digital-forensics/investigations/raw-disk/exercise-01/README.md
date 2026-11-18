# Raw Disk Forensics – Exercise 1

**Investigation:** 003 – Raw Disk Image Examination
**Exercise:** 01
**Status:** In Progress
**Evidence image:** `corrupted_drive.dd`

## 1. Investigation Overview

This investigation examines a supplied raw disk image to identify recognizable file structures, investigate potentially recoverable data, and evaluate file-carving techniques.

The examination uses filesystem analysis, file-signature identification, hexadecimal inspection, automated recovery tools, and Python-based file carving. Recovered data will be assessed carefully to distinguish between signature detection, extraction, and successful file validation.

## 2. Investigation Objectives

- Establish the characteristics and structure of the supplied raw disk image.
- Examine recognizable filesystem and file signatures.
- Identify potentially recoverable files.
- Apply file-carving techniques using forensic tools and Python.
- Validate extracted files using file identification, metadata inspection, image rendering, and cryptographic hashes.
- Compare files recovered by different carving methods.
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
5. Python-based automated PNG carving
6. Recovery validation and comparison
7. Findings and conclusion

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

Extraction was then performed using:

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

The PNG signature was detected and a corresponding data segment was extracted. Its completeness and validity require further investigation.

### 6.6 Manual File-Signature Identification and Offset Analysis

This stage investigates the PNG file signature identified during the automated Binwalk examination. The objective is to locate the exact starting offset of the PNG data and investigate its expected ending signature.

#### 6.6.1 Identifying the PNG Header

**PNG signature:**

```text
89 50 4E 47 0D 0A 1A 0A
```

The hexadecimal dump was searched using:

```bash
xxd corrupted_drive.dd | egrep "89 ?50 ?4e ?47"
```

**Observed output:**

```text
021c6120: 7c83 c888 c01e 407a c1ae 8950 4e47 0d0a  |.....@z...PNG..
```

**Offset calculation:**

The displayed line begins at hexadecimal offset `0x021C6120`.

Each line contains 16 bytes, and the PNG signature begins at byte position 10 (hexadecimal A) within the displayed line.

Therefore:

```text
0x021C6120 + 0x0A = 0x021C612A
```

The identified PNG starting offset is:

- Hexadecimal: `0x21C612A`
- Decimal: `35,414,314`

**Observation:**

The PNG header was located at offset `35,414,314`, matching the offset previously reported by Binwalk.

**Interpretation:**

The matching offsets provide consistent evidence that the PNG signature identified by Binwalk corresponds to the signature located during manual hexadecimal inspection.

#### 6.6.2 Investigating the PNG End Signature

The expected PNG IEND signature is:

```text
49 45 4E 44 AE 42 60 82
```

The initial search command was:

```bash
xxd corrupted_drive.dd | egrep "42 ?60 ?82"
```

**Observed output:**

```text
00e04990: 4260 820e ec38 60db 6117 0359 ccf8 65ab
01166e20: 9f47 40c5 4260 82e7 b077 e125 222d e950
```

**Observation:**

Two occurrences of the byte sequence `42 60 82` were identified.

**Interpretation:**

The search examined only the final three bytes of the expected IEND signature. These occurrences cannot independently establish the presence or location of a valid PNG ending marker.

A subsequent complete signature search was performed during the Python carving stage. The script searched for the full eight-byte sequence:

```text
49 45 4E 44 AE 42 60 82
```

**Observed result:**

```text
Complete IEND signatures found: 0
```

**Finding:**

No complete eight-byte PNG IEND signature was identified by the Python search in the supplied evidence image.

This means that the PNG's expected ending marker was not located using the implemented signature search. The finding does not, on its own, explain why the marker is absent or prove that the PNG image data is entirely unrecoverable.

#### 6.6.3 File Signature Reference

File signatures, also called magic numbers or magic bytes, are byte sequences associated with particular file formats.

Examples include:

- PNG – Portable Network Graphics
- JPEG – Joint Photographic Experts Group
- TIFF – Tagged Image File Format
- GIF – Graphics Interchange Format
- PDF – Portable Document Format

The GCK File Signature Table is used as a reference for researching file signatures and identifying file formats.

Reference: https://filesig.search.org/

#### 6.6.4 Preliminary Findings

| Reference | Examination            | Finding                                                                                |
| --------- | ---------------------- | -------------------------------------------------------------------------------------- |
| F-10      | PNG header search      | PNG signature located                                                                  |
| F-11      | Offset calculation     | PNG begins at decimal offset 35,414,314 (`0x21C612A`)                                |
| F-12      | Partial footer search  | Two occurrences of `42 60 82` identified; neither confirms a complete IEND signature |
| F-13      | Complete footer search | No complete eight-byte IEND signature found                                            |

### 6.7 Automated PNG Carving Using Python

#### 6.7.1 Objective

Develop and execute a Python script to locate PNG file signatures within the supplied raw disk image and carve the identified data into a separate output file.

The script searches for:

- PNG header: `89 50 4E 47 0D 0A 1A 0A`
- PNG IEND footer: `49 45 4E 44 AE 42 60 82`

The script records signature offsets, extracts the data, and calculates a SHA-256 hash of the recovered output.

#### 6.7.2 Implementation

**Script:** `carving_png.py`

The Python implementation uses binary file handling and signature searches to locate PNG data within `corrupted_drive.dd`.

The carving logic searches for PNG headers and complete IEND signatures. It selects the first IEND signature occurring after the PNG header. Where no complete IEND signature is found, it extracts from the header to the end of the evidence image.

The output is saved as:

`M2_TL_recovered_files/recovered_0.png`

#### 6.7.3 Script Compilation

The Python scripts were checked for syntax errors using:

```bash
python3 -m py_compile carvepng.py
python3 -m py_compile carving_png.py
```

**Observed result:**

Both commands completed without displaying errors.

**Interpretation:**

The Python interpreter successfully compiled both scripts without reporting syntax errors. This check does not independently establish that the carving logic produces a complete or valid image.

#### 6.7.4 Execution Results

The script was executed using:

```bash
python3 carving_png.py
```

**Observed output:**

```text
=== PNG CARVING REPORT ===
Evidence image: corrupted_drive.dd
Image size: 52428800 bytes
PNG headers found: 1
Complete IEND signatures found: 0

=== RECOVERY RESULTS ===

File: M2_TL_recovered_files/recovered_0.png
Start offset: 35414314 (0x21c612a)
End offset (exclusive): 52428800 (0x3200000)
Recovery method: No IEND signature found; carved to end of image
Extracted size: 17014486 bytes
SHA-256: 414fd63e64a810c453c0c46c4f14cc49233c2e15780bf67a0b68ee06f15ab838

=== CARVING COMPLETE ===
```

**Observed findings:**

| Finding                        | Observed result            |
| ------------------------------ | -------------------------- |
| Evidence image                 | `corrupted_drive.dd`     |
| Evidence image size            | 52,428,800 bytes           |
| PNG headers found              | 1                          |
| Complete IEND signatures found | 0                          |
| PNG header offset              | 35,414,314 (`0x21c612a`) |
| Extraction end offset          | 52,428,800 (`0x3200000`) |
| Extraction method              | Carved to end of image     |
| Extracted file size            | 17,014,486 bytes           |
| Output filename                | `recovered_0.png`        |

No complete PNG IEND signature was detected. Consequently, the script used the end of the disk image as the extraction boundary.

The extracted size is consistent with the difference between the image size and the PNG starting offset:

```text
52,428,800 - 35,414,314 = 17,014,486 bytes
```

#### 6.7.5 Preliminary Output Examination

The recovered file was examined using:

```bash
file M2_TL_recovered_files/recovered_0.png
```

**Observed output:**

```text
M2_TL_recovered_files/recovered_0.png: PNG image data, 3024 x 4032, 8-bit/color RGB, non-interlaced
```

The file size was examined using:

```bash
stat -c '%n | %s bytes' M2_TL_recovered_files/recovered_0.png
```

**Observed output:**

```text
M2_TL_recovered_files/recovered_0.png | 17014486 bytes
```

The first 32 bytes were inspected using:

```bash
xxd -l 32 M2_TL_recovered_files/recovered_0.png
```

**Observed output:**

```text
00000000: 8950 4e47 0d0a 1a0a 0000 000d 4948 4452  .PNG........IHDR
00000010: 0000 0bd0 0000 0fc0 0802 0000 002f 798d  ............./y.
```

The SHA-256 hash was calculated using:

```bash
sha256sum M2_TL_recovered_files/recovered_0.png
```

**Observed output:**

```text
414fd63e64a810c453c0c46c4f14cc49233c2e15780bf67a0b68ee06f15ab838  M2_TL_recovered_files/recovered_0.png
```

**Observations:**

- The `file` utility recognized the extracted data as PNG.
- The reported image dimensions are 3024 × 4032 pixels.
- The first eight bytes match the PNG signature.
- The following bytes contain an IHDR chunk identifying the image dimensions.
- The extracted file size is 17,014,486 bytes.
- The SHA-256 hash was recorded.

**Preliminary interpretation:**

The carving operation successfully extracted a data segment beginning at the identified PNG header. The PNG signature and IHDR structure were present, and the `file` utility recognized the resulting data as PNG.

However, the absence of a detected IEND signature means that complete file recovery has not yet been established. The extracted segment may contain incomplete image data or unrelated trailing bytes.

Further validation will compare the Python-carved output against the data segments produced by Binwalk. The Foremost output will also be examined to establish which recovered files are available for comparison.

**Status:** Automated PNG carving completed; recovery validation pending.


## 7. Recovery Validation and Comparison

This stage validates the files recovered using Binwalk, Foremost and the custom Python carving script. Validation included file identification, exact file-size comparison, MD5 and SHA-256 checksums, binary comparison and visual inspection.

### 7.1 Recovered File Inventory

The following recovery outputs were examined:

| Recovery method | Output file                               | Identified type |
| --------------- | ----------------------------------------- | --------------- |
| Binwalk         | `_corrupted_drive.dd.extracted/21C612A` | PNG             |
| Python carving  | `M2_TL_recovered_files/recovered_0.png` | PNG             |
| Binwalk         | `_corrupted_drive.dd.extracted/255F9EF` | JPEG            |
| Foremost        | `extracted_files/jpg/00076540.jpg`      | JPEG            |

The two additional Binwalk outputs, `21C62D4` and `255FA0D`, were identified by the `file` utility as TIFF data. They were retained as separate signature-detection results and were not treated as independently validated image recoveries.

### 7.2 File Identification

The `file` utility was used to identify the recovered candidates.

Results:

- Binwalk PNG: PNG image data, 3024 × 4032, 8-bit RGB, non-interlaced.
- Python PNG: PNG image data, 3024 × 4032, 8-bit RGB, non-interlaced.
- Binwalk JPEG: JPEG image data, JFIF 1.02, 3024 × 4032, with Apple iPhone 13 Pro EXIF metadata.
- Foremost JPEG: JPEG image data, JFIF 1.02, 3024 × 4032, with Apple iPhone 13 Pro EXIF metadata.

The file identification results confirm that the candidates contain recognizable image-format headers. File identification alone does not establish that an image is complete or can be decoded successfully.

### 7.3 PNG Checksum Comparison

The Binwalk PNG candidate and Python-carved PNG were compared using MD5 and SHA-256.

**MD5**

| File                             | MD5                                  |
| -------------------------------- | ------------------------------------ |
| Binwalk PNG (`21C612A`)        | `24ee38f3c446f148eac489facf20ecf1` |
| Python PNG (`recovered_0.png`) | `24ee38f3c446f148eac489facf20ecf1` |

**SHA-256**

| File                             | SHA-256                                                              |
| -------------------------------- | -------------------------------------------------------------------- |
| Binwalk PNG (`21C612A`)        | `414fd63e64a810c453c0c46c4f14cc49233c2e15780bf67a0b68ee06f15ab838` |
| Python PNG (`recovered_0.png`) | `414fd63e64a810c453c0c46c4f14cc49233c2e15780bf67a0b68ee06f15ab838` |

**Finding:** Both checksum algorithms produced matching values. This establishes that the Binwalk and Python PNG outputs are byte-for-byte identical.

However, both PNG candidates failed to display during visual inspection. The matching checksums therefore demonstrate consistency between the two extraction outputs, not successful or complete PNG recovery.

The earlier signature analysis also found no complete PNG IEND sequence in the evidence image. The Python carving script consequently extracted from the PNG header to the end of the disk image.

### 7.4 JPEG Checksum and Binary Comparison

The Binwalk JPEG candidate and Foremost JPEG output were compared.

**MD5**

| File                             | MD5                                  |
| -------------------------------- | ------------------------------------ |
| Binwalk JPEG (`255F9EF`)       | `cc9116740a058bdccca628d1e6fe1f78` |
| Foremost JPEG (`00076540.jpg`) | `bfc40fd6b8adf2e7745d833de36b4bc0` |

**SHA-256**

| File                             | SHA-256                                                              |
| -------------------------------- | -------------------------------------------------------------------- |
| Binwalk JPEG (`255F9EF`)       | `e40e5cd7fc9ca673d2417accd86a189499133b3dfbead8b4f5ef3c5aad1e5ce2` |
| Foremost JPEG (`00076540.jpg`) | `c22411c0175a240ab2f96257d6babaa1c6068a3a653ed346ec86444dc8c146c9` |

The checksums differ because the two extracted files have different lengths:

| Candidate     |       Exact size |
| ------------- | ---------------: |
| Binwalk JPEG  | 13,239,825 bytes |
| Foremost JPEG | 10,626,782 bytes |

A further binary comparison established that the Foremost output is an exact prefix of the Binwalk output. The first 10,626,782 bytes are identical, while the Binwalk output contains an additional 2,613,043 bytes.

**Finding:** The different checksums do not indicate that the recovered JPEG contents disagree throughout. They reflect different extraction boundaries. Foremost extracted the JPEG through its detected end marker, while the Binwalk output continued beyond the Foremost file boundary.

Both JPEG candidates displayed successfully during visual inspection.

### 7.5 Visual Inspection

The four recovered candidates were downloaded from the forensic container to the Kali environment and opened for visual inspection.

| Candidate     | Visual inspection      |
| ------------- | ---------------------- |
| Binwalk PNG   | Failed to display      |
| Python PNG    | Failed to display      |
| Binwalk JPEG  | Displayed successfully |
| Foremost JPEG | Displayed successfully |

The JPEG outputs were visually viewable. The PNG outputs were not successfully displayed and are therefore documented as unsuccessful visual recoveries.

Visual inspection was used as an additional validation step alongside file identification and checksum comparison.

### 7.6 Overall Validation Findings

- The Binwalk and Python PNG candidates have matching MD5 and SHA-256 checksums but could not be displayed.
- The Binwalk and Foremost JPEG candidates have different checksums and file sizes.
- Binary comparison confirmed that the Foremost JPEG is an exact prefix of the larger Binwalk JPEG output.
- Both JPEG candidates displayed successfully.
- Binwalk also identified two TIFF data signatures, which were not independently validated as complete images.

These results distinguish between signature detection, data extraction, checksum consistency and successful visual recovery.

## 8. Screenshots and Evidence

The following screenshots document the examination and validation process.

| Screenshot                                    | Description                                                              |
| --------------------------------------------- | ------------------------------------------------------------------------ |
| `01-raw-disk-preliminary-examination.png`   | Initial raw disk examination using `file`, `fdisk` and `fls`       |
| `02-automated-file-recovery.png`            | Foremost and Binwalk automated recovery results                          |
| `03-png-signature-and-offset-analysis.png`  | PNG signature and offset analysis                                        |
| `04-python-png-carving.png`                 | Python-based PNG carving execution and output                            |
| `05-md5-and-sha256-checksum-comparison.png` | MD5 and SHA-256 comparisons for PNG and JPEG candidates                  |
| `06-recovery-transfer-validation.png`       | Local HTTP server and recovery-file transfer process                     |
| `07-recovered-file-identification.png`      | File identification results for recovered candidates                     |
| `08-binwalk-png-display-error.png`          | Failed visual inspection of the Binwalk PNG candidate                    |
| `09-python-png-display-error.png`           | Failed visual inspection of the Python PNG candidate                     |
| `10-jpeg-recovery-display.png`              | Successful visual inspection of the Binwalk and Foremost JPEG candidates |

## 9. Limitations

The examination identified several limitations:

1. The raw disk image did not expose a recognizable filesystem or partition structure through the preliminary checks.
2. The complete PNG IEND signature was not found during the signature search.
3. The PNG carving process therefore extracted data from the identified PNG header to the end of the evidence image.
4. Matching PNG checksums establish that two tools produced identical bytes, but do not establish that the resulting file is complete or valid.
5. Binwalk and Foremost used different extraction boundaries for the JPEG candidate, resulting in different file sizes and checksums.
6. The `file` utility identifies recognizable file signatures and metadata but does not replace full image decoding or visual validation.
7. The TIFF signatures detected by Binwalk were not independently examined to establish whether they represented complete standalone images.

## 10. Conclusion

This investigation applied raw disk forensic techniques to examine a 50 MiB disk image without relying on conventional filesystem metadata.

The examination used preliminary disk inspection, automated recovery with Foremost and Binwalk, manual file-signature and offset analysis, and a Python-based carving script.

The validation stage established that the Binwalk and Python PNG outputs were byte-for-byte identical, although neither could be displayed successfully. The two JPEG outputs had different extraction boundaries, with the Foremost output confirmed as an exact prefix of the Binwalk output. Both JPEG candidates displayed successfully.

The exercise demonstrates the importance of validating recovered data through multiple independent checks. Detecting a file signature, extracting bytes, obtaining matching checksums and successfully displaying a recovered file are distinct outcomes and should be reported separately.

**Investigation status:** Examination and recovery validation documented. PNG visual recovery unsuccessful; JPEG visual recovery successful
