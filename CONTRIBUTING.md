# Contributing

This is where I share my own papers and project files. Corrections, useful connections, and reproducible experiments are welcome.

## Give me something I can check

For a correction, name the project and version, point to the section or file, and explain the issue. Include a derivation, counterexample, or small reproduction when you can. You can [open an issue](https://github.com/DeSa33/knowledge/issues/new/choose) before writing a pull request.

For an experiment, include the code revision, commands, inputs, environment, and results. State the assumptions and limitations. BSG-specific comparisons should follow [its evaluation guide](papers/bsg/EVALUATION.md).

## Adding or updating material

Follow the [repository guide](docs/README.md#add-a-paper-or-project). Keep an original artifact unchanged unless the change is intentional. Give new editions distinct paths so readers can still find the version they used.

Submit only files you have permission to publish. Attribute external work and disclose material AI assistance. For this repo, publication and reuse permissions are separate; see [RIGHTS.md](RIGHTS.md).

## Before a pull request

1. Keep the change focused and explain what it fixes or adds.
2. Update affected links and catalog metadata.
3. Regenerate the indexes with `python scripts/catalog.py --write` if metadata changed.
4. Run `python scripts/verify_repository.py` and `python -m unittest discover -s scripts`.
5. State what you checked and what remains uncertain.

I review changes before accepting them. Passing the repository checks establishes file and catalog consistency; scientific claims need their own evidence.
