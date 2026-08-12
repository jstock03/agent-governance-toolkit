# Agent Governance Python

This directory is the top-level home for first-party published Python packages in the
Agent Governance Toolkit repository.

It exists to give Python the same contributor-facing repository shape as other standalone language
surfaces such as `agent-governance-dotnet/` and `agent-governance-golang/`, while still allowing
Python to publish multiple focused distributions instead of a single monolithic SDK package.

## Installing

The base meta-package installs the compliance CLI. Add an extra when you need
the governance runtime, framework integrations, or the full Python stack:

```
# Compliance CLI only
pip install agent-governance-toolkit

# Framework integrations
pip install agent-governance-toolkit[langchain]
pip install agent-governance-toolkit[crewai]
pip install agent-governance-toolkit[openai-agents]

# Full Python governance stack, including agentmesh and legacy agent_os compatibility
pip install agent-governance-toolkit[full]
```

Durable audit and deployment evidence is also available independently:

```
pip install agt-evidence
```

`agent_os` is the legacy compatibility import from the old `agent-os-kernel`
surface. It currently emits a `DeprecationWarning`; use
`agent-governance-toolkit-core` (or the `[full]` extra) as the replacement
distribution, and prefer `agt-policies`/ACS APIs for new policy-engine host code.

If you only need a specific component, each package can also be installed on its own. See the package listing below for names.

## Scope

This directory is for published Python SDK and package surfaces, reusable foundational Python packages, and package-specific tests, metadata, and documentation.

It is not for applications or dashboards, demos or examples, monorepo-only product composition code, or framework-specific integration packages that are not part of the core first-party Python package story. Those surfaces belong in the repo root, `examples/`, `examples/demos/`, or other existing homes.

## Package Overview

**Core packages** are the runtime kernel, execution supervisor, sandbox, SRE layer, and shared primitives. Most users need only the meta-package or `agent-governance-toolkit-core` once the consolidation in issue #2482 lands.

**Framework integrations** live under `agentmesh-integrations/` and each wraps a specific framework like LangChain, CrewAI, LlamaIndex, or Haystack with AGT governance middleware.

**Agent OS modules** under `agent-os/modules/` are internal kernel primitives. They are not published to PyPI and are not intended for direct external consumption at this time.

## Current Packages

`agt-evidence/`, `agent-compliance/`, `agent-discovery/`, `agent-hypervisor/`, `agent-lightning/`, `agent-marketplace/`, `agent-mcp-governance/`, `agent-mesh/`, `agent-os/`, `agent-primitives/`, `agent-rag-governance/`, `agent-runtime/`, `agent-sandbox/`, `agent-sre/`, `agentmesh-integrations/`

## Package consolidation

The earlier consolidation reduced the Python surface to
`agent-governance-toolkit-core`, `agent-governance-toolkit-integrations`,
`agent-governance-toolkit-cli`, `agent-governance-toolkit-protocols`, and the
toolkit meta-package. `agt-evidence` starts the next boundary pass by extracting
durable governance evidence from the core runtime while preserving legacy
imports. The earlier plan, audit data, and migration guide remain in
`docs/package-consolidation/`.
