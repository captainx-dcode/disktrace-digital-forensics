# Evidence Handling Notes

- Keep source disk images unchanged.
- Record the evidence filename and any available source hash.
- Perform analysis against the source image using read-only workflows where possible.
- Write recovered files to a separate output location.
- Record extraction commands, offsets, logical sizes, and hashes.
- Do not expose sensitive recovered content in public screenshots or commits.
- Do not interpret a file-type identification or matching extraction hashes as proof of authenticity or full integrity.
- Clearly label assumptions, inferred values, failed attempts, and limitations.
