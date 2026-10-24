# Evaluation and evidence guide

This guide summarizes reporting expectations from BSG v4. The [manuscript](../BroadSematnicGenralzation%28BSG%29.pdf) supplies the actual contract; this document adds no new theorem or benchmark result.

## Freeze the contract first

Record the environment family and its law; source pool and provenance; permitted observations, resets, interventions, and oracles; query budgets; deployment horizon; baseline; prediction-query law; numeric precision; randomization; and every success threshold. Relatedness must come from the structural task contract, not from whether a candidate improved its score.

Specify discovery/validation separation before selecting candidates. Freeze the solver and library before held-out evaluation. Treat adaptive reuse of validation data as a changed statistical problem.

## Joint requirements

| Requirement | Evidence needed | Failure to avoid |
| --- | --- | --- |
| Transfer gain | Expected target loss relative to the declared target-only baseline on related tasks | Reporting representation agreement as decision value |
| Controlled harm | Harm-tail control on structurally unrelated tasks with stated estimation uncertainty | Calling zero observed failures zero risk |
| Coverage | Authorization probability on related targets | Always abstaining or reporting only successful cases |
| Prediction | Original-outcome predictive score under the fixed query law | Collapsing outcome labels or evaluating only training histories |
| Source attribution | Rerun under the specified source-null law and compare expected decision performance | Reusing answers to adaptive queries never asked by the control |
| Abstraction | The registered success, cost, or compression criterion on fresh structures | Uncharged target-specific readouts or decorative shared modules |
| Resources | Full code, time, memory, randomness, queries, output size, and precision accounting | Free source acquisition, fallback, or verifier assistance |

In Section XII, negative normalized loss difference favors transfer. Its finite decision track uses normalized Brier excess. Earlier log-loss illustrations and Brier quantities are different objects and must not be interchanged.

## Reference-family care

Section XIII uses composed binary Mealy transducers. Its primary target-only comparator is a precisely defined Bayes-optimal finite decision tree with unrestricted comparator computation. It is not a practical equal-time competitor. A compute-matched experiment may be added, but cannot silently replace the reference comparator.

The reference abstraction test uses four additional charged targets, exact behavioral correctness, a stipulated shared-artifact compression margin, and behaviorally material shared use. A PDF summary or file-integrity check does not implement any of these tests.

## Minimum experiment record

1. Identify manuscript version, problem, contract, and code revision.
2. Publish the generator, split policy, random seeds, access rules, and exact commands.
3. Declare thresholds, sample sizes, stopping rules, comparison method, and uncertainty estimates before evaluation.
4. Report related and unrelated tasks separately; retain failed, rejected, and abstained cases.
5. Include target-only, source-null, and expanded-library controls where the claim requires them.
6. Charge discovery, validation, adapters, fallback maintenance, and deployment as specified.
7. Preserve raw records and machine-readable outputs with provenance and integrity hashes.
8. State which gate passed, failed, or remains untested, and the scope supported by the evidence.

## Claim levels

- **Proposed:** an idea or future experiment.
- **Documented:** a statement present in the manuscript.
- **Observed:** an executed result under named conditions.
- **Reviewed:** a proof or method independently examined, with the review identified.
- **Verified for a contract:** the required checks passed under that exact contract and evidence model.

A bounded empirical success does not establish a universal theorem. A counterexample must satisfy the assumptions it is intended to refute. A failed implementation alone is not an impossibility proof.
