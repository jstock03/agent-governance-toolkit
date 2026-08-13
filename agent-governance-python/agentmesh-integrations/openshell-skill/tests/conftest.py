# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""A minimal ACS contract stub for adapter unit tests.

The published ACS package includes a native extension. Adapter unit tests do
not need that extension, so this stub keeps the suite runnable in lightweight
Python jobs. Native ACS behavior is covered by the policy-engine SDK suite.
"""

from __future__ import annotations

import asyncio
import sys
import threading
import types
from dataclasses import dataclass
from enum import Enum
from typing import Any


class Decision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    WARN = "warn"
    ESCALATE = "escalate"
    TRANSFORM = "transform"

    @property
    def permits(self) -> bool:
        return self in {Decision.ALLOW, Decision.WARN, Decision.TRANSFORM}


class EnforcementMode(str, Enum):
    ENFORCE = "enforce"
    EVALUATE_ONLY = "evaluate_only"


class InterventionPoint(str, Enum):
    PRE_TOOL_CALL = "pre_tool_call"


@dataclass(frozen=True)
class Transform:
    path: str
    value: Any


@dataclass(frozen=True)
class Verdict:
    decision: Decision
    reason: str | None = None
    message: str | None = None
    transform: Transform | None = None


@dataclass(frozen=True)
class InterventionPointResult:
    verdict: Verdict
    transformed_policy_target: Any = None
    transformed_policy_target_applied: bool = False


class AgentControl:
    @classmethod
    def from_path(cls, path: str) -> "AgentControl":
        raise RuntimeError("native ACS is not available in the unit-test stub")


class HostSession:
    def __init__(
        self,
        control: Any,
        *,
        agent_id: str,
        session_id: str,
        mode: EnforcementMode | str,
    ) -> None:
        self.control = control
        self.agent_id = agent_id
        self.session_id = session_id
        self.mode = EnforcementMode(mode)

    def pre_tool_call(
        self, *, tool_name: str, args: Any, call_id: str
    ) -> InterventionPointResult:
        snapshot = {
            "tool_call": {"name": tool_name, "args": args, "id": call_id},
            "envelope": {
                "agent": {"id": self.agent_id},
                "session": {"id": self.session_id},
                "intervention_point": "pre_tool_call",
            },
        }
        coroutine = self.control.evaluate_intervention_point(
            InterventionPoint.PRE_TOOL_CALL, snapshot, self.mode
        )
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(coroutine)
        outcome: dict[str, Any] = {}

        def run() -> None:
            try:
                outcome["value"] = asyncio.run(coroutine)
            except BaseException as exc:
                outcome["error"] = exc

        thread = threading.Thread(target=run)
        thread.start()
        thread.join()
        if "error" in outcome:
            raise outcome["error"]
        return outcome["value"]


module = types.ModuleType("agent_control_specification")
for name, value in {
    "AgentControl": AgentControl,
    "Decision": Decision,
    "EnforcementMode": EnforcementMode,
    "HostSession": HostSession,
    "InterventionPointResult": InterventionPointResult,
    "Transform": Transform,
    "Verdict": Verdict,
}.items():
    setattr(module, name, value)
sys.modules.setdefault("agent_control_specification", module)
