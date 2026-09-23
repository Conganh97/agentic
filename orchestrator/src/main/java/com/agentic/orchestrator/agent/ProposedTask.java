package com.agentic.orchestrator.agent;

import com.agentic.orchestrator.domain.AgentRole;
import com.agentic.orchestrator.domain.Priority;
import com.agentic.orchestrator.domain.TaskType;
import java.util.List;

public record ProposedTask(
        String title,
        String description,
        TaskType type,
        Priority priority,
        AgentRole assigneeAgent,
        List<String> acceptanceCriteria) {

    public ProposedTask {
        acceptanceCriteria = acceptanceCriteria == null ? List.of() : List.copyOf(acceptanceCriteria);
    }
}
