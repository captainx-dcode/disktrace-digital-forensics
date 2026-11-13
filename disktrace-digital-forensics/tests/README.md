# Test Plan — Initial

Tests will be expanded during Phase 5.

| Test ID | Component | Test | Expected result |
|---|---|---|---|
| T-001 | Evidence hashing | Hash the same unchanged file twice | Identical SHA-256 values |
| T-002 | Evidence hashing | Supply a missing path | Clear failure; no false manifest record |
| T-003 | Event logger | Append two events | Second event references first event hash |
| T-004 | Event logger | Modify a prior event manually | Hash-chain verification should detect mismatch once verifier is implemented |
| T-005 | Recovery validation | Validate an empty file | Non-empty check is false; no success claim |
| T-006 | Recovery validation | Validate a normal file | Hash and basic metadata recorded |
| T-007 | Report | Trace each finding to evidence | No unsupported finding remains |

A hash-chain verifier and automated schema validation are planned enhancements; the initial event logger only writes linked events.
