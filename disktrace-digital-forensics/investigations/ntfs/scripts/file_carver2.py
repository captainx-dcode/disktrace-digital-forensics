#!/usr/bin/env python3
"""
DiskTrace - File Carver
Extracts a byte range from a forensic image using hexadecimal offsets.

The source image is opened read-only. The end offset is exclusive:
the number of bytes extracted is end_offset - start_offset.
"""

import hashlib
import os
import sys
from pathlib import Path


CHUNK_SIZE = 1024 * 1024  # Copy in 1 MiB chunks.


def parse_hex_offset(value: str, label: str) -> int:
    """Convert a hexadecimal offset (with or without 0x prefix) to an integer."""
    cleaned = value.strip().lower()
    if cleaned.startswith("0x"):
        cleaned = cleaned[2:]
    if not cleaned:
        raise ValueError(f"{label} cannot be empty.")
    try:
        return int(cleaned, 16)
    except ValueError as exc:
        raise ValueError(
            f"{label} must be a hexadecimal value, for example 1B00000."
        ) from exc


def sha256_file(path: Path) -> str:
    """Calculate SHA-256 without loading the whole file into memory."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def extract_file(image_path: Path, start_hex: str, end_hex: str,
                 output_path: Path, overwrite: bool = False) -> bool:
    """Extract [start_offset, end_offset) from an image into a separate file."""
    try:
        start = parse_hex_offset(start_hex, "Start offset")
        end = parse_hex_offset(end_hex, "End offset")

        if start < 0 or end <= start:
            raise ValueError("End offset must be greater than the start offset.")

        image_path = image_path.expanduser().resolve()
        output_path = output_path.expanduser().resolve()

        if not image_path.is_file():
            raise FileNotFoundError(f"Forensic image not found: {image_path}")
        if image_path == output_path:
            raise ValueError("Output file must not be the forensic image itself.")
        if output_path.exists() and not overwrite:
            answer = input(
                f"'{output_path}' already exists. Overwrite it? (y/N): "
            ).strip().lower()
            if answer != "y":
                print("Skipped: existing output was not changed.")
                return False

        image_size = image_path.stat().st_size
        if end > image_size:
            raise ValueError(
                f"End offset ({end:#x}) exceeds image size ({image_size:#x})."
            )

        bytes_to_copy = end - start
        output_path.parent.mkdir(parents=True, exist_ok=True)

        remaining = bytes_to_copy
        with image_path.open("rb") as source, output_path.open("wb") as target:
            source.seek(start)
            while remaining:
                chunk = source.read(min(CHUNK_SIZE, remaining))
                if not chunk:
                    raise IOError("Unexpected end of image while reading the range.")
                target.write(chunk)
                remaining -= len(chunk)

        actual_size = output_path.stat().st_size
        if actual_size != bytes_to_copy:
            raise IOError(
                f"Size verification failed: expected {bytes_to_copy} bytes, "
                f"wrote {actual_size} bytes."
            )

        print("\n[+] Extraction completed")
        print(f"    Source image : {image_path}")
        print(f"    Start offset : 0x{start:X}")
        print(f"    End offset   : 0x{end:X} (exclusive)")
        print(f"    Bytes copied : {actual_size:,}")
        print(f"    Output file  : {output_path}")
        print(f"    SHA-256      : {sha256_file(output_path)}")
        return True

    except (OSError, ValueError) as exc:
        print(f"[!] Extraction failed: {exc}")
        return False


def process_offsets_file(image_path: Path, offsets_path: Path) -> None:
    """Process CSV-like rows: start_hex,end_hex,output_filename."""
    offsets_path = offsets_path.expanduser()
    if not offsets_path.is_file():
        print(f"[!] Offsets file not found: {offsets_path}")
        return

    successes = 0
    failures = 0

    with offsets_path.open("r", encoding="utf-8") as offsets:
        for line_number, raw_line in enumerate(offsets, start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            fields = [field.strip() for field in line.split(",")]
            if len(fields) != 3 or not all(fields):
                print(f"[!] Line {line_number}: expected start,end,output; skipped.")
                failures += 1
                continue

            start_hex, end_hex, output_name = fields
            if extract_file(image_path, start_hex, end_hex, Path(output_name)):
                successes += 1
            else:
                failures += 1

    print(f"\nBatch finished: {successes} successful, {failures} skipped/failed.")


def main() -> int:
    print("\n=== DiskTrace File Carver ===")
    print("The forensic image will be opened read-only.")
    image_input = input(
        "Forensic image path [forensic_image.dd]: "
    ).strip() or "forensic_image.dd"
    image_path = Path(image_input).expanduser()

    if not image_path.is_file():
        print(f"[!] Image file not found: {image_path}")
        return 1

    mode = input("Batch mode using offsets.txt? (y/n) [n]: ").strip().lower()
    if mode == "y":
        offsets_input = input("Offsets file [offsets.txt]: ").strip() or "offsets.txt"
        process_offsets_file(image_path, Path(offsets_input))
        return 0

    start_hex = input("Start offset in hexadecimal (e.g. 1B00000): ").strip()
    end_hex = input("End offset in hexadecimal (e.g. 25226DE): ").strip()
    output_input = input("Output filename [carved.jpg]: ").strip() or "carved.jpg"

    return 0 if extract_file(
        image_path, start_hex, end_hex, Path(output_input)
    ) else 1


if __name__ == "__main__":
    sys.exit(main())
