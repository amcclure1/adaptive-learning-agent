# SAP-ORG-04 Authoring and Verification Experiment Audit

Status: complete; descriptive one-pilot audit

Date: 2026-07-19

## Integrity findings

Baseline A is the frozen original 14-source/30-claim workspace at commit `c80962c3e0689e3e07e45e0852c238715635e2ec`. It had no deterministic blocking finding and seven reconstructed advisory findings: five medium, two low; five revision-required artifacts and two verified-with-note artifacts. The original advisory run was not preserved as structured evidence, so this fresh reconstruction is a material comparison threat.

Baseline B used a separate author context that was not shown baseline-A defects. Its exact first pass was frozen before verification, then reviewed by fresh verifier contexts. It began with 15 sources, 28 claims, and nine blocking findings (one high, eight medium). Reverification found ten records after cycle one, two after cycle two, and zero at closure. The final set contains 17 sources and 30 claims. Three author revision cycles, five observable isolated worker contexts, and twelve worker turns are documented. No human approval occurred.

## Finding reconciliation

Baseline B has 30 stored finding records but 21 logical findings. Nine first-pass findings were copied additively with new IDs solely to correct target workspace-commit binding; their originals were preserved. The same nine corrections produced nine additive resolution copies. Therefore:

| Measure | Count |
|---|---:|
| Stored finding records | 30 |
| Logical findings | 21 |
| Exact binding-correction duplicates | 9 |
| Stored resolutions | 30 |
| Accepted responses | 26 |
| Modified responses | 4 |
| Disputed responses | 0 |
| Residual findings at closure | 0 |

Logical severity is one high, nineteen medium, and one low. Logical categories are factual error 1, missing qualification 4, overbroad assertion 1, insufficient premises 5, scope drift 7, taxonomy/classification 2, and source mismatch 1. All 21 targeted claims. Stored counts include the nine correction copies and must not be reported as 30 defects.

## Evaluation

First-pass quality: **does not pass an improvement claim**. Baseline B had more first-pass findings and affected artifacts and introduced a high factual error. The generalized protocol did not demonstrate better drafting.

Containment: **passes for recorded findings**. Every recorded material finding was revised or otherwise resolved and independently rechecked before the human gate; closure had zero residual findings. This does not prove that all latent errors were discovered.

Process integrity: **qualified pass**. Artifact freezing, exact references, immutable revisions, author/verifier role separation, and resolution trails are present. The binding correction is transparent and non-destructive, but exposes why metrics need semantic deduplication. The validator was repaired during the experiment, and the author retained context across its own revision turns.

## Validity threats and unverifiable claims

- One pilot with different artifact counts and author choices has no statistical power.
- Baseline A's advisory evidence was reconstructed; reviewer equivalence is not established.
- Fresh invocation establishes context separation, not different weights/provider or statistical independence.
- Exact provider/model metadata and orchestration independence were unavailable and cannot be verified.
- Author and verifier may share correlated model-family errors.
- A validator projection defect was discovered and fixed mid-experiment.
- No qualified human ground truth has yet measured false negatives, review time, or final factual quality.
- Zero residual recorded findings is not a guarantee of correctness.

## Gate decision

Accept ADR 0021 with the added normative author self-audit and corrected metrics. Do not retroactively manufacture self-audits for frozen baselines. Before lessons or questions, the current source/claim set must receive exact-digest self-audits under the accepted protocol, pass current deterministic validation and independent verification, and receive separately authorized qualified human approvals. That gate is not currently satisfied.
