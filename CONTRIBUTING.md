# Contributing to reverse-abliterate

Thanks for your interest in making LLM safety tools better!

## Development Setup

```bash
git clone https://github.com/Carlos-Projects/reverse-abliterate.git
cd reverse-abliterate
pip install -e .
pip install pytest ruff mypy
```

## Running Tests

```bash
python -m pytest tests/ -v
```

All tests must pass before submitting changes.

## Code Style

- **Linting**: `ruff check .` — fix with `ruff check . --fix`
- **Formatting**: `ruff format .`
- **Type checking**: `mypy src/`

We auto-run these via pre-commit hooks. Install them:

```bash
pip install pre-commit
pre-commit install
```

## Project Structure

```
reverse-abliterate/
├── src/reverse_abliterate/
│   ├── cli.py        # CLI commands (typer)
│   ├── constants.py  # Detection patterns and lists
│   ├── detect.py     # Abliteration scanning logic
│   └── harden.py     # Weight manifests + safety wrapper
├── tests/
│   └── test_reverse_abliterate.py
├── pyproject.toml
└── README.md
```

## Pull Request Process

1. Create a feature branch from `master`
2. Add tests for new functionality
3. Run `ruff check .` and `mypy src/` — must pass clean
4. Run `python -m pytest tests/ -v` — all must pass
5. Update CHANGELOG.md under `Unreleased`
6. Open a PR against `master`

## Adding a New Detector

1. Add the check function in `detect.py` following `_check_*` naming
2. Register it in `scan_directory()`
3. Add tests for it in `tests/test_reverse_abliterate.py`
4. Update CHANGELOG.md

## Adding a New Hardening Feature

1. Add the function in `harden.py`
2. Wire it into the CLI in `cli.py`
3. Add tests + update CHANGELOG

## Reporting Issues

Bug reports and feature requests go to [GitHub Issues](https://github.com/Carlos-Projects/reverse-abliterate/issues). For security issues, see SECURITY.md.

## Code of Conduct

Be respectful, constructive, and inclusive. We're all here to improve AI safety.
