# Subject-Pack Rights Policy

Status: Normative for format 0.2 and the Amateur Extra E1A pilot
Updated: 2026-07-18

This is a project policy decision, not legal advice or a formal legal review. Pack maintainers remain responsible for confirming that every included component may be distributed as declared.

## Component-level records

Format-0.2 packs must use component-level rights records. A single pack-wide license is invalid because official pool material, original educational prose, project code, and external references have different rights bases.

Each content-bearing record references the applicable rights record by stable ID. Rights scopes may not overlap ambiguously. An installable pack must contain all rights records required by its content and may not contain an unresolved rights status.

## Official NCVEC question-pool content

- Required `status`: `public_domain`.
- Required scope: only official question wording, ordered choices, answer keys, identifiers, and other pool material actually covered by the NCVEC Question Pool Committee's release statement.
- Required basis: a source reference to the [NCVEC 2024–2028 Extra Class release statement](https://ncvec.org/index.php/2024-2028-extra-class-question-pool-release).
- Public-domain status is a rights status, not a software or content license. Do not place `CC0`, Apache-2.0, or another license expression on this record unless the rights holder separately provides it.

This status does not cover project-authored explanations, third-party study text, NCVEC website presentation, trademarks, logos, seals, screenshots, or branding assets.

## Original project prose

- Scope: original Adaptive Learning Agent lessons and explanations.
- Required `status`: `licensed`.
- Required `license_expression`: `CC-BY-4.0`.
- Required copyright holder: `Adaptive Learning Agent contributors` unless a contributor supplies a more precise designation for their contribution.

Every lesson and project-authored explanation must reference this rights record. Attribution information must remain available to pack users. Project prose must never be labeled as official NCVEC commentary.

## Project code and schemas

Engine, adapter, skill, schema, and other project code remain under Apache License 2.0 as stated by the repository license. They are outside educational-content rights records. A pack must not claim that Apache-2.0 covers its original lessons or explanations.

## External official sources

- Required `status`: `reference_only`.
- Scope: FCC/eCFR and other external official sources used as references, plus NCVEC web pages outside the pool material actually covered by the public-domain statement.
- Permitted pack data: metadata, links, precise locators, titles, publisher details, retrieval/effective dates, revision identity, and optional content digests.
- Prohibited by default: substantial copied source text, complete source snapshots, screenshots, seals, logos, branding assets, and third-party explanatory text.

Additional source content may be redistributed only under separate, recorded authorization. The E1A pilot does not require complete FCC or NCVEC source snapshots inside the pack.

## Validation and review

Machine validation checks record structure, allowed statuses, required fields, component references, and the absence of unresolved scopes. It does not render a legal conclusion or verify a rights holder's claim.

For the E1A pilot, validation or pilot policy must reject:

- missing component rights metadata;
- original lessons or explanations scoped as `public_domain`;
- official pool content scoped as project-authored prose;
- a public-domain record without the NCVEC basis source;
- external official references treated as redistributable content without separate authorization;
- logos, seals, screenshots, branding assets, or unofficial third-party study text.

Human approval must include rights metadata in its non-empty review scope. Any rights-record change changes the pack digest and requires a new pack version or renewed approval under the format-0.2 approval policy.
