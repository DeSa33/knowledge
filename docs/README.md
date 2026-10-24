# Working with this repo

The [README](../README.md) and [catalog](../CATALOG.md) are for reading the work. This guide covers adding files and maintaining the archive.

## Add a paper or project

1. Put related material in `papers/<name>/` or `projects/<name>/`. A collection README should explain what it is, its current status, and how to use the files. Include source/version details there or in a separate provenance record.
2. Keep an existing imported artifact unchanged unless you intend to publish a new edition. Use the requested filename where one was supplied. The original BSG PDF stays at its existing root path.
3. Add a collection record to `catalog.json`. Only list real files approved for public publication.
4. Calculate a SHA-256 digest for each original artifact. You can use `Get-FileHash -Algorithm SHA256 'path-to-file'` in PowerShell, or `sha256sum 'path-to-file'` on Linux. Store the lowercase hexadecimal value in the record.
5. Run `python scripts/catalog.py --write`, then the checks below. Commit the files, metadata, and generated indexes together.

A document-only upload is fine. Add code, datasets, or experimental results when they exist and belong with the work.

## Catalog fields

| Field | What to enter |
| --- | --- |
| `id` | Unique lowercase slug, such as `bsg` |
| `title`, `summary`, `kind`, `status` | The actual title, brief description, type of material, and current status |
| `subtitle` | Optional subtitle |
| `date` | Source date as `YYYY-MM-DD`, or `null` if unknown |
| `version` | Source version without a leading `v`, or `null` for unversioned material |
| `topics` | List of topic names |
| `landing` | Repository-relative path to the collection README |
| `provenance` | Path to source/version details; may be the same README |
| `artifacts` | List of files, each with `label`, `path`, `format`, and `sha256`; optional positive `pages` |

The [existing record](../catalog.json) is a complete example. Paths use forward slashes and exact filename case on every platform. Authors belong in the collection's citation details when established by the source; they are not inferred from the repository owner.

`catalog.json` is the only editable index. The catalog tool generates the readable catalog, checksum manifest, and collection table inside the README markers. It validates files against their recorded digests before writing anything. It never recalculates or silently replaces those digests.

## Check locally

Requires Python 3.10 or later and its standard library. No packages need installing.

```bash
python scripts/verify_repository.py
python -m unittest discover -s scripts
```

On Windows, `py -3` can replace `python`. The same checks run on Linux with Python 3.10 and Windows with Python 3.13 in GitHub Actions.

The verifier checks metadata, generated indexes, original-file hashes, UTF-8 text, common inline/reference/HTML links, and ordinary Markdown headings or explicit HTML IDs. It is a focused repository check rather than a complete CommonMark parser. The tests cover malformed input and realistic failure cases. These checks do not prove mathematical claims, inspect every document format, or check external URLs. Research validation belongs with the relevant project.

## Search the catalog

```bash
python scripts/catalog.py --query transfer
python scripts/catalog.py --topic "Representation learning"
python scripts/catalog.py --type "Research paper" --status "Working manuscript"
python scripts/catalog.py --json
```

Search matches metadata, not the full text of PDFs. Filters combine and are case-insensitive. Topic, type, and status match complete names. An empty result is reported clearly.

## Publish a new edition

Keep the old edition available. Add the new file with a distinct versioned name, document what changed and when, then update the catalog to point to the intended current edition. Record the new digest deliberately and regenerate the indexes. Never fix an unexplained checksum failure by simply changing the expected hash.

## Where things live

See the [repository map](MAP.md). The BSG paper's [provenance](../papers/bsg/PROVENANCE.md) records the preserved original edition. [RIGHTS.md](../RIGHTS.md) describes current reuse permissions.
