package com.agentic.orchestrator.service;

/**
 * Maximum number of CHANGES_REQUESTED rounds and BUG rounds a task may go through before it is blocked
 * for human intervention.
 */
public record WorkflowLimits(int maxReviewIterations, int maxTestIterations) {

    public static final WorkflowLimits DEFAULT = new WorkflowLimits(3, 3);

    public WorkflowLimits {
        if (maxReviewIterations < 1 || maxTestIterations < 1) {
            throw new IllegalArgumentException("limits must be >= 1");
        }
    }
}
