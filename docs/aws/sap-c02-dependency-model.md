# SAP-C02 Objective Dependency Model

Status: accepted 0.3A dependency baseline

Architecture: `aws-sap-c02-learning-architecture` version `0.3A.1`

Dependencies represent competency, not mandatory lesson order. The official guide groups outcomes by exam domain; this model adds cross-domain prerequisites required for coherent architectural reasoning. [Official domains and tasks](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-professional-02/solutions-architect-professional-02.html)

## Categories

- **Blocking prerequisite:** target performance is incoherent or unsafe without it.
- **Bridge prerequisite:** a bounded subset can be taught and checked concisely.
- **Recommended context:** improves depth/transfer but may be omitted with a visible warning.
- **Independent:** no prerequisite edge is required for the selected path.

Every edge is directional: `source -> target` means source competency supports target competency.

## Graph overview

```text
SAP-FND-01 requirements/tradeoffs ─┬─> every professional objective
SAP-FND-02 boundary tracing ───────┘

SAP-ORG-01 network ────────────────> continuity/reliability/performance/migration
SAP-ORG-02 security ───────────────> new security/improvement/migration
SAP-ORG-04 multi-account ──────────> organization cost + migration governance
SAP-ORG-03 resilience ─────────────> continuity + reliability improvement
SAP-ORG-05 cost ───────────────────> new/improvement cost

SAP-NEW-01 deployment ─────────────> operational improvement
SAP-NEW-02 + SAP-NEW-04 ───────────> reliability improvement
SAP-NEW-03 ────────────────────────> security improvement
SAP-NEW-05 ────────────────────────> performance improvement
SAP-NEW-06 ────────────────────────> cost improvement

SAP-MIG-01 assessment ─> SAP-MIG-02 mechanism ─> SAP-MIG-03 target ─> SAP-MIG-04 modernization
```

## Dependency edges

| Source | Target | Category | Why / satisfaction criterion |
|---|---|---|---|
| SAP-FND-01 | All SAP-ORG/NEW/IMP/MIG objectives | Blocking | Learner must identify and prioritize explicit requirements and justify a unique-best tradeoff |
| SAP-FND-02 | SAP-ORG-01, -02, -03, -04; SAP-NEW-02, -03, -04; SAP-MIG-02, -03, -04 | Blocking | Learner must trace the boundary type material to the target scenario |
| SAP-FND-02 | Remaining professional objectives | Bridge | A short ownership/dependency trace is sufficient when cross-boundary behavior is secondary |
| SAP-ORG-01 | SAP-NEW-02 | Bridge | Continuity designs need Region/AZ/DNS/connectivity implications, not the entire networking objective |
| SAP-ORG-01 | SAP-NEW-03 | Bridge | Endpoint and network-control choices require flow/segmentation basics |
| SAP-ORG-01 | SAP-NEW-04 | Blocking | Reliability reasoning must cover routing, failure domains, and connectivity dependencies |
| SAP-ORG-01 | SAP-NEW-05 | Bridge | Latency, global delivery, and access patterns require a bounded network-performance trace |
| SAP-ORG-01 | SAP-MIG-02 | Blocking | Migration approach depends on connectivity, DNS, bandwidth/latency, and hybrid boundaries |
| SAP-ORG-02 | SAP-ORG-04 | Bridge | Multi-account design needs bounded IAM/SCP, federation, encryption, and audit foundations |
| SAP-ORG-02 | SAP-NEW-03 | Blocking | New-solution controls build on identity, network, encryption, and centralized security semantics |
| SAP-ORG-02 | SAP-IMP-02 | Blocking | Improvement requires an established control model against which to audit gaps |
| SAP-ORG-02 | SAP-MIG-02 | Blocking | Migration mechanisms must preserve identity, encryption, and least-privilege boundaries |
| SAP-ORG-03 | SAP-NEW-02 | Blocking | Continuity selection requires RTO/RPO and recovery-pattern judgment |
| SAP-ORG-03 | SAP-NEW-04 | Bridge | Reliability needs failure/backup/recovery foundations, with solution-specific detail added later |
| SAP-ORG-03 | SAP-IMP-04 | Blocking | Existing reliability remediation requires failure-domain and recovery-pattern judgment |
| SAP-ORG-04 | SAP-ORG-05 | Recommended | Account/OU ownership improves allocation and governance, but cost mechanics can be learned separately |
| SAP-ORG-04 | SAP-MIG-02 | Bridge | Large migrations need an account/governance landing context |
| SAP-ORG-05 | SAP-NEW-06 | Blocking | Solution-level optimization builds on pricing, allocation, visibility, and rightsizing concepts |
| SAP-ORG-05 | SAP-IMP-05 | Blocking | Existing-solution cost analysis needs organization-scale visibility/allocation foundations |
| SAP-NEW-01 | SAP-IMP-01 | Blocking | Improving deployment/change automation requires the ability to evaluate deployment and rollback designs |
| SAP-NEW-02 | SAP-IMP-04 | Bridge | Existing reliability improvement reuses continuity and recovery-test concepts |
| SAP-NEW-03 | SAP-IMP-02 | Blocking | Security audit/improvement builds on correct control selection |
| SAP-NEW-04 | SAP-IMP-04 | Blocking | Improvement requires a target reliability model for comparison |
| SAP-NEW-05 | SAP-IMP-03 | Blocking | Bottleneck remediation requires correct target-platform/access-pattern reasoning |
| SAP-NEW-06 | SAP-IMP-05 | Blocking | Cost remediation requires correct solution cost-model judgment |
| SAP-MIG-01 | SAP-MIG-02 | Blocking | Mechanism cannot be selected coherently before workload disposition, constraints, and wave context are known |
| SAP-MIG-02 | SAP-MIG-03 | Blocking | Target platform selection must respect chosen migration/cutover constraints |
| SAP-MIG-03 | SAP-MIG-04 | Bridge | Modernization requires target-platform tradeoffs but can revisit them within a concise bridge |
| SAP-NEW-04 | SAP-MIG-03 | Recommended | Target architecture benefits from reliability pattern depth |
| SAP-NEW-05 | SAP-MIG-03 | Recommended | Target architecture benefits from performance/access-pattern depth |
| SAP-NEW-01 | SAP-MIG-04 | Recommended | Modernization benefits from deployment/change strategy context |
| SAP-NEW-04 | SAP-MIG-04 | Bridge | Decoupling and managed services must still meet reliability requirements |
| SAP-NEW-06 | SAP-MIG-04 | Recommended | Modernization economics matter but may be scoped out if cost is not a material requirement |
| SAP-EMG-01 | all scored objectives | Independent | Emerging pretest watch does not block scored-domain completion |

Objectives within a domain that have no listed edge are independent relative to one another, although SAP-FND-01/02 still apply.

## Objective-cluster prerequisites

| Cluster | Blocking prerequisites | Bridges | Recommended context |
|---|---|---|---|
| Organization-scale architecture | SAP-FND-01, SAP-FND-02 | IAM/policy evaluation, account/OU semantics | Cost allocation and network hub patterns |
| New solutions | SAP-FND-01 plus relevant ORG foundation for each quality attribute | Cross-boundary trace | Other Well-Architected qualities not material to the selected objective |
| Existing improvement | Corresponding NEW target-state competency | Current-state evidence interpretation | Adjacent improvement pillars |
| Migration/modernization | SAP-FND-01/02, SAP-MIG-01 sequence, network/security for mechanism selection | Governance, reliability, cost, deployment as scenario requires | Deep implementation procedures |

## Prerequisite dispositions in a realization

Every relevant prerequisite receives exactly one visible disposition:

| Disposition | Required record | Completion consequence |
|---|---|---|
| Included | Objective/bridge scope and evidence opportunity | Normal completion path |
| Supplied by bridge | Exact bounded competency, source, and completion check | Satisfies only the named edge, not the full source objective |
| Satisfied by prior learning | Learner assertion plus date/scope | Blocking assertions require recommended verification; confidence remains qualified until verified |
| Satisfied by evidence | Reviewed credential/work product mapped to the satisfaction criterion | Accepted only within evidence scope/currency |
| Satisfied by diagnostic | Reviewed deterministic diagnostic and threshold/rule version | Satisfies mapped competency only |
| Temporarily waived | Reason, owner, review date, consequence, and downstream objectives | Remains an unresolved gap; may prohibit full completion claims |

Conversation memory alone cannot satisfy a prerequisite. A blocking assertion should lead with a diagnostic or evidence option; waiver is the explicit fallback.

## Diagnostic/evidence recommendations

- For SAP-FND-01: require the learner to identify all material requirements in a fresh architecture brief and explain why a rejected alternative loses.
- For SAP-FND-02: require a boundary/failure-flow trace across at least two accounts or Regions.
- For a domain objective: accept recent, reviewable architecture work only when it demonstrates the same decision operation and constraints; certification possession alone is supporting evidence, not automatic proof of every objective.
- For time-sensitive service behavior: diagnostic content must use currently approved claims, not remembered implementation facts.

No diagnostic score, threshold, or mastery rule is implemented or approved here.

## Pilot dependency slice

For the proposed SAP-ORG-04 pilot, the smallest coherent graph is:

```text
SAP-FND-01 (included bridge-sized lesson/check)
SAP-FND-02 (included bridge-sized lesson/check)
SAP-ORG-02 bounded identity/SCP/audit bridge
                    └──────────────> SAP-ORG-04 pilot
SAP-ORG-01 network context (warned omission unless a scenario uses shared networking)
SAP-ORG-05 cost context (warned omission)
```

This supports account/OU, governance, workforce access, central observability, resource-sharing, and delegated-security decisions without claiming completion of all Domain 1 or SAP-C02.

## Revision impact

A changed objective statement, task mapping, edge category, or satisfaction criterion creates a new architecture version. Impact review must identify affected realizations, bridges, diagnostics, claims, questions, approvals, and completion statements. Nothing here silently changes installed packs or learner progress.
