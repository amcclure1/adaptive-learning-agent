# SAP-ORG-04 Experiment Baseline B

Status: independent verification complete; stopped before human approval

Date: 2026-07-19

## Independence and reproducibility

Baseline B was authored in the separate `authoring/aws-sap-c02-org-04-baseline-b/` workspace by a fresh author invocation that received the accepted architecture, fixed pilot scope, schemas, and generalized quality policy. It did not receive baseline A, its defect list, corrected wording, claim-specific hints, or review report before its first pass.

The first authored commit is `4be13e760337bab63221f881c313804bbb1d202e`. Commit `926134a49e8894be7bf9eef06f93a3bb486ec326` fixed its exact first-pass target as 15 source revision-1 records and 28 claim revision-1 records. The passing deterministic report digest was `ba5a312a31550b7b18ca5a0aedd543efa523b0fde81ded24218195c8350d63f2`.

The first verifier was a separate fresh invocation with no baseline-A material or hidden author reasoning. Its first formal run accidentally named the pre-freeze author commit. The immutable evidence was preserved, and an additive corrected run bound the same exact targets to `926134a49e8894be7bf9eef06f93a3bb486ec326`. The corrected run digest is `6c8a411b2ed7997bb4e05831a48c60b0e08b754c57de5bf1f2ba840386d97631`. This correction did not repeat or alter the semantic review.

Exact deployed model snapshots, provider invocation identifiers, temperatures, seeds, system fingerprints, and reasoning settings were not exposed by the host and cannot be verified. Research used freshly opened public official AWS documentation. No AWS account, private source, exam dump, MCP capability, or agent memory was used as authority.

## First-pass result

- Sources: 15; all verified.
- Claims: 28: 17 documented facts, 6 service limitations, and 5 derived recommendations.
- Deterministic findings: 0.
- Independent findings: 9 blocking: 1 high and 8 medium.
- Dispositions: 34 verified and 9 revision required across 43 targets.
- First-pass verification finding categories: 1 factual error, 2 missing qualifications, 1 overbroad assertion, 2 insufficient-premise findings, and 3 scope-drift findings.

| Target | Category / severity | Required correction |
|---|---|---|
| `clm-b-scp-parent-chain` | factual error / high | Separate allow-at-every-hierarchy-level behavior from explicit-deny behavior and bound the other applicable policy types. |
| `clm-b-ram-principals` | missing qualification / medium | Add the conditional AWS Organizations, all-features, and RAM service-linked-role prerequisites. |
| `clm-b-securityhub-central-authority` | overbroad assertion / medium | Limit delegated-administrator authority to settings governed by central configuration policies. |
| `clm-b-securityhub-region-unit` | missing qualification / medium | Add the global-resource-control exception and opt-in Region condition. |
| `clm-b-rec-control-aligned-ous` | insufficient premises / medium | Add exact atomic premises for control-aligned grouping and restrained OU hierarchy. |
| `clm-b-rec-isolate-management` | insufficient premises / medium | Add an atomic premise for management-account resource/workload isolation guidance. |
| `clm-b-rec-complement-config-securityhub` | scope drift / medium | Include AWS Config and Security Hub CSPM in structured service scope. |
| `clm-b-rec-org-trail` | scope drift / medium | Include AWS CloudTrail in structured service scope. |
| `clm-b-rec-pair-access-guardrail` | scope drift / medium | Include AWS IAM Identity Center in structured service scope. |

## Revision and reverification history

### Cycle 1

Commit `b9b8ffb03d49f3c36acbd84fbcc8b699ce926339` preserved all first-pass records, revised nine claims, added one official SCP-evaluation source and two atomic premise claims, and created nine logical finding responses. The additive binding correction caused the same nine logical findings to have nine additional formally linked resolution records. There were no disputes.

Fresh full reverification run `verify-baseline-b-reverification-20260719`, digest `8a5e4e67cbe2de4e65b1d3d44b1734f04071e33d66efb076863205a8d780a627`, confirmed all nine first-pass defects resolved but found 10 new issues: 9 medium blocking and 1 low nonblocking. Categories were 2 missing qualifications, 2 insufficient premises, 4 scope drift, and 2 taxonomy/classification errors.

### Cycle 2

Commit `8b199f13268d173b4a0c026145f5cea6975f1d4b` addressed all 10 findings. It added one official Config source and one atomic Config premise, explicitly superseded a redundant CloudTrail caveat while preserving its history, and retained 30 current claims.

A fresh full review found a generic validator defect: historical superseded claims were still counted and freshness-checked as current. Commit `71dc7f009d94170f5342cb1de8770d79f1ce9acb` corrected the current-revision projection and added regression coverage. The same completed verifier then formalized two medium findings in run `verify-baseline-b-cycle-two-20260719`, digest `9f202f1d0dea52dca9531157bdc18c8981fa4d04a8bcc579149bdb9b52a3379f`: an OU troubleshooting source mismatch and its dependent recommendation-premise defect.

### Cycle 3 and closure

Commit `db33fc3fb0f8d22de2b8bd74d74881e2ada1f773` revised the OU guidance to the exact official OU-practices locator, rebound its recommendation to the new premise digest, and added two immutable resolution records.

The final fresh closure run `verify-baseline-b-closure-20260719` reviewed all 47 current targets and reopened all 17 official URLs. Its digest is `d60215c5ac92b8b5d9a55738d0aa9fc7215dbdd2061305265e02a9db559aab99`. Its deterministic report digest is `6b6323aca08d1ed9002c49bc4de9c7b4464d878dc6dd0b5531b55aee548f9edb`.

- Sources: 17 verified.
- Claims: 30 verified: 19 documented facts, 6 service limitations, and 5 derived recommendations.
- Final dispositions: 47 verified; 0 other dispositions.
- Residual findings: 0 at every severity.
- Unresolved questions: 0.
- Verification eligibility: 47 of 47.
- Historical logical findings: 21; all resolved after three author revision cycles.
- Stored finding/resolution records: 30 because the nine first-pass findings were additively duplicated to correct their commit binding; 26 responses are accepted and 4 modified, with none disputed.

## Stop state

Independent verification is evidence, not approval. All human source and claim approvals remain pending. The 97 nonblocking diagnostics in the final deterministic report are expected approval-pending notices. No lesson, question specification, learner-ready question, pack, installation, activation, publication, release, or tag was created.
