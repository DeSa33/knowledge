# Catalog metadata

`catalog.json` is the source for [CATALOG.md](../CATALOG.md). Edit the JSON, then regenerate the readable catalog. CI rejects a stale generated catalog.

## Collection fields

| Field | Meaning |
| --- | --- |
| `id` | Unique stable lowercase slug |
| `title`, `subtitle` | Display title and optional subtitle |
| `summary` | Concise description of actual contents |
| `kind` | Artifact category, such as Research paper or Project documentation |
| `version` | Source edition, without a leading v |
| `date` | Document date in YYYY-MM-DD format |
| `status` | Accurate maturity or publication status |
| `topics` | Nonempty list of plain topic names used for browsing |
| `landing` | Existing repository-relative collection entry page |
| `provenance` | Existing provenance record |
| `artifacts` | Nonempty list of actual files |

Each artifact has a `label`, `path`, `format`, and exact `sha256`. Optional fields such as `pages` add file-specific context. Paths must resolve to files inside the repository. Do not enter placeholder filenames, authorship, or publication identifiers.

## Commands

```bash
python scripts/catalog.py --write
python scripts/catalog.py --check
python scripts/catalog.py --query transfer
python scripts/catalog.py --topic "Representation learning"
python scripts/catalog.py --type "Research paper" --status "Working manuscript"
python scripts/catalog.py --json
```

Search is a case-insensitive substring across metadata. Topic, type, and status filters use case-insensitive exact matches. Multiple filters are combined. With no filters the script lists every collection. This is local metadata search, not full-text search of PDFs.

The validator checks the schema version, required fields, collection IDs, ISO dates, topic names, local paths, and actual SHA-256 digests. The original `SHA256SUMS` is also checked separately by the repository verifier. Update both digest records intentionally when publishing a changed artifact.

## Adding another collection

Follow [Adding files](ADDING_FILES.md). Use the existing BSG entry as an example of metadata structure, not as a template for another project's scientific requirements. No specific topic, PDF filename, or BSG problem ID is required by the catalog tool.
