
# FAT32 Forensics Investigation

**Investigation:** 002 – FAT32 Disk Image Examination
**Status:** In Progress
**Evidence image:** `fat32_forensic.dd`

## 1. Investigation Scope

This investigation examines a supplied FAT32 disk image to identify deleted files, inspect their filesystem metadata, recover their contents, and compare the results obtained using two recovery methods.

The investigation uses The Sleuth Kit (TSK), including `fls`, `istat`, and `icat`, alongside a Python-based file carving script.

## 2. Investigation Tasks

### Task 1: Prepare the Forensics Environment

The investigation was conducted inside the provided Docker-based forensics environment.

**Environment verification:**

```bash
whoami
id
pwd
```

The commands confirmed that the investigation was running as `root` in `/home/student/Forensics`.

The evidence image `fat32_forensic.dd` was available in the working directory.

### Task 2: Identify the Filesystem

The following commands were used to identify the filesystem and inspect its metadata:

```bash
file fat32_forensic.dd
fsstat fat32_forensic.dd
```

**Findings:**

- Filesystem: FAT32
- Sector size: 512 bytes
- Cluster size: 512 bytes
- Root directory cluster: 2
- FAT copies: 2
- Volume ID: `0xa742e8f9`
- Volume label: `NO NAME`

The filesystem begins at sector 0, as indicated by the `fsstat` output.

### Task 3: Locate Deleted Files

The following command was used to recursively list filesystem entries:

```bash
fls -r fat32_forensic.dd
```

**Relevant output:**

```text
r/r * 4:        IMG_2019.jpg
r/r * 6:        IMG_0117.png
```

The asterisk (`*`) indicates that the entries are deleted or not allocated.

Two deleted image entries were identified:

| Directory Entry | Filename         |
| --------------- | ---------------- |
| 4               | `IMG_2019.jpg` |
| 6               | `IMG_0117.png` |

### Task 4: Examine Metadata – IMG_2019.jpg

The following command was used:

```bash
istat fat32_forensic.dd 4
```

**Findings:**

- Directory entry: 4
- Allocation status: Not Allocated
- File attributes: File, Archive
- Size: 3,190,011 bytes
- Filename reported by `istat`: `_MG_2019.JPG`
- Written: 2036-01-01 07:59:58 UTC
- Accessed: 2025-03-07 00:00:00 UTC
- Created: 2025-03-07 22:08:29 UTC
- Sector range: 32990–39220

**Observation:** The filename reported by `istat` differs from the name displayed by `fls`. The Written timestamp is also later than the Created timestamp. These discrepancies are documented as observed; their causes have not been established.

### Task 5: Examine Metadata – IMG_0117.png

The following command was used:

```bash
istat fat32_forensic.dd 6
```

**Findings:**

- Directory entry: 6
- Allocation status: Not Allocated
- File attributes: File, Archive
- Size: 12,876,314 bytes
- Filename reported by `istat`: `_MG_0117.PNG`
- Written: 2025-03-07 22:09:00 UTC
- Accessed: 2025-03-07 00:00:00 UTC
- Created: 2025-03-07 22:09:01 UTC
- Sector range: 39221–64370

**Observation:** The filename reported by `istat` differs from the name displayed by `fls`. The Written timestamp precedes the Created timestamp by one second.

### Task 6: Recover the Deleted Images

Two recovery approaches were used to recover the identified image files.

**Method 1: Recovery using `icat`**

```bash
icat fat32_forensic.dd 4 > icat_IMG_2019.JPG
icat fat32_forensic.dd 6 > icat_IMG_0117.png
```

This method used the identified filesystem directory entries to extract the file contents.

**Method 2: Recovery using the Python carving script**

The Python script `file_carver.py` was used to extract image data from specified byte offsets.

The offsets were supplied through `offset.txt`:

```text
101bc00,13268fb,python_IMG_2019.JPG
1326a00,1f6e41a,python_IMG_0117.png
```

The script was executed in batch mode:

```bash
python3 file_carver.py
```

**Recovered output files:**

| Recovery method | IMG_2019                | IMG_0117                |
| --------------- | ----------------------- | ----------------------- |
| `icat`        | `icat_IMG_2019.JPG`   | `icat_IMG_0117.png`   |
| Python          | `python_IMG_2019.JPG` | `python_IMG_0117.png` |

Separate filenames were maintained for each recovery method to prevent one output from overwriting another.

### Task 7: Verify Recovery Results Using MD5

MD5 checksums were calculated to compare the files recovered using `icat` against those recovered using the Python script.

**IMG_2019.jpg:**

```bash
md5sum icat_IMG_2019.JPG python_IMG_2019.JPG
```

Output:

```text
b3ab520fa902f0f21d3e77d399aabde2  icat_IMG_2019.JPG
b3ab520fa902f0f21d3e77d399aabde2  python_IMG_2019.JPG
```

**IMG_0117.png:**

```bash
md5sum icat_IMG_0117.png python_IMG_0117.png
```

Output:

```text
5759303ec45a944b853f36a5084757f6  icat_IMG_0117.png
5759303ec45a944b853f36a5084757f6  python_IMG_0117.png
```

**Verification result:**

Both pairs produced matching MD5 checksums. This indicates that the files recovered through `icat` and the Python script are byte-for-byte identical for each image.

This comparison establishes agreement between the two recovery methods. It does not independently establish that the recovered files are identical to the original pre-deletion files, as no separate original reference copies were available for comparison.

## 3. Consolidated Findings

The investigation established the following:

1. The supplied disk image uses the FAT32 filesystem.
2. Two deleted image entries were identified using `fls`.
3. Their allocation status, sizes, timestamps, filenames, and sector ranges were examined using `istat`.
4. Both images were extracted using `icat`.
5. Both images were independently extracted using a Python-based carving script.
6. MD5 comparisons showed matching checksums between the two recovery methods for each image.

## 4. Investigation Screenshots

Screenshots are intended to document the execution and results of the investigation tasks.

| Screenshot                                 | Description                                                             |
| ------------------------------------------ | ----------------------------------------------------------------------- |
| `01-fat32-environment.png`               | Forensics environment and evidence image verification                   |
| `02-fat32-filesystem-identification.png` | Filesystem identification and metadata                                  |
| `03-fat32-deleted-file-listing.png`      | Deleted image entries identified using `fls`                          |
| `04-fat32-img-2019-metadata.png`         | Metadata examination of directory entry 4                               |
| `05-fat32-img-0117-metadata.png`         | Metadata examination of directory entry 6                               |
| `06-fat32-recovery-and-verification.png` | Recovery using `icat` and Python, followed by MD5 checksum comparison |

## 5. Investigation Status

The FAT32 investigation has completed deleted-file identification, metadata examination, image recovery using two methods, and MD5 comparison.

Further examination and documentation may be added as the investigation progresses.
