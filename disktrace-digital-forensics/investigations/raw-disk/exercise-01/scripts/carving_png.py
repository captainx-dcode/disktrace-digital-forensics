#!/usr/bin/env python3

import hashlib
from pathlib import Path

IMAGE_PATH = Path("corrupted_drive.dd")
OUTPUT_DIR = Path("M2_TL_recovered_files")

PNG_HEADER = bytes.fromhex("89 50 4E 47 0D 0A 1A 0A")
PNG_FOOTER = bytes.fromhex("49 45 4E 44 AE 42 60 82")


def find_signatures(data, signature):
    """Return every byte offset at which a signature occurs."""
    offsets = []
    position = 0

    while True:
        position = data.find(signature, position)

        if position == -1:
            break

        offsets.append(position)
        position += 1

    return offsets


def calculate_sha256(data):
    """Calculate the SHA-256 hash of extracted data."""
    return hashlib.sha256(data).hexdigest()


def carve_png(data, start_offset, end_offset, output_path):
    """Write the selected byte range to an output file."""
    recovered_data = data[start_offset:end_offset]

    with output_path.open("xb") as output_file:
        output_file.write(recovered_data)

    return recovered_data


def main():
    if not IMAGE_PATH.is_file():
        print(f"[ERROR] Evidence image not found: {IMAGE_PATH}")
        return

    image_data = IMAGE_PATH.read_bytes()
    image_size = len(image_data)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    start_offsets = find_signatures(image_data, PNG_HEADER)
    end_offsets = find_signatures(image_data, PNG_FOOTER)

    print("=== PNG CARVING REPORT ===")
    print(f"Evidence image: {IMAGE_PATH}")
    print(f"Image size: {image_size} bytes")
    print(f"PNG headers found: {len(start_offsets)}")
    print(f"Complete IEND signatures found: {len(end_offsets)}")

    if not start_offsets:
        print("[RESULT] No PNG headers found. Carving cannot proceed.")
        return

    print("\n=== RECOVERY RESULTS ===")

    for index, start_offset in enumerate(start_offsets):
        # Find the first footer that occurs after this header.
        matching_footers = [
            offset for offset in end_offsets
            if offset >= start_offset + len(PNG_HEADER)
        ]

        if matching_footers:
            footer_offset = matching_footers[0]
            end_offset = footer_offset + len(PNG_FOOTER)
            recovery_method = "Complete IEND signature found"
        else:
            end_offset = image_size
            recovery_method = "No IEND signature found; carved to end of image"

        output_path = OUTPUT_DIR / f"recovered_{index}.png"

        if output_path.exists():
            print(f"\n[SKIPPED] {output_path} already exists.")
            print("Rename or move the existing file before retrying.")
            continue

        recovered_data = carve_png(
            image_data,
            start_offset,
            end_offset,
            output_path
        )

        print(f"\nFile: {output_path}")
        print(f"Start offset: {start_offset} ({hex(start_offset)})")
        print(f"End offset (exclusive): {end_offset} ({hex(end_offset)})")
        print(f"Recovery method: {recovery_method}")
        print(f"Extracted size: {len(recovered_data)} bytes")
        print(f"SHA-256: {calculate_sha256(recovered_data)}")

    print("\n=== CARVING COMPLETE ===")


if __name__ == "__main__":
    main()
