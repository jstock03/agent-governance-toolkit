# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from agt_evidence import AuditEntry as EvidenceAuditEntry
from agt_evidence import AuditLog as EvidenceAuditLog
from agt_evidence import FileAuditSink as EvidenceFileAuditSink
from agentmesh.governance.audit import AuditEntry, AuditLog
from agentmesh.governance.audit_backends import FileAuditSink


def test_legacy_audit_imports_alias_agt_evidence() -> None:
    assert AuditEntry is EvidenceAuditEntry
    assert AuditLog is EvidenceAuditLog
    assert FileAuditSink is EvidenceFileAuditSink
