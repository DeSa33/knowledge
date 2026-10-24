<p align="center">
  <img src="assets/banner.svg" alt="Knowledge — Projects, papers, and research" width="100%">
</p>

<p align="center">
  <a href="https://github.com/DeSa33/knowledge/actions/workflows/repository-checks.yml"><img src="https://github.com/DeSa33/knowledge/actions/workflows/repository-checks.yml/badge.svg" alt="Repository checks"></a>
</p>

<p align="center">
  <a href="CATALOG.md"><strong>Browse the catalog</strong></a> ·
  <a href="docs/ADDING_FILES.md">Add a collection</a> ·
  <a href="CONTRIBUTING.md">Contribute</a> ·
  <a href="CHANGELOG.md">Changelog</a>
</p>

## About

**knowledge** is a public archive of DeSa33's projects, papers, and research. It brings manuscripts, technical documents, mathematical work, and supporting evidence into one organized, versioned collection.

Each project has its own context and status. The [catalog](CATALOG.md) connects readers to the original files and their supporting documentation.

## Collections

### Broad Semantic Generalization · BSG

**Problems in Representation and Transfer** explores when a mechanism learned in one environment can remain useful in another with a different representation. The manuscript defines eight mathematical problems and a joint research challenge.

**v4.0 · 22 October 2026 · 17 pages · Working manuscript**

[**Read the paper →**](BroadSematnicGenralzation%28BSG%29.pdf) · [Reading guide](docs/bsg/README.md) · [Problem index](docs/bsg/PROBLEM_INDEX.md) · [Provenance](docs/bsg/PROVENANCE.md)

BSG is the archive's first collection. Additional projects and papers are indexed independently as they are published.

## Navigate

| Resource | Purpose |
| --- | --- |
| [Catalog](CATALOG.md) | Find projects, papers, versions, and primary files |
| [Archive guide](docs/README.md) | Understand organization and document conventions |
| [Adding files](docs/ADDING_FILES.md) | Prepare a new upload or collection |
| [Contribution guide](CONTRIBUTING.md) | Submit corrections, reviews, and new material |
| [Project map](PROJECT_MAP.md) | Locate files, responsibilities, and dependencies |
| [Verification guide](scripts/README.md) | Check local links and artifact integrity |

## Organization

| Path | Contents |
| --- | --- |
| `CATALOG.md` | Index of published collections |
| `docs/` | Archive guidance and collection documentation |
| `docs/bsg/` | BSG reading guide, evaluation notes, and provenance |
| `assets/` | Repository presentation assets |
| `scripts/` | Repository verification tools |
| `.github/` | Issue forms, review templates, and automated checks |

New collections may use `projects/<slug>/` or `papers/<slug>/` as material is added. Existing artifact paths remain stable, including `BroadSematnicGenralzation(BSG).pdf` at the repository root.

## Quality and provenance

Original imports retain their bytes unless a revision is explicitly requested. Catalog entries identify the artifact's version, date, and status; [SHA-256 records](SHA256SUMS) make registered file changes detectable.

The current BSG edition is an independent working manuscript, has not undergone independent peer review, and discloses AI assistance in its preparation note. Collection-specific claims and limitations are documented alongside each work. Repository checks cover packaging and integrity, not mathematical or scientific validity.

## Local verification

```bash
git clone https://github.com/DeSa33/knowledge.git
cd knowledge
python scripts/verify_repository.py
```

Requires Python 3.10 or later; no third-party packages. On Windows, `py -3 scripts/verify_repository.py` is also supported. GitHub Actions runs the same checks on pushes and pull requests.

## Contributing

New project files, precise corrections, proof reviews, and reproducible experiments are welcome. Start with [the contribution guide](CONTRIBUTING.md) or choose an [issue template](https://github.com/DeSa33/knowledge/issues/new/choose).

For citations, use the specific paper or artifact and its version. [CITATION.cff](CITATION.cff) identifies the archive. Rights and reuse permissions are described in [RIGHTS.md](RIGHTS.md); no repository-wide open license has been selected.

---

Maintained by [**DeSa33**](https://github.com/DeSa33) · [Code of conduct](CODE_OF_CONDUCT.md) · [Security](SECURITY.md)
