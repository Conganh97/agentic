package com.agentic.orchestrator.agent;

import com.agentic.orchestrator.domain.AgentRole;
import com.agentic.orchestrator.domain.Task;
import java.util.Map;
import java.util.Objects;

/** Built by the Orchestrator. {@code task} is an immutable snapshot; agents cannot change its state. */
public record AgentRequest(String executionId, AgentRole agent, Task task, Map<String, String> inputs) {

    public AgentRequest {
        Objects.requireNonNull(executionId, "executionId");
        Objects.requireNonNull(agent, "agent");
        Objects.requireNonNull(task, "task");
        inputs = inputs == null ? Map.of() : Map.copyOf(inputs);
    }
}
