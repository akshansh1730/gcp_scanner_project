# Checks catalogue

Map each check to its control ID in the pinned CIS benchmark version (`docs/CIS_VERSION.md`).
IDs are deliberately not listed here, because they change between versions. Look them up in the
benchmark PDF; never guess. Integrity checks are custom and use `cis_control = "CUSTOM"`.

MVP = Phases 3 to 5. Stretch = Phase 10.

## IAM (MVP)

| check_id | What fails | Default severity |
| --- | --- | --- |
| iam.sa_admin_roles | Service account holds Owner, Editor or an admin role | HIGH |
| iam.user_managed_sa_keys | User-managed service account keys exist | MEDIUM |
| iam.sa_key_age | User-managed key older than 90 days | MEDIUM |
| iam.non_org_accounts | Personal (e.g. gmail.com) accounts have project access | HIGH |
| iam.sa_user_at_project | Service Account User or Token Creator granted at project level | HIGH |
| iam.kms_rotation | KMS key rotation period longer than 90 days or unset | MEDIUM |
| iam.api_key_restrictions | API keys without application or API restrictions | MEDIUM |

## Logging and monitoring (MVP)

| check_id | What fails | Default severity |
| --- | --- | --- |
| log.audit_config_all_services | Data Access audit logs not enabled for all services | MEDIUM |
| log.sink_all_logs | No sink exports all log entries | MEDIUM |
| log.bucket_retention | Log export bucket has no retention policy / bucket lock | MEDIUM |
| log.metric_alerts | Missing log metric + alert for: ownership changes, audit config changes, custom role changes, firewall changes, route changes, VPC changes, storage IAM changes, SQL config changes | LOW each |
| log.dns_logging | Cloud DNS logging disabled on VPC networks | LOW |

## Audit-log integrity (MVP, custom)

| check_id | What fails | Default severity |
| --- | --- | --- |
| integrity.tamper_identities | Identities other than an approved list hold permissions to change audit config, sinks or log buckets (`resourcemanager.projects.setIamPolicy`, `logging.sinks.update/delete`, `logging.buckets.update/delete`) | HIGH |
| integrity.sink_changed | A sink's destination or filter differs from the previous scan | HIGH |
| integrity.sink_deleted | A sink present in the previous scan is gone | CRITICAL |
| integrity.default_sink_exclusions | Exclusions on `_Default` drop audit log entries | HIGH |
| integrity.audit_config_reduced | Audit log types enabled in the previous scan are now disabled | CRITICAL |

The three "compared with previous scan" checks need the prior snapshot; skip with a notice on
the first scan.

## Networking (MVP)

| check_id | What fails | Default severity |
| --- | --- | --- |
| net.default_network | The `default` network exists | MEDIUM |
| net.ssh_open_world | Firewall allows 0.0.0.0/0 to port 22 | HIGH |
| net.rdp_open_world | Firewall allows 0.0.0.0/0 to port 3389 | HIGH |
| net.flow_logs | VPC Flow Logs disabled on a subnet | LOW |
| net.dnssec | DNSSEC disabled on a public Cloud DNS zone | LOW |

## Compute (MVP)

| check_id | What fails | Default severity |
| --- | --- | --- |
| vm.default_sa_full_scope | VM uses the default compute service account with full API access | HIGH |
| vm.public_ip | VM has an external IP | MEDIUM |
| vm.serial_port | Interactive serial port enabled | MEDIUM |
| vm.project_ssh_keys | Project-wide SSH keys not blocked | MEDIUM |
| vm.os_login | OS Login not enabled | MEDIUM |
| vm.shielded_vm | Shielded VM features off | LOW |
| vm.ip_forwarding | IP forwarding enabled | LOW |

## Storage (MVP)

| check_id | What fails | Default severity |
| --- | --- | --- |
| gcs.public_bucket | Bucket grants access to `allUsers` or `allAuthenticatedUsers` | CRITICAL |
| gcs.uniform_access | Uniform bucket-level access disabled | MEDIUM |

## Cloud SQL (stretch)

| check_id | What fails | Default severity |
| --- | --- | --- |
| sql.public_authorized_networks | Authorized networks include 0.0.0.0/0 | CRITICAL |
| sql.public_ip | Instance has a public IP | MEDIUM |
| sql.ssl_required | SSL not required for connections | HIGH |

## BigQuery (stretch)

| check_id | What fails | Default severity |
| --- | --- | --- |
| bq.public_dataset | Dataset accessible to `allUsers` or `allAuthenticatedUsers` | CRITICAL |

## Testbed ground truth

For every MVP check, `testbed/` plants at least one failing resource and one passing resource.
`testbed/expected_findings.json` lists the expected `check_id` + resource pairs; `make validate`
reports detected, missed and unexpected findings.
