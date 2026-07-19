# SAP-ORG-04 Experiment Baseline A

Status: frozen original-process baseline; independent advisory findings recorded; no approval

Baseline workspace commit: `c80962c3e0689e3e07e45e0852c238715635e2ec`

Original lifecycle: `authoring → deterministic validation → pending human review`

## Reproducibility boundary

Baseline A is the exact source/claim workspace committed at the baseline commit. Its project digest is `5330a4a157b91913dfd2d2793fe80294bb46bf6c93078fceea3e3e9253506afc`; its zero-structural-finding validation report digest is `759126e3f5a802337adb797039b415105f1efde9330240bc8b53b2b905efb37e`. The [machine manifest](../../authoring/experiments/sap-org-04/baseline-a/manifest.json) enumerates all 14 source and 30 claim digests. None of those records is rewritten by this experiment.

The original completed advisory report was not present as a repository or attachment artifact. To avoid fabricating its bytes or digest, this task ran a new fresh independent advisory invocation over the exact frozen baseline and all current official sources. This document is that reproducible replacement evidence; its repository-byte SHA-256 is recorded in the machine manifest. It is not retroactive verification in the baseline-A lifecycle and grants no approval.

## Counts

- Sources: 14; all independently verified as current official AWS records.
- Claims: 30 (20 documented facts, 3 service limitations, 7 derived recommendations).
- Deterministic findings: 0.
- Independent advisory findings: 7 total—5 medium and 2 low.
- Categories: 3 source mismatch, 1 weak locator, 1 insufficient premises, and 2 missing qualification. One Control Tower finding involves both source mismatch and missing qualification but is counted once under its primary category for experiment metrics.
- Initial dispositions: 23 `verified`, 2 `verified_with_nonblocking_note`, 5 `revision_required`, 0 `blocked`, 0 `unable_to_verify`.

## Material findings

| ID | Target | Category / severity | Finding | Required action | Downstream effect |
|---|---|---|---|---|---|
| A-F01 | `clm-control-tower-control-mechanisms` | source mismatch + missing qualification / medium | The overview does not precisely support all effects; proactive controls apply to supported resources created or updated through CloudFormation stack operations, not every creation path. | Add the exact “How controls work” source/locator and CloudFormation qualification. | `clm-rec-distinguish-control-roles` depends on the corrected premise. |
| A-F02 | `clm-ou-hierarchy-controls` | weak locator / medium | The statement is supported, but the recorded “Benefits of using OUs” locator does not establish nesting. | Use the official AWS Organizations “Organizational units” section locator. | `clm-rec-control-aligned-ous` depends on this premise. |
| A-F03 | `clm-permission-set-account-roles` | source mismatch / medium | The registered account-access page does not precisely support IAM-role provisioning from permission sets. | Add the official permission-set concepts page and opening definition. | `clm-rec-pair-workforce-grants-and-scps` depends on the corrected premise. |
| A-F04 | `clm-ram-consumer-permission-boundary` | source mismatch / medium | The getting-started page supports consumer permissions but not retained ownership with the needed precision. | Add the official RAM overview ownership/consumer sections or narrow the statement. | `clm-rec-share-eligible-resources` depends on this premise. |
| A-F05 | `clm-rec-distinguish-control-roles` | insufficient premises / medium | Its GuardDuty premise establishes Regional administration, not GuardDuty’s threat-detection role. | Add an atomic GuardDuty detection/finding premise or remove that role from the recommendation. | The recommendation itself and later lesson/question dependencies remain blocked. |
| A-F06 | `clm-scp-effective-permission-intersection` | missing qualification / low, nonblocking | Current AWS wording also identifies RCPs in the complete effective-permission intersection. The bounded SCP statement remains true. | Name RCPs before using the claim to teach complete permission evaluation. | No immediate block; downstream full-policy explanations need the note. |
| A-F07 | `clm-ram-organization-sharing` | missing qualification / low, nonblocking | When the owner account is included in an organization/OU share, principals in that sharing account can receive access bounded by the managed permission. | Add an applicability/exclusion note before scenario use. | No immediate block; downstream RAM scenarios need the qualification. |

Official evidence used includes [Control Tower control behavior](https://docs.aws.amazon.com/controltower/latest/userguide/how-controls-work.html), [AWS Organizations and OUs](https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/aws-organizations.html), [IAM Identity Center permission sets](https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsetsconcept.html), [AWS RAM overview](https://docs.aws.amazon.com/ram/latest/userguide/what-is.html), [SCP behavior](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html), and [RAM organization sharing](https://docs.aws.amazon.com/ram/latest/userguide/getting-started-sharing.html).

## Claim-by-claim initial dispositions

| Disposition | Claims |
|---|---|
| `revision_required` | `clm-control-tower-control-mechanisms`; `clm-ou-hierarchy-controls`; `clm-permission-set-account-roles`; `clm-ram-consumer-permission-boundary`; `clm-rec-distinguish-control-roles` |
| `verified_with_nonblocking_note` | `clm-scp-effective-permission-intersection`; `clm-ram-organization-sharing` |
| `verified` | `clm-account-isolation-boundary`; `clm-cloudtrail-member-protection`; `clm-cloudtrail-organization-coverage`; `clm-config-aggregator-read-only`; `clm-guardduty-regional-administration`; `clm-identity-center-central-workforce-access`; `clm-management-account-workload-boundary`; `clm-ou-control-based-organization`; `clm-ram-regional-sharing`; `clm-rec-control-aligned-ous`; `clm-rec-delegate-central-services`; `clm-rec-pair-workforce-grants-and-scps`; `clm-rec-separate-audit-ownership`; `clm-rec-separate-workload-accounts`; `clm-rec-share-eligible-resources`; `clm-scp-does-not-grant`; `clm-scp-hierarchical-inheritance`; `clm-scp-management-account-exception`; `clm-scp-maximum-permissions`; `clm-scp-staged-testing`; `clm-security-hub-central-configuration`; `clm-service-delegated-administrator`; `clm-workforce-temporary-credentials` |

## Source dispositions

All 14 source records were `verified` as public first-party AWS pages. The Control Tower overview, Identity Center account-access page, and RAM sharing page remain valid source records but are insufficient alone for the affected full claim statements; the defect belongs to claim evidence selection rather than source identity.

## Interpretation

Baseline A demonstrates that a zero-finding structural report did not contain semantic defects before human review. The five revision-required claims would have reached the human queue under the old process. This baseline therefore supports the proposed independent-verification gate without claiming statistical significance.
