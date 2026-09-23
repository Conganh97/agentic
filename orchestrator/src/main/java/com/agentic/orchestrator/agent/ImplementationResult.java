package com.agentic.orchestrator.agent;

import java.util.List;

/** BE/FE implementation outcome. {@code pullRequest} may be null until Git integration exists. */
public record ImplementationResult(String summary, String branch, String pullRequest, List<String> changedFiles)
        implements AgentResult {

    public ImplementationResult {
        changedFiles = changedFiles == null ? List.of() : List.copyOf(changedFiles);
    }
}
