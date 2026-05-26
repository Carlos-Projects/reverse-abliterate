from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from reverse_abliterate.constants import (
    ABLITERATION_META_FILE,
    COMMIT_PATTERN,
    LORA_FILES,
    OBLITERATED_SUFFIX,
)


def scan_directory(model_path: str | Path) -> list[dict[str, Any]]:
    """Scan a model directory for signs of abliteration.

    Performs static analysis, weight inspection, and config auditing
    to identify indicators of model abliteration (refusal direction removal).

    Args:
        model_path: Path to the model directory to scan.

    Returns:
        List of findings, each with keys: severity, check, detail, evidence.
        Severities: critical, high, warning, info, error.

    Example:
        >>> findings = scan_directory("./my-model/")
        >>> for f in findings:
        ...     print(f["severity"], f["check"])
    """
    path = Path(model_path).resolve()
    if not path.exists():
        return [
            {"severity": "error", "check": "path_exists", "detail": f"Path does not exist: {path}"}
        ]

    findings: list[dict[str, Any]] = []

    _check_abliteration_metadata(path, findings)
    _check_lora_adapters(path, findings)
    _check_weight_anomalies(path, findings)
    _check_repo_name(path, findings)
    _check_config_suspicious(path, findings)

    return findings


def _check_abliteration_metadata(path: Path, findings: list[dict[str, Any]]) -> None:
    """Check for abliteration_metadata.json left by OBLITERATUS.

    Reads the metadata file and extracts method, source_model, and quality_metrics.
    """
    meta_file = path / ABLITERATION_META_FILE
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text())
            findings.append(
                {
                    "severity": "critical",
                    "check": "abliteration_metadata",
                    "detail": f"Abliteration metadata found: {meta.get('method', 'unknown')} method on {meta.get('source_model', 'unknown')}",
                    "evidence": {
                        "path": str(meta_file),
                        "method": meta.get("method"),
                        "source_model": meta.get("source_model"),
                        "quality_metrics": meta.get("quality_metrics"),
                    },
                }
            )
        except (json.JSONDecodeError, OSError) as e:
            findings.append(
                {
                    "severity": "warning",
                    "check": "abliteration_metadata",
                    "detail": f"Abliteration metadata file exists but unreadable: {e}",
                }
            )


def _check_lora_adapters(path: Path, findings: list[dict[str, Any]]) -> None:
    """Check for LoRA adapter files left after abliteration.

    Looks for adapter_config.json and adapter_model.safetensors
    which OBLITERATUS writes when using LoRA-based abliteration.
    """
    for fname in LORA_FILES:
        f = path / fname
        if f.exists():
            findings.append(
                {
                    "severity": "high",
                    "check": "lora_adapter",
                    "detail": f"LoRA adapter file found: {fname}",
                    "evidence": {"path": str(f)},
                }
            )


def _check_weight_anomalies(path: Path, findings: list[dict[str, Any]]) -> None:
    """Check weight files for suspicious names and sizes.

    Flags single small shards (under 100MB) that may indicate
    non-original checkpoints, and filenames containing 'abliterated'.
    """
    safetensors_files = list(path.glob("*.safetensors"))
    if not safetensors_files:
        safetensors_files = list(path.glob("*.bin"))
    if not safetensors_files:
        return

    shards = [f for f in safetensors_files if f.stat().st_size > 0]
    if not shards:
        return

    if len(shards) == 1 and shards[0].stat().st_size < 100_000_000:
        findings.append(
            {
                "severity": "info",
                "check": "weight_shard_size",
                "detail": f"Single small shard ({shards[0].stat().st_size / 1e6:.1f}MB) — may indicate non-original checkpoint",
                "evidence": {
                    "file": str(shards[0]),
                    "size_mb": round(shards[0].stat().st_size / 1e6, 1),
                },
            }
        )

    for sf in shards:
        name_lower = sf.name.lower()
        if "abliterated" in name_lower or "obliterated" in name_lower:
            findings.append(
                {
                    "severity": "critical",
                    "check": "weight_filename",
                    "detail": f"Shard filename suggests abliteration: {sf.name}",
                    "evidence": {"file": str(sf)},
                }
            )


def _check_repo_name(path: Path, findings: list[dict[str, Any]]) -> None:
    """Check if directory name ends with -OBLITERATED suffix.

    OBLITERATUS renames models with this suffix after abliteration.
    """
    if OBLITERATED_SUFFIX in path.name:
        findings.append(
            {
                "severity": "critical",
                "check": "repo_name",
                "detail": f"Repository name ends with {OBLITERATED_SUFFIX}",
                "evidence": {"repo_name": path.name},
            }
        )


def _check_config_suspicious(path: Path, findings: list[dict[str, Any]]) -> None:
    """Check model config files for OBLITERATUS signatures and anomalies.

    Looks for:
    - Commit hashes containing 'OBLITERATUS: abliterated'
    - Missing quantization config on quantized models (post-abliteration stripping)
    """
    config_file = path / "config.json"
    if not config_file.exists():
        config_file = path / "adapter_config.json"
    if not config_file.exists():
        return

    try:
        config = json.loads(config_file.read_text())
        if "_commit_hash" in config and COMMIT_PATTERN in config.get("_commit_hash", ""):
            findings.append(
                {
                    "severity": "critical",
                    "check": "commit_hash",
                    "detail": f"Config commit hash contains OBLITERATUS signature: {config['_commit_hash']}",
                    "evidence": {"commit_hash": config["_commit_hash"]},
                }
            )
        if config.get("quantization_config") is None:
            orig = config.get("_name_or_path", "")
            if orig and any(kw in orig.lower() for kw in ["gptq", "awq", "gguf"]):
                findings.append(
                    {
                        "severity": "high",
                        "check": "quantization_stripped",
                        "detail": f"Model appears to use {orig} but quantization config is missing — may have been stripped during abliteration",
                        "evidence": {"original_model": orig},
                    }
                )
    except (json.JSONDecodeError, OSError):
        pass


def detect_hook_registration(_source: Any = None) -> dict[str, Any]:
    """Detect if torch forward hooks are currently being monitored.

    Checks if ``torch.nn.Module.register_forward_hook`` has been wrapped,
    which OBLITERATUS does during the PROBE phase to monitor activations.

    Args:
        _source: Reserved for future use.

    Returns:
        Dict with keys: register_forward_hook_detected, state_dict_access_detected,
        detail, risk.
    """
    result: dict[str, Any] = {
        "register_forward_hook_detected": False,
        "state_dict_access_detected": False,
        "detail": "",
        "risk": "none",
    }
    try:
        modules = list(sys.modules.keys())
        if "torch" in modules:
            torch_mod = sys.modules["torch"]
            if hasattr(torch_mod, "nn"):
                nn_mod = torch_mod.nn
                if hasattr(nn_mod, "Module"):
                    orig = getattr(nn_mod.Module, "register_forward_hook", None)
                    if orig and hasattr(orig, "__wrapped__"):
                        result["register_forward_hook_detected"] = True
                        result["risk"] = "high"
                        result["detail"] = (
                            "torch.nn.Module.register_forward_hook appears to be wrapped — active hook monitoring"
                        )
    except Exception:
        result["detail"] = "Unable to inspect torch module"
    return result


def generate_report(path: str | Path) -> str:
    """Generate a human-readable abliteration detection report.

    Args:
        path: Path to the scanned model directory.

    Returns:
        Formatted report string with findings grouped by severity.
    """
    findings = scan_directory(path)
    if not findings:
        return "No signs of abliteration detected."

    lines = ["## Abliteration Detection Report\n"]
    severity_order = {"critical": 0, "high": 1, "warning": 2, "info": 3, "error": 4}
    findings.sort(key=lambda f: severity_order.get(f.get("severity", "info"), 99))

    for f in findings:
        icon = {
            "critical": "[!!]",
            "high": "[!]",
            "warning": "[?]",
            "info": "[i]",
            "error": "[E]",
        }.get(f.get("severity", "info"), "[?]")
        lines.append(f"  {icon} {f['check']}: {f['detail']}")

    critical = sum(1 for f in findings if f["severity"] == "critical")
    high = sum(1 for f in findings if f["severity"] == "high")
    lines.append(f"\n{len(findings)} finding(s): {critical} critical, {high} high")
    return "\n".join(lines)
