# Adding files and collections

## Intake

1. Identify the project or paper and the exact files to publish.
2. Check that public publication is intended and that the files contain no private information, credentials, or material lacking publication permission.
3. Preserve the original bytes when importing an existing artifact. Use the requested name when supplied; otherwise choose a clear, stable name.
4. Place related files together when that helps readers. Use `projects/<slug>/` or `papers/<slug>/` for new collections, or retain an explicitly requested path.
5. Create a short collection README for multi-file material. Describe real contents, scope, status, version/date, and how to use the files.
6. Add a [catalog](../CATALOG.md) entry and provenance information. Record original filename, import date, edits, and attribution when known.
7. Add an exact SHA-256 entry to `SHA256SUMS` for a primary imported artifact. Do not update an existing digest merely to silence an unexplained mismatch.
8. Update relevant maps and run `python scripts/verify_repository.py`.
9. Publish with a commit message naming the collection and purpose.

## Naming and versioning

Keep names descriptive and use extensions matching the actual file format. Preserve a user-specified spelling. If multiple editions are published, give them distinguishable versioned paths and link the current edition from the catalog. Do not silently replace a published edition with different content.

## Minimum context

| Field | What to record |
| --- | --- |
| Title and collection | What the artifact is and which project owns it |
| Type | Paper, design note, dataset, code, presentation, or other actual type |
| Version/date | Source version/date, or explicitly unknown |
| Status | Draft, proposal, working manuscript, experiment, reviewed result, etc. |
| Path | Exact relative path with working links |
| Provenance | Origin, import date, edits, and attribution when known |
| Integrity | SHA-256 for registered imported artifacts |
| Validation | Checks actually run and their limits |
| Rights | Applicable artifact-specific permissions, or unresolved status |

## Supporting evidence

For code or experiments, include the actual runnable sources, environment, commands, seeds, budgets, inputs, and outputs needed to reproduce the claim. If these are absent, say so. A document-only upload is valid; it need not pretend to include an implementation.

BSG-specific gates are documented in [its evaluation guide](bsg/EVALUATION.md). They are not requirements automatically imposed on every other project.
