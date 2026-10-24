# knowledge

### A working archive of projects, papers, and ideas

**knowledge** is DeSa33's central repository for files from different projects: research papers, technical notes, mathematical work, project documents, and supporting evidence. Each project keeps its own context, provenance, and status. The archive can grow across topics without treating every file as part of one research program.

**Maintainer:** [DeSa33](https://github.com/DeSa33) · **Visibility:** public · **Current catalog:** [CATALOG.md](CATALOG.md)

## Explore the archive

| Collection | What is available | Status | Start here |
| --- | --- | --- | --- |
| Broad Semantic Generalization (BSG) | Original 17-page v4 manuscript, reading guide, problem index, and evaluation notes | Independent working manuscript; research questions remain open | [PDF](BroadSematnicGenralzation%28BSG%29.pdf) · [Collection guide](docs/bsg/README.md) |

BSG is the first collection, not the scope of the entire repository. Future uploads may belong to unrelated projects or papers. The [catalog](CATALOG.md) is the entry point for all collections.

## What belongs here

- Papers, manuscripts, and mathematical problem statements.
- Project plans, design documents, architecture notes, and technical explanations.
- Research logs, review notes, derivations, and counterexamples with clear context.
- Supporting datasets, code, or experiment records when their provenance and publication permissions are established.
- Versioned artifacts that should remain findable and understandable after the original conversation or work session.

An uploaded paper does not need an accompanying software implementation. A project document does not need to be a research result. Organize each item according to what it actually contains.

## Start here

| Your goal | Where to go |
| --- | --- |
| Find a paper or project | [Archive catalog](CATALOG.md) |
| Upload material from another project | [Adding files and collections](docs/ADDING_FILES.md) |
| Understand the folder conventions | [Archive guide](docs/README.md) |
| Navigate responsibilities and dependencies | [Project map](PROJECT_MAP.md) |
| Propose a correction or contribution | [Contributing](CONTRIBUTING.md) |
| Review the first research collection | [BSG guide](docs/bsg/README.md) |
| Verify artifact integrity | [SHA-256 manifest](SHA256SUMS) and [verification guide](scripts/README.md) |

## Organization

| Location | Responsibility |
| --- | --- |
| `CATALOG.md` | Human-readable index of every project, paper, and collection |
| `docs/` | Archive conventions and collection-specific guides |
| `docs/bsg/` | Supporting documentation for BSG only |
| `BroadSematnicGenralzation(BSG).pdf` | Original BSG v4 manuscript, kept at its requested path |
| `scripts/` | Repository packaging and integrity checks |
| `.github/` | Contribution forms, pull-request template, review routing, and CI |
| `CITATION.cff` | Citation metadata for the archive, not a substitute for individual paper citations |
| `SHA256SUMS` | Exact integrity records for cataloged artifacts |

For new collections, use `projects/<project-slug>/` or `papers/<paper-slug>/` when a dedicated folder is useful. Create those folders when real material arrives; empty directories do not establish a project. Existing explicitly requested paths, including the BSG PDF, remain stable.

## Document identity and evidence

Each catalog entry should state a title, project or collection, artifact type, version/date, path, and status. Keep an original file unchanged when importing it unless an edit is requested. Distinguish original artifacts from editorial summaries and derived results.

Claims belong to their source and scope. Mark work as a draft, working manuscript, proposal, executed experiment, reviewed result, or other accurate status. Public hosting and passing repository checks do not establish correctness, peer review, novelty, or a solved research problem.

## Verify locally

```bash
git clone https://github.com/DeSa33/knowledge.git
cd knowledge
python scripts/verify_repository.py
```

Python 3.10 or later and its standard library are sufficient. On Windows, use `py -3 scripts/verify_repository.py` if appropriate. The script checks required archive files, local Markdown destinations, metadata essentials, and registered file hashes. The same command runs in GitHub Actions.

The checks validate packaging, not mathematical proofs, scientific conclusions, external URLs, or every file format's internal structure. Project-specific validation belongs with the relevant collection.

## Featured first upload: BSG

[**Broad Semantic Generalization: Problems in Representation and Transfer**](BroadSematnicGenralzation%28BSG%29.pdf) — v4.0, 22 October 2026, 17 pages.

The original PDF is published as `BroadSematnicGenralzation(BSG).pdf` without changing its bytes. It defines eight mathematical problems and an integrated challenge involving representation and transfer. It describes itself as an independent working manuscript, discloses generative-AI assistance, and has not undergone independent peer review. Read [its provenance](docs/bsg/PROVENANCE.md) and [problem index](docs/bsg/PROBLEM_INDEX.md) for scope.

## Contribute and cite

See [CONTRIBUTING.md](CONTRIBUTING.md) for submissions and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for participation expectations. Research forms can be used for any collection; name the project or paper rather than assuming BSG.

Cite the specific artifact and version when discussing its contents. [CITATION.cff](CITATION.cff) describes this repository as an archive; individual papers may have different authorship and citation metadata.

No repository-wide open license has been selected. Public visibility does not create an additional general reuse license. See [RIGHTS.md](RIGHTS.md). Report sensitive issues according to [SECURITY.md](SECURITY.md).

[Changelog](CHANGELOG.md) · [Agent instructions](AGENTS.md) · [Archive map](PROJECT_MAP.md)
