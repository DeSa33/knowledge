# Scripts map

`verify_repository.py` reads repository files and `SHA256SUMS`. It writes nothing, requires no network, and uses only Python's standard library. It is called locally and by `.github/workflows/repository-checks.yml`.

Changes to the canonical PDF require an intentional manifest and provenance update. Changes to Markdown routes should be checked by this script. This subsystem owns packaging verification only; mathematical validation belongs to future explicit research implementations and evidence.

`catalog.py` consumes `catalog.json` and artifact bytes, produces `CATALOG.md` with `--write`, and validates it with `--check`. It also offers local metadata filtering. `test_catalog.py` verifies admission, integrity failure, and filtering behavior using temporary synthetic fixtures. CI runs both tools and the tests.
