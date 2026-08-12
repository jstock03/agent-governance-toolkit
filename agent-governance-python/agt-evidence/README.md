# agt-evidence

`agt-evidence` owns the durable governance evidence contract for the Agent
Governance Toolkit.

It includes:

- hash-chained audit records and Merkle inclusion proofs
- pluggable file and stdout audit sinks
- the `agt-runtime-evidence/v1` deployment manifest loader
- optional OpenTelemetry trace and span correlation identifiers

It does not own operational metrics, dashboards, SLOs, trace exporters, SBOM
generation, artifact signing, or release provenance. Operational telemetry can
be sampled or dropped. Governance evidence must remain independently
verifiable, so the two surfaces share correlation identifiers rather than
storage and retention semantics.

## Install

```bash
pip install agt-evidence
```

Install the optional OpenTelemetry API integration when the application does
not already provide it:

```bash
pip install "agt-evidence[otel]"
```

## Audit records

```python
from agt_evidence import AuditLog

audit = AuditLog()
entry = audit.log(
    event_type="policy_evaluation",
    agent_did="did:mesh:agent-1",
    action="read_customer_record",
    outcome="denied",
    policy_decision="deny",
    trace_id="4bf92f3577b34da6a3ce929d0e0e4736",
)

assert audit.verify_integrity() == (True, None)
assert entry.entry_hash
```

Legacy imports such as `agentmesh.governance.AuditLog` and
`agentmesh.governance.audit.AuditEntry` remain compatibility aliases.

The integrity verifier now hashes `agt_evidence.audit` and
`agt_evidence.backends`, which contain the implementation. Regenerate an
existing integrity manifest once after upgrading so it contains the new module
and critical-function entries.

## Trace correlation

```python
from agt_evidence import AuditLog, capture_current_correlation

correlation = capture_current_correlation()
audit = AuditLog()
audit.log(
    event_type="tool_invocation",
    agent_did="did:mesh:agent-1",
    action="lookup_order",
    trace_id=correlation.trace_id if correlation else None,
)
```

The audit record stores the W3C trace ID. `CorrelationContext` also exposes the
current span ID and trace flags for adapters that need them.

## Runtime evidence manifests

```python
from agt_evidence import RuntimeEvidence

evidence = RuntimeEvidence.load("agt-evidence.json")
assert evidence.schema == "agt-runtime-evidence/v1"
```

The loader accepts JSON or YAML and requires a top-level `deployment` object.
