# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import sys
from types import ModuleType, SimpleNamespace

from agt_evidence import CorrelationContext, capture_current_correlation


def test_capture_current_correlation_formats_w3c_ids(monkeypatch) -> None:
    span_context = SimpleNamespace(
        is_valid=True,
        trace_id=0x4BF92F3577B34DA6A3CE929D0E0E4736,
        span_id=0x00F067AA0BA902B7,
        trace_flags=1,
    )
    trace = SimpleNamespace(
        get_current_span=lambda: SimpleNamespace(
            get_span_context=lambda: span_context
        )
    )
    module = ModuleType("opentelemetry")
    module.trace = trace
    monkeypatch.setitem(sys.modules, "opentelemetry", module)

    assert capture_current_correlation() == CorrelationContext(
        trace_id="4bf92f3577b34da6a3ce929d0e0e4736",
        span_id="00f067aa0ba902b7",
        trace_flags=1,
    )


def test_capture_current_correlation_ignores_invalid_context(monkeypatch) -> None:
    trace = SimpleNamespace(
        get_current_span=lambda: SimpleNamespace(
            get_span_context=lambda: SimpleNamespace(is_valid=False)
        )
    )
    module = ModuleType("opentelemetry")
    module.trace = trace
    monkeypatch.setitem(sys.modules, "opentelemetry", module)

    assert capture_current_correlation() is None
