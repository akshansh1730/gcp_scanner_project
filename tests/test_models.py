import pytest

from gcpscan.models import Finding, make_finding_id


def _finding(**overrides):
    base = dict(
        check_id="iam.sa_admin_roles",
        cis_control="TODO-CIS-ID",
        title="Service account has admin role",
        severity="HIGH",
        resource="//cloudresourcemanager.googleapis.com/projects/demo",
        remediation="gcloud projects remove-iam-policy-binding demo --member=... --role=roles/owner",
        evidence={"role": "roles/owner"},
    )
    base.update(overrides)
    return Finding(**base)


def test_finding_id_is_stable_and_derived():
    f1, f2 = _finding(), _finding(title="different title")
    assert f1.finding_id == f2.finding_id == make_finding_id(f1.check_id, f1.resource)


def test_finding_id_differs_by_resource():
    assert _finding().finding_id != _finding(resource="//x/projects/other").finding_id


def test_round_trip():
    f = _finding()
    assert Finding.from_dict(f.to_dict()) == f


def test_rejects_bad_severity():
    with pytest.raises(ValueError):
        _finding(severity="URGENT")


def test_rejects_empty_remediation():
    with pytest.raises(ValueError):
        _finding(remediation="")


def test_rejects_mismatched_finding_id():
    with pytest.raises(ValueError):
        _finding(finding_id="deadbeef")
