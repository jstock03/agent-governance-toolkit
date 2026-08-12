# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from agt_evidence import AuditEntry, AuditLog, FileAuditSink, HashChainVerifier


def test_public_audit_contract_preserves_hash_chain(tmp_path) -> None:
    path = tmp_path / "audit.jsonl"
    secret = b"test-secret"
    sink = FileAuditSink(path, secret)
    audit = AuditLog(sink=sink)

    first = audit.log(
        event_type="policy_evaluation",
        agent_did="did:mesh:agent-1",
        action="read",
        policy_decision="allow",
        trace_id="4bf92f3577b34da6a3ce929d0e0e4736",
    )
    second = audit.log(
        event_type="tool_invocation",
        agent_did="did:mesh:agent-1",
        action="lookup",
    )

    assert isinstance(first, AuditEntry)
    assert second.previous_hash == first.entry_hash
    assert audit.verify_integrity() == (True, None)
    assert audit.get_proof(first.entry_id)["verified"] is True
    assert sink.verify_integrity() == (True, None)
    assert HashChainVerifier().verify_file(path, secret) == (True, [])


def test_audit_entry_keeps_trace_identifier() -> None:
    entry = AuditEntry(
        event_type="policy_evaluation",
        agent_did="did:mesh:agent-1",
        action="read",
        trace_id="4bf92f3577b34da6a3ce929d0e0e4736",
    )

    assert entry.trace_id == "4bf92f3577b34da6a3ce929d0e0e4736"
