# Contributing to the CBD Two-Pathway Model

Thank you for your interest in contributing to this research. This project is an open-science effort, and we welcome contributions from computational biologists, pharmacologists, mitochondrial researchers, and anyone with relevant expertise.

## How to Contribute

### Reporting Issues

- **Model discrepancies:** If simulation outputs conflict with published experimental data, please open an issue with the relevant citation.
- **Parameter challenges:** If you believe a kinetic parameter (Kd, scavenging capacity, etc.) should be recalibrated, provide the source data or reference.
- **Bug reports:** For code issues (dependency errors, numerical instability, plotting bugs), use the Bug Report issue template.

### Proposing Changes

1. Fork the repository.
2. Create a feature branch (`git checkout -b improvement/your-description`).
3. Make your changes with clear commit messages.
4. Ensure all simulations still run: `python simulation/simulation_v4_honest.py`
5. Open a Pull Request describing what changed and why.

### Research Collaboration

If you are interested in:
- **Wet-lab validation** of the falsifiable hypotheses (H1--H3)
- **Extending the ODE model** (e.g., adding ATP dynamics, calcium handling)
- **Cross-species parameterization** (rodent vs. human hepatocyte data)
- **Clinical data integration** (CBD trial datasets with liver function markers)

Please open an issue using the Research Collaboration template, or contact the corresponding author directly.

## Code Standards

- Python 3.9+ with dependencies listed in `requirements.txt`.
- Simulation scripts should save output to `figures/` using path-relative resolution.
- Use descriptive variable names that map to the biological quantities they represent.
- Include printed numerical summaries alongside any generated figures.

## Scientific Standards

- All parameter values must be traceable to published literature or clearly labeled as estimated.
- Synthetic or simulated data must never be presented as experimental results.
- New model versions should be added as separate scripts (e.g., `simulation_v5_*.py`), preserving the existing version history.

## License

By contributing, you agree that your contributions will be licensed under the same [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) license that covers this project.
