package com.agentic.orchestrator.agent;

import java.util.List;

/** SA analysis of a requirement: design summary, task breakdown and technical risks. */
public record DesignResult(String summary, List<ProposedTask> tasks, List<String> risks) implements AgentResult {

    public DesignResult {
        tasks = tasks == null ? List.of() : List.copyOf(tasks);
        risks = risks == null ? List.of() : List.copyOf(risks);
    }
}
