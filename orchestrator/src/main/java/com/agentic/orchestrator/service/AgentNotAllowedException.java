package com.agentic.orchestrator.service;

import com.agentic.orchestrator.domain.AgentRole;
import com.agentic.orchestrator.workflow.TaskState;

public class AgentNotAllowedException extends RuntimeException {

    public AgentNotAllowedException(AgentRole role, String taskId, TaskState state) {
        super("Agent " + role + " is not allowed to work on " + taskId + " in state " + state);
    }
}
