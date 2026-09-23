package com.agentic.orchestrator.agent;

public record ReviewComment(String file, ReviewSeverity severity, String message) {
}
