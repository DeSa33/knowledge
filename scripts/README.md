# Repository verification

Run `python scripts/verify_repository.py` from the checkout. Python 3.10 or later and its standard library are sufficient; the working directory does not matter.

The script checks expected files, UTF-8 text, relative Markdown and HTML file destinations, essential citation/issue-form fields, and the exact PDF digest from `SHA256SUMS`. It rejects checksum paths escaping the repository, missing files, duplicate manifest entries, malformed digests, and a non-PDF header. A failing check exits nonzero.

It does not check external URLs, Markdown fragment anchors, complete YAML/CFF schema compliance, PDF rendering, proof correctness, or experimental results. The GitHub Actions workflow runs the same packaging check, not a BSG benchmark.

## Files

| File | Responsibility |
| --- | --- |
| [verify_repository.py](verify_repository.py) | Packaging, local-link, and artifact-integrity checks |
| [MAP.md](MAP.md) | Script dependencies and ownership |

## Catalog tools

`catalog.py` validates `catalog.json`, checks original artifact hashes, generates `CATALOG.md`, and searches collection metadata. Run `python scripts/catalog.py --check` to detect a stale index, or use `--write` after editing the metadata. See [the metadata reference](../docs/CATALOG_FORMAT.md).

`test_catalog.py` tests non-BSG and multiple collections, duplicate IDs, corrupt/missing files, path traversal, filters, deterministic rendering, and invalid dates. Run `python -m unittest discover -s scripts -p "test_*.py"`. These fixtures are synthetic contract tests, not research results.
