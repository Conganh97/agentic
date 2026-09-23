package com.agentic.orchestrator.agent;

/** Structured result schemas an agent can return. */
public sealed interface AgentResult permits DesignResult, ImplementationResult, ReviewResult {
}
