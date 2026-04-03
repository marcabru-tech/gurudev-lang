# Contributing to GuruDev®

Thank you for your interest in contributing to **GuruDev®**! This document describes the contribution process.

## Before You Start

1. **Read the CLA** — By submitting a pull request, you agree to the [Contributor License Agreement](../CLA.md).
2. **Read the Code of Conduct** — We expect all contributors to follow our [Code of Conduct](CODE_OF_CONDUCT.md).
3. **Check existing issues** — Search open issues before creating a new one.

## Development Setup

```bash
git clone https://github.com/marcabru-tech/gurudev-lang.git
cd gurudev-lang
pip install -e ".[dev]"
pytest  # confirm all tests pass
```

See [SETUP.md](../SETUP.md) for detailed instructions.

## Types of Contributions

### 🐛 Bug Reports

Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.md). Include:
- Minimal reproducible `.guru` code
- Expected vs. actual behavior
- Environment details

### ✨ Feature Requests

Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.md). Describe:
- The motivation for the feature
- Proposed syntax or API
- Which hermeneutic levels are affected

### 🔬 Research Proposals

Use the [Research Proposal template](.github/ISSUE_TEMPLATE/research_proposal.md) for theoretical extensions.

### 📝 Documentation

Documentation contributions are welcome! Files under `docs/` are licensed under CC BY-SA 4.0.

## Pull Request Process

1. **Fork** the repository and create your branch from `main`:
   ```bash
   git checkout -b feat/my-feature
   ```

2. **Make changes** following the project conventions:
   - Source code in `src/` (packages: `compiler`, `runtime`, `gurumatrix`, `gurudev`, `cli`)
   - Tests in `tests/` with `pytest`
   - Follow `black` + `isort` formatting

3. **Add tests** for new functionality.

4. **Run the full test suite**:
   ```bash
   pytest
   ```

5. **Format your code**:
   ```bash
   black src/ tests/
   isort src/ tests/
   ```

6. **Submit your PR** using the [PR template](.github/PULL_REQUEST_TEMPLATE.md).

## Coding Style

- Python 3.9+ compatible
- `black` for formatting (line length: 100)
- `isort` for import sorting
- Type annotations encouraged (mypy-compatible)
- Docstrings for public functions/classes

## Commit Message Format

```
<type>(<scope>): <short summary>

Types: feat, fix, docs, refactor, test, chore
Scope: lexer, parser, bytecode, runtime, dvm, cli, gurumatrix, docs

Examples:
  feat(runtime): add EMOTE opcode for level 6
  fix(lexer): handle multiline strings correctly
  docs(spec): update GURUMATRIX_SPEC with cells explanation
```

## Testing Guidelines

- All tests must pass before merging.
- New features must have corresponding tests.
- Tests are in `tests/` and run with `pytest`.
- The MVP proof test (`TestCasoZero.test_tres_outputs_computacionalmente_distintos`) must always pass.

## Questions?

Open an issue or email: guilherme@hubstry.com
