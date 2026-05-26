from __future__ import annotations

import json
import tempfile
from pathlib import Path


from reverse_abliterate.detect import scan_directory, generate_report
from reverse_abliterate.harden import (
    generate_weight_manifest,
    safety_wrapper,
    verify_weight_integrity,
)


class TestDetect:
    def test_scan_empty_directory(self):
        with tempfile.TemporaryDirectory() as d:
            findings = scan_directory(d)
            assert len(findings) == 0

    def test_scan_nonexistent(self):
        findings = scan_directory("/nonexistent/path")
        assert any(f["severity"] == "error" for f in findings)

    def test_abliteration_metadata_detected(self):
        with tempfile.TemporaryDirectory() as d:
            meta = {"method": "advanced", "source_model": "test-model"}
            Path(d, "abliteration_metadata.json").write_text(json.dumps(meta))
            findings = scan_directory(d)
            assert any(f["check"] == "abliteration_metadata" for f in findings)
            critical = [f for f in findings if f["severity"] == "critical"]
            assert len(critical) >= 1

    def test_lora_adapter_detected(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d, "adapter_config.json").write_text("{}")
            findings = scan_directory(d)
            assert any(f["check"] == "lora_adapter" for f in findings)

    def test_repo_name_obliterated(self):
        with tempfile.TemporaryDirectory(suffix="-OBLITERATED") as d:
            findings = scan_directory(d)
            assert any(f["check"] == "repo_name" for f in findings)

    def test_generate_report_no_findings(self):
        with tempfile.TemporaryDirectory() as d:
            report = generate_report(d)
            assert "No signs of abliteration detected" in report

    def test_generate_report_with_findings(self):
        with tempfile.TemporaryDirectory() as d:
            meta = {"method": "basic"}
            Path(d, "abliteration_metadata.json").write_text(json.dumps(meta))
            report = generate_report(d)
            assert "abliteration_metadata" in report


class TestHarden:
    def test_safety_wrapper_clean(self):
        result = safety_wrapper("What is the weather today?", "It is sunny.")
        assert not result["input_flagged"]
        assert not result["output_flagged"]

    def test_safety_wrapper_refusal_keyword(self):
        result = safety_wrapper("I cannot do that", None)
        assert result["input_flagged"]

    def test_weight_manifest_generation(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d, "model.safetensors").write_bytes(b"\x00" * 100)
            Path(d, "config.json").write_text("{}")
            manifest = generate_weight_manifest(d)
            assert len(manifest["files"]) == 1
            assert manifest["files"][0]["sha256"] is not None
            assert manifest["integrity_hash"] is not None

    def test_verify_integrity_pass(self):
        with tempfile.TemporaryDirectory() as d:
            data = b"\x01" * 100
            Path(d, "model.safetensors").write_bytes(data)
            manifest = generate_weight_manifest(d)
            issues = verify_weight_integrity(d, manifest)
            assert len(issues) == 0

    def test_verify_integrity_fail_on_tamper(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d, "model.safetensors").write_bytes(b"\x01" * 100)
            manifest = generate_weight_manifest(d)
            Path(d, "model.safetensors").write_bytes(b"\x02" * 100)
            issues = verify_weight_integrity(d, manifest)
            assert len(issues) >= 1
