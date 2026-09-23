package com.agentic.orchestrator.agent;

/** Error details, required when the status is FAILED, NEEDS_INPUT or BLOCKED. */
public record AgentError(String code, String message) {
}
