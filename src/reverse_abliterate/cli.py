from __future__ import annotations

import json
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

from reverse_abliterate.detect import (
    detect_hook_registration,
    generate_report,
    scan_directory,
)
from reverse_abliterate.harden import (
    generate_hardening_report,
    generate_weight_manifest,
    safety_wrapper,
    verify_weight_integrity,
)

console = Console()
app = typer.Typer(
    name="reverse-abliterate",
    help="Detect and reverse model abliteration; harden LLMs against safety removal",
)


@app.command()
def scan(
    path: Path = typer.Argument(..., help="Path to model directory"),
    json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON"),
):
    """Scan a model directory for signs of abliteration."""
    if not path.exists() or not path.is_dir():
        console.print(f"[red]Error:[/] {path} is not a valid directory")
        raise typer.Exit(1)

    findings = scan_directory(path)
    if json_output:
        console.print(json.dumps(findings, indent=2))
    else:
        report = generate_report(path)
        console.print(Panel(report, title="Detection Results", border_style="yellow"))
        if findings:
            critical = sum(1 for f in findings if f["severity"] == "critical")
            high = sum(1 for f in findings if f["severity"] == "high")
            if critical or high:
                console.print(
                    f"\n[red]Found {critical} critical and {high} high-severity indicators.[/]"
                )
            else:
                console.print("\n[green]No critical or high-severity indicators found.[/]")


@app.command()
def manifest(
    path: Path = typer.Argument(..., help="Path to model directory"),
    verify: bool = typer.Option(False, "--verify", "-v", help="Verify against existing manifest"),
):
    """Generate a weight integrity manifest for a model."""
    if not path.exists() or not path.is_dir():
        console.print(f"[red]Error:[/] {path} is not a valid directory")
        raise typer.Exit(1)

    if verify:
        manifest_file = path / "weight_manifest.json"
        if not manifest_file.exists():
            console.print(f"[red]Error:[/] No manifest found at {manifest_file}")
            raise typer.Exit(1)
        manifest = json.loads(manifest_file.read_text())
        issues = verify_weight_integrity(path, manifest)
        if issues:
            console.print("[red]Weight integrity verification FAILED:[/]")
            for issue in issues:
                console.print(f"  [!] {issue}")
        else:
            console.print("[green]Weight integrity verification PASSED.[/]")
    else:
        m = generate_weight_manifest(path)
        manifest_path = path / "weight_manifest.json"
        manifest_path.write_text(json.dumps(m, indent=2))
        console.print(f"[green]Manifest written to {manifest_path}[/]")
        console.print(f"  Files: {len(m['files'])}")
        console.print(f"  Integrity hash: {m['integrity_hash'][:16]}...")


@app.command()
def probe(
    text: str = typer.Argument(..., help="User input to evaluate"),
    response: str = typer.Option(None, "--response", "-r", help="Model response to evaluate"),
):
    """Evaluate a user input or model response for safety concerns."""
    result = safety_wrapper(text, response)
    if result["input_flagged"]:
        console.print(f"[yellow]Input flagged:[/] {', '.join(result['warnings'])}")
    if result["output_flagged"]:
        console.print(f"[red]Output flagged:[/] {', '.join(result['warnings'])}")
    if not result["input_flagged"] and not result["output_flagged"]:
        console.print("[green]No safety concerns detected.[/]")
    if result:
        console.print("\n[dim]Details:[/]")
        console.print(json.dumps(result, indent=2))


@app.command()
def harden(
    path: Path = typer.Argument(..., help="Path to model directory"),
    output: Path = typer.Option(None, "--output", "-o", help="Output report to file"),
):
    """Generate a hardening report for a model."""
    if not path.exists() or not path.is_dir():
        console.print(f"[red]Error:[/] {path} is not a valid directory")
        raise typer.Exit(1)

    report = generate_hardening_report(path)
    if output:
        output.write_text(report)
        console.print(f"[green]Report written to {output}[/]")
    else:
        console.print(Panel(report, title="Hardening Report", border_style="green"))


@app.command()
def check_hooks():
    """Check if torch module.forward hooks are being monitored."""
    result = detect_hook_registration()
    if result["register_forward_hook_detected"]:
        console.print("[green]Forward hook monitoring is active.[/]")
    else:
        console.print("[yellow]No hook monitoring detected (torch may not be loaded).[/]")
    console.print(json.dumps(result, indent=2))


def main():
    app()


if __name__ == "__main__":
    main()
