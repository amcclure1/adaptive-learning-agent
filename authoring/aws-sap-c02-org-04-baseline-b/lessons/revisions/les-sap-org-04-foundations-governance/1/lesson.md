# Multi-account foundations and governance

## Learning outcomes

After this lesson, you should be able to:

- choose account and organizational-unit boundaries from explicit control requirements;
- separate organizational grouping from workforce permission assignment;
- distinguish an SCP permission ceiling from an IAM permission grant; and
- preserve management-account, feature-mode, hierarchy, and account qualifications in an architecture decision.

## Begin with the decision boundary

`SAP-ORG-04` asks you to design a multi-account environment. In this pilot, an account boundary is useful when it makes a different governance or administrative requirement explicit. Do not infer that every team or reporting line requires its own OU. AWS guidance recommends applying common policies at the OU level because that can simplify policy management and troubleshooting. An OU is a logical grouping of accounts to which organization policies can be applied. Therefore, when accounts genuinely share a security-control baseline, a control-aligned OU can reduce repeated account-by-account policy work.

That is architectural guidance, not a universal service rule. A different set of requirements can justify a different grouping, and extra hierarchy adds reasoning and operational work. State the requirement first, then add only the boundary needed to express it.

## Protect the management-account boundary

AWS recommends limiting resources and data in the Organizations management account to what must be managed there. For ordinary workloads with no management-account-only dependency, the approved recommendation is to use member accounts. This qualification matters: the recommendation is not a claim that the management account can contain no resources.

The boundary is also technically distinct because SCPs do not constrain IAM users or roles in the management account. A design that places ordinary workloads there cannot cite a management-account-targeted SCP as their guardrail. This pilot does not claim a quantified blast-radius reduction; it teaches the narrower, approved management-account guidance and SCP exception.

## Understand what an SCP does—and does not do

SCPs are available only when the organization has the required feature mode; they are unavailable with consolidated-billing features only. For principals in affected member accounts that are subject to SCPs, an SCP defines a maximum-permission boundary and does not grant an allow. Evaluation follows the policy set at every level from the root through each OU to the account: the action must remain allowed through that chain, and an applicable explicit deny blocks it.

Keep two questions separate:

1. **May this principal receive the permission?** The applicable SCP chain bounds the answer for affected member-account principals.
2. **Has this principal actually received the permission?** Identity or resource policies still supply the allow.

Treating an SCP as an identity grant collapses those two questions and produces a faulty design.

## Assign workforce access centrally

IAM Identity Center account assignments connect workforce identities to permission sets. A permission set can be reused across more than one account. When assigned, IAM Identity Center creates the corresponding IAM role in the target account and attaches the permission-set policies. An assigned user can obtain temporary credentials for programmatic access.

This permission-assignment mechanism is different from an OU or an SCP. OUs group accounts for policy application; permission sets define reusable account access; SCPs bound maximum permissions for affected principals. When the scenario requires both reusable workforce access and prohibited actions in member accounts, combine Identity Center account assignments with correctly scoped SCPs. Neither mechanism should be described as doing both jobs.

## Decision checklist

- Identify which accounts share a control baseline before creating an OU.
- Keep ordinary workloads out of the management account unless a management-account-only function requires them there.
- Confirm the organization feature mode before relying on SCPs.
- Trace the entire root-to-account SCP chain.
- Name the identity mechanism that grants access; never claim that an SCP grants it.
- State whether a rule is AWS behavior, AWS guidance, or a conditional architecture recommendation.

## Learner-safe source summary

This lesson is based on official AWS documentation for Organizations management-account practices, OU policy targeting, SCP behavior and evaluation, and IAM Identity Center account access and permission sets. The source records retain exact retrieval dates, rights classification, and internal locators; the learner-facing links below identify the governing public pages without exposing private review notes.

## Sources

- [Management-account best practices](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_best-practices_mgmt-acct.html)
- [OU best practices](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_ous_best_practices.html)
- [Service control policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html)
- [SCP evaluation](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps_evaluation.html)
- [Configure access to AWS accounts](https://docs.aws.amazon.com/singlesignon/latest/userguide/manage-your-accounts.html)
- [Permission sets](https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsetsconcept.html)
- [Temporary IAM Identity Center credentials](https://docs.aws.amazon.com/singlesignon/latest/userguide/howtogetcredentials.html)
