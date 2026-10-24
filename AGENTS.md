# Repository instructions

This is DeSa33's multi-project archive. Keep the README in a direct first-person voice. Read `docs/MAP.md`, then the exact collection files involved in the task.

- Preserve `BroadSematnicGenralzation(BSG).pdf` and its bytes unless an edit to the manuscript is explicitly requested. The PDF is authoritative for v4 statements.
- Keep a collection's overview, provenance, and guides together. Avoid duplicate READMEs and maps that repeat the same instructions.
- `catalog.json` owns collection metadata and artifact hashes. `scripts/catalog.py --write` generates `CATALOG.md`, `SHA256SUMS`, and the marked collection block in `README.md`. Do not edit those outputs by hand.
- Treat unknown authorship, dates, and versions as unknown; never fabricate peer review, affiliation, novelty, experimental results, or solved status.
- Keep repository checks separate from mathematical verification. Report the actual scope of any result.
- Run `python scripts/verify_repository.py` and `python -m unittest discover -s scripts` after changes. Use `python scripts/catalog.py --check` for a focused catalog check.
- Do not add an open-content license, third-party files, private data, or secrets without authorization.
- Update links and `docs/MAP.md` when paths change. Git history preserves previous layouts; do not rewrite it.
