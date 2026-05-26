# reverse-abliterate

## [Unreleased]

### Added
- Initial project creation
- `scan` command to detect abliteration artifacts
- `manifest` command to generate SHA-256 weight manifests
- `probe` command to probe model safety behavior
- Safety wrapper with keyword-based refusal detection
- System prompt leak detection
- LoRA adapter scanning for anomaly detection
- Docstrings for all public API functions (detect.py, harden.py)
- CONTRIBUTING.md with development setup, code style, PR process
- SECURITY.md with vulnerability reporting policy
- Sphinx documentation (docs/) with install, usage, API, development guides
- GitHub Pages deployment workflow (.github/workflows/docs.yml)
- GitHub issue templates (bug_report.yml, feature_request.yml)
- Pull request template (.github/PULL_REQUEST_TEMPLATE.md)
- Interactive demo script (demo.py) showcasing all capabilities
- `__version__` attribute in package init

### Changed
- pyproject.toml: added classifiers, keywords, project URLs, readme field
- pyproject.toml: fixed build-backend to setuptools.build_meta
- pyproject.toml: configured ruff lint rules
- README.md: comprehensive rewrite with badges, tables, CLI reference, related projects

## [0.1.0] - 2025-08-01

### Added
- Model directory scanning for abliteration metadata
- Weight integrity verification via SHA-256 manifests
- Safety hardening wrapper for LLM responses
- Refusal rate analysis
- CLI with typer and rich output
