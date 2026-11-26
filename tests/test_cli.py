from typer.testing import CliRunner

from gcpscan.cli import app

runner = CliRunner()


def test_help_lists_commands():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    for cmd in ("scan", "report", "diff"):
        assert cmd in result.output


def test_scan_requires_project():
    assert runner.invoke(app, ["scan"]).exit_code != 0


def test_scan_stub_exits_cleanly():
    result = runner.invoke(app, ["scan", "--project", "demo"])
    assert result.exit_code == 2
    assert "not implemented" in result.output
