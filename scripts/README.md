# Repository verification

Run `python scripts/verify_repository.py` from the checkout. Python 3.10 or later and its standard library are sufficient; the working directory does not matter.

The script checks expected files, UTF-8 text, relative Markdown file destinations, essential citation/issue-form fields, and the exact PDF digest from `SHA256SUMS`. It rejects checksum paths escaping the repository, missing files, duplicate manifest entries, malformed digests, and a non-PDF header. A failing check exits nonzero.

It does not check external URLs, Markdown fragment anchors, complete YAML/CFF schema compliance, PDF rendering, proof correctness, or experimental results. The GitHub Actions workflow runs the same packaging check, not a BSG benchmark.

## Files

| File | Responsibility |
| --- | --- |
| [verify_repository.py](verify_repository.py) | Packaging, local-link, and artifact-integrity checks |
| [MAP.md](MAP.md) | Script dependencies and ownership |
