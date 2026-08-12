# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Optional OpenTelemetry correlation helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CorrelationContext:
    """W3C trace identifiers that correlate evidence with operational telemetry."""

    trace_id: str
    span_id: str
    trace_flags: int


def capture_current_correlation() -> CorrelationContext | None:
    """Return the active OpenTelemetry trace context when one is available."""
    try:
        from opentelemetry import trace
    except ImportError:
        return None

    span_context = trace.get_current_span().get_span_context()
    if not span_context.is_valid:
        return None

    return CorrelationContext(
        trace_id=f"{span_context.trace_id:032x}",
        span_id=f"{span_context.span_id:016x}",
        trace_flags=int(span_context.trace_flags),
    )
