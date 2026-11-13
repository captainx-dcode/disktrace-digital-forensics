# Reporting Standard

## Report structure

1. Case details and report control
2. Executive summary
3. Authority, scope, and objectives
4. Evidence received and evidence integrity
5. Tools and examination environment
6. Methodology and procedures
7. Findings
8. Recovery results and validation
9. Timeline (only where supported)
10. Limitations and alternative explanations
11. Conclusion
12. Appendices: hashes, command log, tool output references, screenshots

## Finding format

Each finding should include:

- **Finding ID**
- **Statement:** concise and factual.
- **Classification:** confirmed observation, interpretation, or unresolved hypothesis.
- **Evidence references:** exhibit ID and output/artifact reference.
- **Method:** how the observation was obtained.
- **Impact / relevance:** why it matters to the investigation.
- **Limitations:** what the evidence does not establish.
- **Examiner note:** follow-up or corroboration needed.

## Language rules

Prefer:
- “The examination identified…”
- “The tool output indicates…”
- “The file was recovered and validated by…”
- “The available evidence does not establish…”

Avoid unsupported statements such as:
- “The suspect deleted…”
- “The employee intentionally concealed…”
- “The file is authentic…” unless authenticity is independently established.

## Quality review

Before release, verify:
- Every factual claim has an evidence reference.
- Hashes and IDs match the registers.
- Dates, time zones, units, and offsets are explicit.
- Confirmed facts are separated from interpretations.
- Recovery status is accurately represented.
- Limitations are visible, not buried.
