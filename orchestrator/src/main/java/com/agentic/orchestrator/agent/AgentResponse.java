package com.agentic.orchestrator.agent;

import com.agentic.orchestrator.domain.AgentRole;

/**
 * Untrusted agent output. It is only acted on after {@link AgentResponseValidator} reports no violations.
 */
public record AgentResponse(
        String executionId,
        AgentRole agent,
        String taskId,
        AgentStatus status,
        AgentResult result,
        AgentError error) {

    public static AgentResponse completed(AgentRequest request, AgentResult result) {
        return of(request, AgentStatus.COMPLETED, result, null);
    }

    public static AgentResponse changesRequested(AgentRequest request, ReviewResult result) {
        return of(request, AgentStatus.CHANGES_REQUESTED, result, null);
    }

    public static AgentResponse failed(AgentRequest request, String code, String message) {
        return of(request, AgentStatus.FAILED, null, new AgentError(code, message));
    }

    public static AgentResponse needsInput(AgentRequest request, String code, String message) {
        return of(request, AgentStatus.NEEDS_INPUT, null, new AgentError(code, message));
    }

    public static AgentResponse blocked(AgentRequest request, String code, String message) {
        return of(request, AgentStatus.BLOCKED, null, new AgentError(code, message));
    }

    private static AgentResponse of(AgentRequest request, AgentStatus status, AgentResult result, AgentError error) {
        return new AgentResponse(request.executionId(), request.agent(), request.task().id(), status, result, error);
    }
}
