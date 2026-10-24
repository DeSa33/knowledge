# BSG problem index

These are navigation summaries of v4, not replacement specifications. Read the complete statement and its local assumptions before proposing a solution.

| ID | Manuscript section | Task | Questions a contribution should answer |
| --- | --- | --- | --- |
| P1 | IV | Identify internal state from experiments | Which histories are distinguishable? What reset/query access and state bound are available? |
| P2 | V | Align domains while preserving behavior and loss | Which maps are learned? What equivalence is required and how is it checked? |
| P3 | VI | Learn reusable programs with resource advantage | Are library acquisition, definitions, adapters, and expanded controls charged? |
| P4 | VII | Design experiments identifying a causal effect | Which interventions are legal? Can two admissible models remain indistinguishable? |
| P5 | VIII | Admit transfer with controlled statistical risk | Are candidates fixed? Are validation episodes independent? How is selection accounted for? |
| P6 | IX | Certify composition error | Are error bounds uniform or distribution-specific? What support and stability assumptions are used? |
| P7 | X | Adapt under changing usefulness and delayed feedback | What changes, when is feedback available, and which comparator defines performance? |
| P8 | XI | Identify and transfer hidden-memory mechanisms | What state is observable, what history is retained, and how is identifiability established? |
| G | XII | Satisfy the joint requirements | Does one frozen procedure meet every gate for the exact contract? |
| Reference | XIII | Evaluate composed binary transducers | Are generator, source-null law, comparator, code, and abstraction test preserved? |

## Cross-cutting routes

- **Constant-map collapse and external prediction:** Section III and Appendix A.
- **Description-length and computability boundaries:** Appendix B.
- **Passive causal indistinguishability:** Appendix C.
- **Fixed-sample calibration and zero observed failures:** Appendix D.
- **Composition certificates:** Appendix E.
- **Notation:** Appendix F.

## Result submission header

Every proposed result should begin with:

```text
Manuscript: BSG v4.0 (22 October 2026)
Problem/section/equation:
Exact variant and environment class:
Information access:
Resources and precision:
Claim type: construction / proof / obstruction / empirical result / clarification
Evidence and reproduction method:
Known limitations:
```

Use the [evaluation guide](EVALUATION.md) for integrated claims and [contribution guide](../CONTRIBUTING.md) for submission details.
