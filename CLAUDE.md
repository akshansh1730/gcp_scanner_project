# GCP CIS Scanner

## End goal

A read-only command-line tool that checks a Google Cloud project against the CIS Google Cloud
Platform Foundations Benchmark. It:

- ranks findings by severity,
- gives a specific fix for each finding,
- verifies that audit logging can be trusted,
- re-scans on a schedule and reports what is new, fixed or regressed since the last scan.

It must be proven to work: a deliberately misconfigured test project is scanned, and every
planted issue is caught.

## Definition of done

1. `gcpscan scan --project <id>` runs a full scan in one command.
2. Every check maps to a CIS control ID, and the README states how many controls are covered.
3. Every finding has: severity, resource, CIS control ID, description, remediation.
4. `gcpscan report` produces an HTML report and a JSON file.
5. `gcpscan diff` classifies findings as new, resolved, persisting or regressed.
6. Audit-log integrity checks detect disabled audit logs, changed or deleted log sinks, and
   identities that can tamper with logging.
7. The testbed in `testbed/` plants known misconfigurations, and `make validate` shows that
   every planted issue is detected.
8. `gcpscan schedule` sets up a recurring re-scan, and each run writes a diff against the
   previous scan (new / resolved / persisting / regressed).

## Rules (always follow)

- **Read-only against GCP.** Never run a command, API call or script that creates, changes or
  deletes GCP resources. The only exceptions are `testbed/` and `deploy/` Terraform, and only
  when I explicitly ask in the current message.
- **Never commit credentials.** No keys, tokens or service account JSON in the repo. Use
  Application Default Credentials. `.gitignore` covers `*.json` keys and `.env`.
- **Do not invent CIS control IDs.** Control numbers change between benchmark versions. Use the
  version pinned in `docs/CIS_VERSION.md`. If unsure of an ID, write `TODO-CIS-ID` and tell me.
- **Work one phase at a time** (see Build order). Do not start the next phase unless asked.
- **Every check gets a unit test** using a saved JSON fixture, never the live API.
- Run `pytest` before saying a task is done, and report the result.
- Ask before adding a new dependency or doing a large refactor.
- Keep replies short: show changed files and test results, not long explanations.

## Architecture

The design separates collecting data from checking it, so checks are testable offline and
drift detection compares saved snapshots.

```
collect  ->  snapshot (JSON on disk)  ->  checks (pure functions)  ->  findings  ->  report / diff
```

- **Collectors** call GCP APIs (prefer Cloud Asset Inventory where it covers the data) and save
  a timestamped snapshot to `scans/<project>/<timestamp>/snapshot.json`.
- **Checks** are pure functions: `check(snapshot) -> list[Finding]`. No API calls inside checks.
- **Findings** follow the schema below and are saved as `findings.json` next to the snapshot.
- **Diff** compares two `findings.json` files by `finding_id`.

```
gcp-cis-scanner/
  CLAUDE.md
  README.md
  pyproject.toml
  docs/
    CHECKS.md          # catalogue of checks to implement
    CIS_VERSION.md     # pinned benchmark version
    SEVERITY.md        # severity rubric
  src/gcpscan/
    cli.py
    collectors/        # one module per GCP area
    checks/            # iam.py, logging.py, integrity.py, network.py, compute.py, storage.py, sql.py, bigquery.py
    models.py          # Finding dataclass
    severity.py
    diff.py
    report/            # Jinja2 HTML template + JSON writer
  tests/
    fixtures/          # saved API responses, secure and insecure variants
  testbed/             # Terraform for the misconfigured test project + expected_findings.json
  deploy/              # Terraform for Cloud Scheduler + Cloud Run scheduled scans
  scans/               # git-ignored scan output
```

## Finding schema

```python
@dataclass
class Finding:
    finding_id: str      # stable: hash of check_id + resource_name
    check_id: str        # e.g. "iam.sa_admin_roles"
    cis_control: str     # from the pinned benchmark, or "CUSTOM" for integrity checks
    title: str
    severity: str        # CRITICAL | HIGH | MEDIUM | LOW (rubric in docs/SEVERITY.md)
    resource: str        # full GCP resource name
    evidence: dict       # the exact setting that failed
    remediation: str     # specific fix, with a gcloud command where possible
```

## Tech stack

- Python 3.11+, `pytest`, `typer` (CLI), `jinja2` (HTML report)
- Google Cloud client libraries; Cloud Asset Inventory API first
- Auth: Application Default Credentials, using a scanning identity with only the
  Security Reviewer and Viewer roles (plus Cloud Asset Viewer)
- Testbed: Terraform

## Build order

- [x] Phase 1: project skeleton, `Finding` model, CLI stub, pytest set up
- [ ] Phase 2: collectors for IAM and logging; save snapshots
- [ ] Phase 3: IAM and logging checks with fixtures and tests
- [ ] Phase 4: audit-log integrity checks
- [ ] Phase 5: network, compute and storage checks
- [ ] Phase 6: severity scoring + HTML/JSON report
- [ ] Phase 7: diff and drift detection (new / resolved / persisting / regressed)
- [ ] Phase 8: scheduled re-scans: `gcpscan schedule` installs a local cron/launchd job that
      runs scan + diff; Cloud Scheduler + Cloud Run job defined in `deploy/` (Terraform),
      applied only when I explicitly ask, same rule as `testbed/`
- [ ] Phase 9: testbed Terraform, `expected_findings.json`, `make validate`
- [ ] Phase 10 (stretch): Cloud SQL and BigQuery checks

The full check list is in `docs/CHECKS.md`. Read it only when working on checks.
