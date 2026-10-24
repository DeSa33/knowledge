# Reading guide

BSG asks when learned mechanisms can be reused across environments whose representations differ. The central difficulty is establishing that an apparent correspondence preserves the behavior needed for prediction and decisions.

## Suggested reading order

1. **Introduction and common setting (I–II):** environments, observations, interventions, source pools, encoders, and outcome readouts.
2. **Constraints (III):** external predictive scoring, representation collapse, and charged resource costs.
3. **Component problems (IV–XI):** P1–P8, each with its own information access and success conditions.
4. **Joint challenge (XII):** finite feasibility, uniform quantifiers, transfer/harm/coverage gates, and source attribution.
5. **Fixed reference family (XIII):** composed binary transducers, exact access, comparator, and abstraction test.
6. **Remaining discussion and appendices:** restricted checks, proof details, limitations, notation, and references. Consult the PDF's headings rather than assuming every illustration uses the same access model.

## Terms to keep distinct

| Term | Meaning in this collection |
| --- | --- |
| Representation | Declared information used to predict and choose actions, including charged adapters and memory |
| Correspondence | A mapping between domains that must preserve specified behavior and loss |
| Transfer | Source information used to improve a target decision task |
| Source-null control | Rerun with the source channel replaced under a registered law, keeping target rules and budgets fixed |
| Coverage | Frequency of authorization on related targets, rather than accuracy on only a selected subset |
| Breadth | The independently specified families handled by one procedure |
| Finite feasibility | An existence question for one complete finite contract and budget |
| Uniform guarantee | A claim about the same procedure across all declared sizes and, where specified, families |

## Common reading traps

- Predicting a self-chosen latent code perfectly does not establish accurate prediction of original outcomes.
- A passive correlation is not automatically an interventional effect.
- A fitted target decoder can hide the work attributed to a shared representation unless its full cost is charged.
- One failed candidate does not prove that the finite feasible set is empty.
- A theorem under a probability-law oracle does not automatically apply to a sample-only experiment.
- Zero observed failures is not a proof of zero risk.

Read the [manuscript](../../BroadSematnicGenralzation%28BSG%29.pdf), use the [problem index](PROBLEM_INDEX.md) to choose a task, and consult the [evaluation guide](EVALUATION.md) before making a result claim.
