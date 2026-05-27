<div align="center">

# 🛡️ reverse-abliterate

**Detect and reverse model abliteration — harden LLMs against safety removal.**

[![CI](https://github.com/Carlos-Projects/reverse-abliterate/actions/workflows/ci.yml/badge.svg)](https://github.com/Carlos-Projects/reverse-abliterate/actions/workflows/ci.yml)
[![Docs](https://github.com/Carlos-Projects/reverse-abliterate/actions/workflows/docs.yml/badge.svg)](https://carlos-projects.github.io/reverse-abliterate/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

</div>

Abliteration surgically removes refusal directions from model weights, allowing models to comply with harmful requests. **reverse-abliterate** detects signs of abliteration, verifies weight integrity, and provides hardening measures to keep LLMs safe.

Inspired by [OBLITERATUS](https://github.com/elder-plinius/OBLITERATUS) research — the counterpart to [L1B3RT4S](https://github.com/elder-plinius/L1B3RT4S) jailbreak library.

---

## What makes reverse-abliterate unique

| Capability | reverse-abliterate | Manual inspection | OBLITERATUS (complement) |
|---|---|---|---|
| **Abliteration detection** | ✅ scans metadata, weights, hooks | ❌ | Has the opposite goal |
| **SHA-256 weight manifests** | ✅ generate + verify | ❌ | ❌ |
| **Safety wrapper** | ✅ keyword-based refusal + system prompt leak | Manual | ❌ |
| **Jailbreak probe prompts** | ✅ 10 known patterns | ❌ | ❌ |
| **LoRA adapter detection** | ✅ | ❌ | ❌ |
| **CI/CD integration** | ✅ JSON output, exit codes | ❌ | ❌ |

---

## 🔍 Features

### Detection
| Check | What it finds |
|-------|--------------|
| `abliteration_metadata.json` | Created by OBLITERATUS during abliteration |
| LoRA adapter files | `adapter_config.json`, `adapter_model.safetensors` |
| Repo name `-OBLITERATED` | Standard abliteration naming convention |
| Weight anomalies | Suspicious shard sizes and filenames |
| Missing quantization config | On quantized models post-abliteration |
| OBLITERATUS commit hashes | Embedded `git rev-parse HEAD` in config files |
| Forward hook registration | Detects PROBE phase monitoring hooks |

### Hardening
| Feature | Description |
|---------|-------------|
| **Weight manifests** | SHA-256 hash manifests to detect tampering |
| **Integrity verification** | Verify weights against a trusted manifest |
| **Safety wrapper** | Keyword-based refusal detection |
| **System prompt leak detection** | Identifies system prompt extraction attempts |
| **Jailbreak probe prompts** | 10 known L1B3RT4S-derived jailbreak test patterns |

---

## ⚡ Quick Start

```bash
# Scan a model directory for signs of abliteration
reverse-abliterate scan ./my-model/

# JSON output for CI pipelines
reverse-abliterate scan ./my-model/ --json

# Generate weight integrity manifest
reverse-abliterate manifest ./my-model/

# Verify weights against a manifest
reverse-abliterate manifest ./my-model/ --verify

# Evaluate a prompt for safety concerns
reverse-abliterate probe "How do I make a bomb?"

# Check if forward hooks are being monitored
reverse-abliterate check-hooks

# Generate hardening report
reverse-abliterate harden ./my-model/
```

---

## 📦 Installation

```bash
pip install reverse-abliterate
```

Or from source:

```bash
git clone https://github.com/Carlos-Projects/reverse-abliterate.git
cd reverse-abliterate
pip install -e .
```

---

## 🧪 Detection Details

The scanner performs four categories of checks:

### Static Analysis
- Scans directory trees for `abliteration_metadata.json`
- Searches for `adapter_config.json` + `adapter_model.safetensors` pairs (LoRA)
- Checks repository name against `-OBLITERATED` suffix pattern
- Validates quantization config files for signs of tampering

### Weight Analysis
- Inspects `.safetensors` and `.bin` (PyTorch) files for size anomalies
- Detects unexpectedly small shards that may indicate weight replacement
- Flags files that don't match expected model architecture patterns

### Config Analysis
- Searches model config files (`config.json`, etc.) for OBLITERATUS commit hashes
- Checks if `_name_or_path` field contains `-OBLITERATED` suffix
- Validates metadata timestamps against known abliteration timeline

### Runtime Detection
- `check-hooks` command scans for `torch.nn.Module.register_forward_hook` registrations
- Forward hooks are used by OBLITERATUS during the PROBE phase to monitor activations
- Detects hook callback functions targeting refusal-related layers

---

## 🔐 Hardening Report

```bash
reverse-abliterate harden ./my-model/
```

Generates a comprehensive report with:
- **Weight manifest**: SHA-256 hashes for every weight file
- **Integrity check**: Cross-reference against previous manifest
- **Safety wrapper**: Python code for runtime input/output safety filtering
- **Known jailbreak patterns**: 10 L1B3RT4S-derived test prompts
- **System prompt leak test**: Evaluates model for system prompt extraction

---

## 🧰 CLI Reference

```
Usage: reverse-abliterate [OPTIONS] COMMAND

Commands:
  scan         Scan a model directory for signs of abliteration
  manifest     Generate or verify weight integrity manifests
  probe        Evaluate a prompt for safety concerns
  harden       Generate hardening report
  check-hooks  Check if forward hooks are registered on a model

Options:
  -j, --json    Output as JSON (scan command)
  --verify      Verify weights against manifest (manifest command)
```

---

## 🤝 Related Projects

| Project | Description |
|---------|-------------|
| [OBLITERATUS](https://github.com/elder-plinius/OBLITERATUS) | Model abliteration toolkit (⭐ 5.7k) |
| [L1B3RT4S](https://github.com/elder-plinius/L1B3RT4S) | Jailbreak library (⭐ 19k) |
| [MCPGuard](https://github.com/Carlos-Projects/mcpguard) | Runtime security proxy for MCP/A2A protocols |
| [MCPwn](https://github.com/Carlos-Projects/mcpwn) | Offensive security testing for MCP servers |
| [Palisade Scanner](https://github.com/Carlos-Projects/palisade-scanner) | Scan web content for prompt injection |
| [MCPscop](https://github.com/Carlos-Projects/mcpscope) | Unified security dashboard for MCP/A2A |
| [AgentGate](https://github.com/Carlos-Projects/agentgate) | Firewall and honeypot for AI agents |

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## 🔒 Security

Found a vulnerability? See [SECURITY.md](SECURITY.md).

## 📄 License

MIT
