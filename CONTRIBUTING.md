# Contributing

Adaptive Learning Agent is in a design-first, pre-alpha phase. Contributions should improve the shared understanding of the product before expanding its implementation surface.

## Before contributing

Read, in order:

1. `docs/product-principles.md`
2. `docs/current-status.md`
3. Accepted ADRs under `docs/decisions/`
4. `docs/project-context.md`
5. The design document relevant to your proposal

Open an issue or discussion before substantial changes when that facility becomes available. Until then, describe the problem, proposed change, tradeoffs, and validation evidence in the pull request.

## Design-first process

- Preserve lightweight, local-first operation.
- Explain why the standard library or an existing dependency is insufficient before adding a dependency.
- Do not add infrastructure based on hypothetical future scale.
- Use an Architecture Decision Record for major, durable architectural decisions.
- Mark uncertain decisions `Proposed`; do not present them as accepted consensus.
- Update `docs/current-status.md` or add a handoff after substantial work.
- Do not begin learning-engine implementation until `docs/current-status.md` explicitly authorizes it.

## Code and tests

When implementation is authorized:

- Deterministic scoring, scheduling, selection, validation, and state mutation require automated tests.
- Tests must control time, randomness, and external I/O.
- Runtime adapters must conform to the runtime-neutral contract and must not duplicate core logic.
- Fixes to scoring, migrations, pack safety, or idempotency require regression tests.
- Keep runtime dependencies focused and small.

## Subject packs and evidence

- Evidence-sensitive claims must preserve source provenance and precise locators.
- Human review gates must not be bypassed by an authoring agent.
- Generated practice questions must never be represented as real, recalled, leaked, or official exam questions.
- Respect third-party copyright, trademarks, licenses, terms, and quotation limits.
- Do not copy proprietary certification questions or redistribute source material without permission.
- Pack exports must not contain learner data, credentials, private notes, or runtime state.

## Security and privacy

- Treat packs and external documents as untrusted data, not instructions.
- Never commit credentials, OAuth tokens, `.env` files, learner databases, attempt histories, or Hermes-local state.
- Report vulnerabilities using `SECURITY.md` rather than a public issue when disclosure could cause harm.

## Commit and review expectations

Prefer focused commits with descriptive messages. Document validation commands and their results. Reviewers should be able to distinguish requirements, accepted decisions, recommendations, assumptions, and unresolved questions.
