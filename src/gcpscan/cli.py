"""gcpscan command-line interface (Phase 1: stubs only)."""

from __future__ import annotations

import typer

app = typer.Typer(help="Read-only CIS GCP Foundations Benchmark scanner.", no_args_is_help=True)


def _not_yet(command: str, phase: int) -> None:
    typer.echo(f"`gcpscan {command}` is not implemented yet (planned for Phase {phase}).")
    raise typer.Exit(code=2)


@app.command()
def scan(project: str = typer.Option(..., "--project", "-p", help="GCP project ID")) -> None:
    """Collect a snapshot and run all checks."""
    _not_yet("scan", 2)


@app.command()
def report(project: str = typer.Option(..., "--project", "-p", help="GCP project ID")) -> None:
    """Write HTML and JSON reports for the latest scan."""
    _not_yet("report", 6)


@app.command()
def diff(project: str = typer.Option(..., "--project", "-p", help="GCP project ID")) -> None:
    """Compare the latest two scans: new, resolved, persisting, regressed."""
    _not_yet("diff", 7)


if __name__ == "__main__":
    app()
