# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Runtime evidence manifest contract."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

EVIDENCE_SCHEMA = "agt-runtime-evidence/v1"


@dataclass
class RuntimeEvidence:
    """Runtime evidence manifest emitted by an AGT deployment."""

    source_path: str
    schema: str
    generated_at: str
    toolkit_version: str
    deployment: dict[str, Any]

    @classmethod
    def load(cls, path: str | Path) -> RuntimeEvidence:
        """Load and validate a JSON or YAML runtime evidence manifest."""
        evidence_path = Path(path).expanduser().resolve()
        raw = evidence_path.read_text(encoding="utf-8")

        if evidence_path.suffix.lower() in {".yaml", ".yml"}:
            data = yaml.safe_load(raw)
        else:
            data = json.loads(raw)

        if not isinstance(data, dict):
            raise ValueError("Evidence file must contain an object at the top level.")

        schema = data.get("schema")
        if schema != EVIDENCE_SCHEMA:
            raise ValueError(
                f"Unsupported evidence schema {schema!r}. "
                f"Expected {EVIDENCE_SCHEMA!r}."
            )

        deployment = data.get("deployment")
        if not isinstance(deployment, dict):
            raise ValueError("Evidence file missing required 'deployment' object.")

        return cls(
            source_path=str(evidence_path),
            schema=schema,
            generated_at=str(data.get("generated_at", "")),
            toolkit_version=str(data.get("toolkit_version", "")),
            deployment=deployment,
        )
