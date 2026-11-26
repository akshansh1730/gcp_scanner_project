"""Finding model shared by checks, report and diff."""

from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass, field
from typing import Any

SEVERITIES = ("CRITICAL", "HIGH", "MEDIUM", "LOW")


def make_finding_id(check_id: str, resource: str) -> str:
    """Stable ID: same check + same resource always gives the same ID across scans."""
    return hashlib.sha256(f"{check_id}|{resource}".encode()).hexdigest()[:16]


@dataclass
class Finding:
    check_id: str
    cis_control: str
    title: str
    severity: str
    resource: str
    remediation: str
    evidence: dict[str, Any] = field(default_factory=dict)
    finding_id: str = ""

    def __post_init__(self) -> None:
        if self.severity not in SEVERITIES:
            raise ValueError(f"severity must be one of {SEVERITIES}, got {self.severity!r}")
        for name in ("check_id", "cis_control", "title", "resource", "remediation"):
            if not getattr(self, name):
                raise ValueError(f"{name} must not be empty")
        expected = make_finding_id(self.check_id, self.resource)
        if not self.finding_id:
            self.finding_id = expected
        elif self.finding_id != expected:
            raise ValueError("finding_id does not match check_id + resource")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Finding:
        return cls(**data)
