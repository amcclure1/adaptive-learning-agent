# Centralized operations and shared services

## Learning outcomes

After this lesson, you should be able to:

- choose an organization trail for centrally managed activity evidence while preserving Region qualifications;
- distinguish read-only configuration aggregation from central security-setting authority;
- explain the service-specific boundary of delegated administration; and
- trace RAM resource ownership, consumer permissions, organization-sharing prerequisites, and Region scope.

## Centralize audit evidence deliberately

An organization trail records the configured CloudTrail events for the management and member accounts, subject to the trail's Region design and each account's applicable opt-in Region enablement. When another account joins, CloudTrail adds the applicable trail copy and service-linked role and starts logging under those same Region and opt-in conditions. A member-account user with sufficient permission can view the trail but cannot alter or delete it.

Those properties support a conditional recommendation: when the requirements call for centrally managed activity evidence and automatic coverage of joining accounts, use an organization trail and verify its Region and opt-in design. “Organization trail” is not shorthand for every event in every Region. The configured event selection and applicable Region conditions still matter.

The approved lesson scope does not establish destination-policy, bucket-ownership, encryption, notification, or log-delivery prerequisites. Validate those separately before treating delivered records as usable central evidence.

## Separate visibility from configuration authority

An AWS Config aggregator replicates authorized configuration and compliance data into a read-only view. With Organizations as its account source, it does not require per-source-account authorization. It also does not enable AWS Config in source accounts or Regions, deploy rules, or mutate source resources. A design must therefore ensure AWS Config is already enabled where evidence is required.

Security Hub CSPM central configuration solves a different problem. Its delegated administrator can associate a central configuration policy with accounts, OUs, or the organization root. For centrally managed targets, only that delegated administrator changes the governed enablement, standards, controls, and supported parameters in the home and linked Regions. Every intended target account must have Security Hub enabled in each intended opt-in linked Region. Except for controls involving global resources, a policy applies across the home-and-linked-Region set rather than an arbitrary subset.

When the requirement includes both a configuration-evidence view and centrally governed Security Hub settings, use the two capabilities as complements. Do not describe the Config aggregator as a deployment mechanism or Security Hub central configuration as a general inventory aggregator.

## Delegate by service, not by assumption

Registering a member account as delegated administrator grants authority for the particular integrated AWS service. It does not grant general administration of the organization. This allows bounded administrative responsibility for that integrated service to move to a member account while keeping the delegation boundary explicit. Apply only the approved service-specific configuration and Region rules; delegation alone does not establish a cross-service rule.

## Share eligible resources without changing ownership

For a supported resource type, AWS RAM can share a resource with accounts in a specified OU when the organization has all features enabled and resource sharing is enabled through RAM. Enabling the integration through RAM creates the required service-linked role; trusted access enabled only through Organizations is insufficient. The sharing account remains the owner. The RAM permission attached to the share is a maximum for a consumer; the consumer also needs an applicable identity policy granting the operation.

Regional resources remain Regional: the consumer accesses the resource only in the Region where it exists in the owner account. The share does not transfer ownership, override consumer identity controls, make an unsupported type shareable, or make a Regional resource global.

## Architecture tradeoffs

- **Separation of duties:** service-specific delegation can place operational authority in a member account without granting general organization administration.
- **Operational overhead:** control-aligned OU policies can simplify policy management, and an organization trail can avoid per-account trail creation when their approved prerequisites fit.
- **Visibility versus control:** Config aggregation supplies a read-only view; Security Hub central configuration supplies bounded central authority over selected CSPM settings.
- **Ownership:** a RAM participant consumes the resource within both the share permission and its identity permissions; the owner retains the resource.
- **Blast radius:** the approved baseline does not establish a general or quantified blast-radius claim for these services. Evaluate that concern only when a later approved claim defines the relevant failure or administrative boundary.

## Coverage boundary

These two lessons are a bounded, partial realization of SAP-ORG-04. Event-notification strategy and the relationship between AWS Control Tower and AWS Organizations are intentionally deferred because the approved claim baseline contains no claims for them. This pilot does not claim complete SAP-ORG-04, Domain 1, or SAP-C02 coverage.

## Learner-safe source summary

This lesson uses official AWS documentation for CloudTrail organization trails, AWS Config aggregation, Security Hub CSPM central configuration, Organizations delegated administration, and AWS RAM. The internal workspace binds exact approved source and claim digests; these learner links identify the public material without exposing internal findings or reviewer data.

## Sources

- [CloudTrail organization trails](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/creating-trail-organization.html)
- [AWS Config aggregation](https://docs.aws.amazon.com/config/latest/developerguide/aggregate-data.html)
- [Config aggregator authorization](https://docs.aws.amazon.com/config/latest/developerguide/aggregated-add-authorization.html)
- [Security Hub CSPM central configuration](https://docs.aws.amazon.com/securityhub/latest/userguide/central-configuration-intro.html)
- [Enable Security Hub central configuration](https://docs.aws.amazon.com/securityhub/latest/userguide/start-central-configuration.html)
- [Organizations delegated administrators](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_integrate_delegated_admin.html)
- [AWS RAM overview](https://docs.aws.amazon.com/ram/latest/userguide/what-is.html)
- [Sharing resources with AWS RAM](https://docs.aws.amazon.com/ram/latest/userguide/getting-started-sharing.html)
