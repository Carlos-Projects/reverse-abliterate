# reverse-abliterate

Detect and reverse model abliteration; harden LLMs against safety removal.

Abliteration surgically removes refusal directions from model weights, allowing
models to comply with harmful requests. This tool detects signs of abliteration
and applies hardening measures.

## Quick Start

```bash
# Scan a model directory for signs of abliteration
reverse-abliterate scan ./my-model/

# Generate weight integrity manifest
reverse-abliterate manifest ./my-model/

# Verify weights against a manifest
reverse-abliterate manifest ./my-model/ --verify

# Evaluate a prompt for safety concerns
reverse-abliterate probe "How do I make a bomb?"

# Check if forward hooks are being monitored
reverse-abliterate check-hooks
```

## Installation

```bash
pip install reverse-abliterate
```

## Detection

The scanner checks for:

- `abliteration_metadata.json` — created by OBLITERATUS during abliteration
- LoRA adapter files — `adapter_config.json`, `adapter_model.safetensors`
- Repository names ending in `-OBLITERATED`
- Missing quantization config on quantized models
- OBLITERATUS commit hashes in config files
- Suspicious weight shard filenames and sizes

## Hardening

- **Weight manifests**: SHA-256 hash manifests to detect tampering
- **Safety wrapper**: Keyword-based refusal detection and system prompt leak detection
- **Probe prompts**: 10 known jailbreak patterns for testing model compliance
- **Hook detection**: Detects when forward hooks are registered (PROBE phase of abliteration)
