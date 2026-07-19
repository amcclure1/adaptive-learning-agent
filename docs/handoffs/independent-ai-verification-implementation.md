# Independent AI Verification Implementation Handoff

Status: generic implementation complete; ADR 0021 Proposed; experiment in progress

Date: 2026-07-19

## Implemented boundary

The runtime-independent `adaptive_learning.authoring` package now implements closed and canonically digested `ai_verification_run`, `verification_finding`, and `finding_resolution` records. The workspace adds confined `verifications/runs`, `findings`, `resolutions`, and `metrics` directories.

Eight closed `AuthoringOperations` methods cover run creation, independently consulted-source registration, finding creation, finalization, current eligibility, resolution creation, run comparison, and experiment metrics. These methods perform no research themselves and expose no shell, unrestricted filesystem, unrestricted network, approval, compilation, installation, activation, publication, or release capability.

## Fail-closed behavior

- A run requires a passing deterministic report covering every exact target digest.
- A target author cannot act as its independent verifier.
- Finalization requires exactly one disposition for every target and exact finding linkage.
- Blocking findings cannot coexist with a verified disposition.
- A changed target digest has no current verification eligibility.
- Critical/high/medium open or disputed findings block; low/informational findings require explicit nonblocking treatment.
- Derived claim approval additionally requires verified and approved exact premises.
- Human approval/review creation is blocked without eligible current verification.
- The AI verifier identity cannot be recorded as the human approver.
- Verification and resolution results always declare or imply no approval.

Historical approvals and released packs are not rewritten. The gate applies through authored-content operations for new decisions. SQLite schema 1, the ten learner operations, scoring, pack formats, Hermes, and MCP remain unchanged.

## Tests

Twelve new generic tests cover closed schemas, JSON serialization, exact binding, stale verification, blocking and nonblocking findings, revision invalidation, resolution linkage, disputed findings, absent-verification approval rejection, verifier/approver conflict, comparison metrics, bounded offline source registration, SQLite schema 1, ten learner operations, and absence of Hermes/MCP/network dependencies. Existing authoring fixtures now carry synthetic independent verification evidence before synthetic human decisions.

The implementation does not assert factual correctness. Research-capable agents operate outside the deterministic module and submit inspected evidence through the bounded records.
