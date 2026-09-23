package com.agentic.orchestrator.workflow;

public enum TaskState {
    BACKLOG,
    READY,
    IN_PROGRESS,
    CODE_REVIEW,
    CHANGES_REQUESTED,
    MERGED,
    TESTING,
    BUG,
    READY_FOR_DEPLOY,
    DEPLOYING,
    RELEASED,
    BLOCKED
}
