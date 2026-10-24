# Project map

## Identity

`knowledge` is DeSa33's public archive for files from multiple projects and papers. BSG is its first collection. Original artifacts are authoritative for their contents; maps and guides provide routes and context.

## Task routes

| Task | Read first | Target |
| --- | --- | --- |
| Find any project or paper | [README](README.md) | [Catalog](CATALOG.md) |
| Add an unrelated project | [Adding files](docs/ADDING_FILES.md) | New collection and catalog entry |
| Read BSG | [Collection guide](docs/bsg/README.md) | [Original PDF](BroadSematnicGenralzation%28BSG%29.pdf) |
| Review a BSG statement | [BSG problem index](docs/bsg/PROBLEM_INDEX.md) | Exact PDF section/equation |
| Update an imported edition | Its collection provenance | Artifact, checksum, catalog, changelog |
| Change archive documentation | [Documentation map](docs/MAP.md) | Relevant Markdown file |
| Change CI | [Script guide](scripts/README.md) | Verification script and workflow |
| Contribute | [Contributing](CONTRIBUTING.md) | Scoped issue or pull request |

## Boundaries and dependencies

- `CATALOG.md` routes to real artifacts and collection guides.
- `assets/` owns the vector README masthead; see [its map](assets/MAP.md).
- `docs/` owns general conventions; `docs/bsg/` owns BSG context only.
- New collections use real `projects/<slug>/` or `papers/<slug>/` files when appropriate. No empty collections are implied.
- `SHA256SUMS` records exact registered artifact bytes; changes require intentional provenance updates.
- `.github/workflows/repository-checks.yml` runs `scripts/verify_repository.py` with read-only contents permissions.
- Packaging checks do not establish proof correctness or scientific validity.
- No BSG solver or dataset is bundled with its initial manuscript.

## Change discipline

Keep original filenames and bytes stable unless an edit is requested. Update the catalog and nearest map when adding or moving files. Keep claims within their collection and evidence scope. During initial setup, BSG supporting Markdown guides moved into `docs/bsg/`; the original PDF stayed at the requested root path. No implementation source was moved.
