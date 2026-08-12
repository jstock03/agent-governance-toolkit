# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import json

import pytest

from agt_evidence import EVIDENCE_SCHEMA, RuntimeEvidence


def test_runtime_evidence_loads_json(tmp_path) -> None:
    path = tmp_path / "agt-evidence.json"
    path.write_text(
        json.dumps(
            {
                "schema": EVIDENCE_SCHEMA,
                "generated_at": "2026-08-12T00:00:00Z",
                "toolkit_version": "5.0.0",
                "deployment": {"audit_sink": {"enabled": True}},
            }
        ),
        encoding="utf-8",
    )

    evidence = RuntimeEvidence.load(path)

    assert evidence.source_path == str(path.resolve())
    assert evidence.deployment["audit_sink"]["enabled"] is True


def test_runtime_evidence_loads_yaml(tmp_path) -> None:
    path = tmp_path / "agt-evidence.yaml"
    path.write_text(
        "\n".join(
            [
                f"schema: {EVIDENCE_SCHEMA}",
                "generated_at: 2026-08-12T00:00:00Z",
                "toolkit_version: 5.0.0",
                "deployment:",
                "  identity:",
                "    enabled: true",
            ]
        ),
        encoding="utf-8",
    )

    evidence = RuntimeEvidence.load(path)

    assert evidence.deployment["identity"]["enabled"] is True


def test_runtime_evidence_rejects_unknown_schema(tmp_path) -> None:
    path = tmp_path / "agt-evidence.json"
    path.write_text(
        json.dumps({"schema": "unknown", "deployment": {}}),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Unsupported evidence schema"):
        RuntimeEvidence.load(path)
