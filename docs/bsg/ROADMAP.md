# Research roadmap

This is a direction for future work, not a claim that the listed research is implemented.

## Available now

- Original BSG v4 PDF, preserved under the requested filename.
- Reading guide, problem index, evidence/reporting guide, and provenance.
- Contribution guidance and structured issue forms.
- Automated repository packaging and integrity checks.

## Next useful contributions

| Workstream | Deliverable | Completion evidence |
| --- | --- | --- |
| Independent review | Section-specific proof and definition review | Public review tied to exact assumptions and equations |
| Reference implementation | Explicit Section XIII generator and access interfaces | Deterministic tests and independently checked equivalence cases |
| Baselines and controls | Implemented comparator and source-null protocol | Matched-access audit and full resource records |
| Finite feasibility | Construction or obstruction for a declared contract | Executable witness plus gate proof, or valid lower-bound argument |
| Uniform results | One procedure with stated size-dependent guarantees | Proof covering declared sizes and resource scaling |
| Additional families | Independently specified symbolic, numeric, or stateful families | Public encodings, interfaces, and family-specific limits |

## Admission of new results

Use a pull request with a claim header, derivation or reproducible implementation, validation evidence, and limitations. Add real files only when they exist; avoid empty `src/`, `data/`, or `results/` directories suggesting an implementation is already present.

Licensing and archival identifiers remain maintainer decisions. No publication date, journal acceptance, DOI, or research completion deadline is promised.
