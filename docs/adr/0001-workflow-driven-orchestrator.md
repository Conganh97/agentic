# ADR-0001: Workflow-driven Orchestrator with a minimal Java stack

- **Status:** Accepted
- **Date:** 2026-09-23
- **Deciders:** Project owner

## Context

We are building an agentic engineering team (Scrum, SA, BE, FE, Test, DevOps). Letting agents
collaborate free-form makes the process non-deterministic, hard to audit, and allows agents to
skip reviews, merge their own code, or deploy without approval.

We also need to move fast in early phases without committing to heavy infrastructure.
The team's primary expertise is Java, not Python.

## Decision

1. **The Orchestrator owns workflow state.** Task state changes only through Orchestrator-validated
   transitions of an explicit state machine. Agents are stateless workers that return structured,
   schema-validated results; they never set state directly.
2. **Structured contracts, not free-form text,** drive every workflow decision.
3. **Guardrails are enforced by the platform,** not by agent prompts: retry limits, approval gates,
   per-agent tool permissions.
4. **Java for both the Orchestrator and the agent runtime:** Java 21, Maven, Spring Boot
   (application layer only), JUnit 5 + AssertJ. `domain` and `workflow` stay pure Java.
5. **Minimal infrastructure:** in-memory persistence first, then H2 locally / PostgreSQL.
   Kafka, Redis, Temporal, and Kubernetes are introduced only when a phase requires them,
   each with its own ADR.
6. The LLM client library (e.g. Spring AI or LangChain4j) is chosen in Phase 3 (SA Agent) with a
   separate ADR.

## Consequences

**Positive**
- Deterministic, testable, auditable workflow.
- Agents can be replaced or improved independently of the workflow.
- One language across the platform, matching team expertise and the planned production stack
  (Java/Spring), so no later rewrite from Python.

**Negative / risks**
- The Orchestrator is a central component and must be well tested.
- Java's LLM/agent ecosystem is smaller than Python's; some integrations may need more code.
- More boilerplate and slower experimentation than Python.

## Alternatives considered

- **Python agent runtime + Java platform** — rejected: team is not fluent in Python; two stacks
  to maintain.
- **Free-form multi-agent chat** — rejected: non-deterministic, weak auditability, bypass risk.
- **Full production stack from day one (Kafka, Temporal, Kubernetes)** — rejected for now:
  premature complexity before the MVP loop is proven.
