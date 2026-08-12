# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Compatibility aliases for audit sinks now owned by agt-evidence."""

from agt_evidence.backends import (
    AuditSink,
    FileAuditSink,
    HashChainVerifier,
    SignedAuditEntry,
    StdoutAuditSink,
)

__all__ = [
    "AuditSink",
    "FileAuditSink",
    "HashChainVerifier",
    "SignedAuditEntry",
    "StdoutAuditSink",
]
