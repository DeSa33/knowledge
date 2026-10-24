# Repository map

| Responsibility | Canonical location |
| --- | --- |
| Personal introduction and current work | [Root README](../README.md) |
| Collection metadata and artifact digests | [catalog.json](../catalog.json) |
| Generated reader index | [CATALOG.md](../CATALOG.md) |
| Original BSG manuscript | [Root PDF](../BroadSematnicGenralzation%28BSG%29.pdf) |
| BSG overview, citation, and reading order | [papers/bsg/README.md](../papers/bsg/README.md) |
| BSG mathematical task routes | [Problem index](../papers/bsg/PROBLEM_INDEX.md) |
| BSG evidence requirements | [Evaluation guide](../papers/bsg/EVALUATION.md) |
| BSG original-file record | [Provenance](../papers/bsg/PROVENANCE.md) |
| BSG proposed research directions | [Roadmap](../papers/bsg/ROADMAP.md) |
| Uploads, metadata format, and local commands | [Repository guide](README.md) |
| Catalog validation, generation, and search | `scripts/catalog.py` |
| Repository and section-link checks | `scripts/verify_repository.py` |
| Regression tests | `scripts/test_catalog.py`, `scripts/test_verify_repository.py` |
| README masthead | `assets/banner.svg` |
| Issue forms and CI | `.github/` |

`catalog.json` generates `CATALOG.md`, `SHA256SUMS`, and the marked README collection block. CI compares each output with freshly rendered content and verifies artifact digests. It never writes to the repository.

The original PDF is kept at its existing path. BSG guidance previously split across `docs/bsg/` and `papers/bsg/` now lives together under `papers/bsg/`. Those old layouts remain in Git history. The redundant navigation files, archive-level software citation, and speculative security-contact policy were removed. No research implementation was moved or added.
