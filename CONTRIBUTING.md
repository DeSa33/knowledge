# Contributing

This archive accepts material from different projects and papers. For a new collection, follow [Adding files](docs/ADDING_FILES.md) and update [the catalog](CATALOG.md). Name the relevant project; BSG is not the default scope of every submission.

Contributions should make a claim easier to understand, test, or falsify. Corrections and counterexamples are as useful as positive constructions.

## Choose a contribution

Use a **research review** issue for a theorem, definition, proof gap, counterexample, or clarification. Use an **experiment proposal or result** issue for a reproducible empirical investigation. For a documentation typo, a focused pull request is enough.

## Required context

State the project or paper, version, and section/equation/page or other precise location, exact assumptions, and the smallest reproducible example or derivation. Distinguish a proposed change from an established result. If an argument depends on an oracle, resets, intervention access, independence, a finite state bound, or numeric precision, say so explicitly.

For experiments, include code revision, environment, commands, seeds, budgets, baselines, source-null/expanded controls where relevant, raw outputs, uncertainty, and all failure cases. Follow [the evaluation guide](docs/bsg/EVALUATION.md).

## Pull-request workflow

1. Open an issue for substantial mathematical or structural changes.
2. Work on a descriptive branch and keep the change focused.
3. Update the nearest guide and map when paths or responsibilities change.
4. Run `python scripts/verify_repository.py`.
5. Explain what changed, why, how it was checked, and what remains uncertain.

Do not silently replace the original PDF. Proposed paper corrections should first identify the exact current text and the proposed replacement. Accepted new editions must update [provenance](docs/bsg/PROVENANCE.md), `SHA256SUMS`, citation information, and the changelog together.

## Attribution and permissions

Attribute external ideas and sources precisely. Disclose material AI assistance and what was checked by a person or executable test. Submit only material you have authority to contribute. No repository-wide open license has been selected; contributing does not imply a broad license change.

## Review criteria

- Assumptions and quantifiers are explicit and consistent.
- Information and computation available to the solver match the claim.
- Evidence supports the stated scope.
- Existing original artifacts and unrelated content are preserved.
- Documentation links and packaging checks pass.

Maintainer review is required for acceptance. Passing CI alone is not mathematical review.
