package com.agentic.orchestrator.service;

import com.agentic.orchestrator.agent.AgentResponse;
import com.agentic.orchestrator.domain.AgentRole;
import com.agentic.orchestrator.workflow.TaskState;
import java.time.Instant;
import java.util.List;

/**
 * Audit record of one agent execution. {@code response} is the effective response: when the agent threw
 * or returned an invalid response, it is a synthesized FAILED response and {@code violations} explains why.
 */
public record AgentExecution(
        String executionId,
        AgentRole agent,
        String taskId,
        Instant startedAt,
        Instant finishedAt,
        AgentResponse response,
        List<String> violations,
        TaskState stateBefore,
        TaskState stateAfter) {

    public AgentExecution {
        violations = List.copyOf(violations);
    }

    public boolean accepted() {
        return violations.isEmpty();
    }
}
