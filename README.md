<p align="center">
  <img src="assets/banner.svg" alt="Knowledge — Projects, papers, and research" width="100%">
</p>

<p align="center">
  <a href="https://github.com/DeSa33/knowledge/actions/workflows/repository-checks.yml"><img src="https://github.com/DeSa33/knowledge/actions/workflows/repository-checks.yml/badge.svg" alt="Repository checks"></a>
</p>

<p align="center">
  <a href="CATALOG.md"><strong>Browse all work</strong></a> ·
  <a href="#papers--research">Papers &amp; research</a> ·
  <a href="#browse-by-topic">Topics</a> ·
  <a href="docs/ADDING_FILES.md">Add files</a>
</p>

**knowledge** collects DeSa33's original papers, project documents, and research in one versioned archive. Start with a collection below or use the [full catalog](CATALOG.md) to find files, editions, and supporting material.

## Papers & research

| Collection | About | Edition | Open |
| --- | --- | --- | --- |
| **[Broad Semantic Generalization](papers/bsg/README.md)** | Eight mathematical problems in representation and transfer | v4.0 · Working manuscript | [Read PDF](BroadSematnicGenralzation%28BSG%29.pdf) · [Download](BroadSematnicGenralzation%28BSG%29.pdf?raw=true) |

Each collection has an entry page with its overview, artifacts, provenance, review status, and citation details. The archive also accepts technical designs, project notes, and supporting evidence from other work as they are published.

## Browse by topic

[**Representation learning**](CATALOG.md#representation-learning) · [**Transfer learning**](CATALOG.md#transfer-learning) · [**Causal identification**](CATALOG.md#causal-identification)

Only topics with published material are listed. [Browse all collections →](CATALOG.md)

## Find your way

| I want to… | Start here |
| --- | --- |
| Read a paper or explore a project | [Catalog](CATALOG.md) |
| Understand BSG before reading the manuscript | [BSG collection](papers/bsg/README.md) |
| Add files from another project | [Upload and collection guide](docs/ADDING_FILES.md) |
| Report an issue or suggest a correction | [Issue forms](https://github.com/DeSa33/knowledge/issues/new/choose) |
| Review or contribute research | [Contributing](CONTRIBUTING.md) |
| Navigate the repository's internals | [Project map](PROJECT_MAP.md) |

## About this archive

Original artifacts retain their own scope, version history, and rights status. The current BSG edition is an independent working manuscript; its [collection page](papers/bsg/README.md) documents review status and limitations. Metadata and [integrity records](SHA256SUMS) help readers identify the exact files they are using.

The catalog is generated from [structured metadata](catalog.json), with checks for missing files, duplicate identifiers, and artifact digests. See the [verification guide](scripts/README.md) for local commands and the limits of these checks.

<details>
<summary><strong>Local tools and repository conventions</strong></summary>

```bash
git clone https://github.com/DeSa33/knowledge.git
cd knowledge
python scripts/verify_repository.py
python scripts/catalog.py --check
python scripts/catalog.py --query transfer
```

Python 3.10 or later; no third-party packages. On Windows, `py -3` can replace `python`.

New multi-file collections use `papers/<slug>/` or `projects/<slug>/` when appropriate. Existing artifact paths remain stable. See the [archive guide](docs/README.md), [metadata reference](docs/CATALOG_FORMAT.md), and [project map](PROJECT_MAP.md).

</details>

---

Maintained by [**DeSa33**](https://github.com/DeSa33) · [Changelog](CHANGELOG.md) · [Citation metadata](CITATION.cff) · [Rights](RIGHTS.md) · [Conduct](CODE_OF_CONDUCT.md) · [Security](SECURITY.md)
