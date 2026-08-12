# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
"""Durable governance evidence contracts for AGT."""

from .audit import (
    AuditChain,
    AuditEntry,
    AuditLog,
    ChainNode,
    MerkleAuditChain,
    MerkleNode,
)
from .backends import (
    AuditSink,
    FileAuditSink,
    HashChainVerifier,
    SignedAuditEntry,
    StdoutAuditSink,
)
from .correlation import CorrelationContext, capture_current_correlation
from .runtime import EVIDENCE_SCHEMA, RuntimeEvidence

__all__ = [
    "AuditChain",
    "AuditEntry",
    "AuditLog",
    "AuditSink",
    "ChainNode",
    "CorrelationContext",
    "EVIDENCE_SCHEMA",
    "FileAuditSink",
    "HashChainVerifier",
    "MerkleAuditChain",
    "MerkleNode",
    "RuntimeEvidence",
    "SignedAuditEntry",
    "StdoutAuditSink",
    "capture_current_correlation",
]
