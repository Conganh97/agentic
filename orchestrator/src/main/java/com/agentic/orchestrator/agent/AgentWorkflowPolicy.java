package com.agentic.orchestrator.agent;

import static com.agentic.orchestrator.domain.AgentRole.BE;
import static com.agentic.orchestrator.domain.AgentRole.FE;
import static com.agentic.orchestrator.domain.AgentRole.SA;

import com.agentic.orchestrator.domain.AgentRole;
import com.agentic.orchestrator.workflow.TaskState;
import java.util.Map;
import java.util.Optional;
import java.util.Set;

/**
 * Which agents may work on a task in a given state, which result schema they must return, and which
 * transition the Orchestrator applies on COMPLETED. States without a step accept no agent work.
 */
public final class AgentWorkflowPolicy {

    public record Step(Set<AgentRole> roles, Class<? extends AgentResult> resultType,
                       Optional<TaskState> onCompleted) {
    }

    private static final Map<TaskState, Step> STEPS = Map.of(
            TaskState.BACKLOG, new Step(Set.of(SA), DesignResult.class, Optional.empty()),
            TaskState.IN_PROGRESS, new Step(Set.of(BE, FE), ImplementationResult.class,
                    Optional.of(TaskState.CODE_REVIEW)),
            // Approval moves straight to MERGED until Git integration performs the real merge (Phase 6).
            TaskState.CODE_REVIEW, new Step(Set.of(SA), ReviewResult.class, Optional.of(TaskState.MERGED)));

    private AgentWorkflowPolicy() {
    }

    public static Optional<Step> stepFor(TaskState state) {
        return Optional.ofNullable(STEPS.get(state));
    }

    public static boolean canExecute(AgentRole role, TaskState state) {
        return stepFor(state).map(step -> step.roles().contains(role)).orElse(false);
    }
}
