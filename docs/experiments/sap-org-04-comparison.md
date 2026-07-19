# SAP-ORG-04 Baseline A/B Comparison

Status: repeat experiment complete; one-pilot descriptive comparison only

Date: 2026-07-19

## Result

Baseline B did **not** improve first-pass quality by the requested raw measures. It had 9 first-pass findings versus baseline A's 7, affected 9 records versus 5, and included one high factual error while baseline A had no high finding. The result must not be presented as first-pass improvement.

The mandatory process did demonstrate earlier defect containment. Baseline B's independent gate found every recorded defect before human review, preserved every revision and response, required three author revision cycles, and ended with 47 of 47 current source/claim artifacts verified and zero residual findings. No human approval was inferred.

## Descriptive measures

| Measure | Baseline A | Baseline B first pass | Baseline B closure |
|---|---:|---:|---:|
| Sources | 14 | 15 | 17 |
| Claims | 30 | 28 | 30 |
| Deterministic blocking findings | 0 | 0 | 0 |
| AI findings | 7 | 9 | 0 residual |
| Critical | 0 | 0 | 0 |
| High | 0 | 1 | 0 |
| Medium | 5 | 8 | 0 |
| Low | 2 | 0 | 0 |
| Factual error | 0 | 1 | 0 |
| Missing qualification | 2 | 2 | 0 |
| Unsupported recommendation | 0 | 0 | 0 |
| Insufficient premises | 1 | 2 | 0 |
| Taxonomy/classification error | 0 | 0 | 0 |
| Stale or weak source/support | 4 | 0 | 0 |
| Records needing revision | 5 | 9 | 0 |
| Author revision cycles | 0 recorded | 3 total | complete |
| Residual critical/high/medium | 5 | 9 | 0 |

The baseline-A stale/weak-source measure comprises three source-support mismatches and one weak locator. Baseline B's three first-pass structured scope-drift findings are not counted as source defects. `unsupported_recommendation` is the controlled category; neither baseline used it, while insufficient-premise findings are reported separately.

## Defect flow in baseline B

| Review stage | Findings | Severity | Outcome |
|---|---:|---|---|
| First independent verification | 9 | 1 high, 8 medium | Nine records revised. |
| Reverification after cycle 1 | 10 | 9 medium, 1 low | Ten findings addressed; all original nine confirmed resolved. |
| Full review after cycle 2 | 2 | 2 medium | Validator projection bug fixed; two OU evidence/dependency findings revised. |
| Closure after cycle 3 | 0 | none | 47 verified, 0 unresolved. |

There were 21 distinct logical findings. Thirty finding and 30 resolution records exist because the nine first-pass findings and resolutions were reproduced additively when correcting their target workspace-commit binding; this did not create nine new semantic defects. Metrics now report stored records, logical findings, exact duplicates, repeats on changed target digests, explicit supersessions, resolutions, and residuals separately.

Across the logical findings, severity is 1 high, 19 medium, and 1 low. Category is factual error 1, missing qualification 4, overbroad assertion 1, insufficient premises 5, scope drift 7, taxonomy/classification 2, and source mismatch 1. All 21 target claims. Stored resolutions are 26 accepted, 4 modified, and 0 disputed.

## Human-review burden

There is no measured reviewer-time dataset, so minutes or cost cannot be estimated honestly. A bounded burden proxy is:

- Baseline A would have presented 30 claims to humans with 5 blocking defects and 2 nonblocking notes still embedded.
- Baseline B presents 30 current claims and 17 sources with a complete verification trail and no known residual verification finding.
- Human reviewers must still independently inspect all artifacts, evidence, findings, and resolutions and may discover defects the AI passes missed.

No defect was caught only by a human because human approval was intentionally not run. This is not evidence that humans would find none.

## Model invocations and research capability

The baseline-A original author invocation count cannot be reconstructed from repository evidence. Preservation used one fresh independent advisory reconstruction invocation.

Baseline B used 12 observable worker turns: 6 in the continuing author context, 2 in the first-verifier context including metadata correction, 1 cycle-1 re-verifier, 2 in the cycle-2 verifier context including post-fix formalization, and 1 closure verifier. These represent 5 fresh isolated worker contexts: one author and four independent semantic verifier contexts. Coordinator turns are excluded. Exact provider invocation IDs were unavailable.

Research-capable author/verifier contexts used public web access limited to official AWS material. Mechanical freeze, resolution-link, validation, and formal-binding turns used repository-local operations. The deterministic core itself performed no web search and gained no network dependency.

## Interpretation limits

This is one repeated pilot with different artifact counts, authoring choices, verifier contexts, and a validator fix during the experiment. It has no statistical power and does not establish a model-quality effect. It shows that generalized author instructions alone did not improve this first pass, while a fail-closed independent verification/revision loop contained the observed defects before human review.
