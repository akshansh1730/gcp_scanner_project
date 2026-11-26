# gcpscan

Read-only scanner for the CIS Google Cloud Platform Foundations Benchmark. It ranks findings by
severity, gives a fix for each, checks that audit logging can be trusted, and reports what changed
since the last scan.

**Status:** Phase 1 (skeleton). CIS controls covered: 0 (updated as checks land).

## Setup

```bash
uv venv && uv pip install -e ".[dev]"
gcloud auth application-default login   # scanning identity: Security Reviewer + Viewer + Cloud Asset Viewer
```

## Usage

```bash
gcpscan scan --project <id>
gcpscan report --project <id>
gcpscan diff --project <id>
```

## Tests

```bash
pytest
```
