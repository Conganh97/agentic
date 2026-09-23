package com.agentic.orchestrator.workflow;

import static com.agentic.orchestrator.workflow.TaskState.BACKLOG;
import static com.agentic.orchestrator.workflow.TaskState.BLOCKED;
import static com.agentic.orchestrator.workflow.TaskState.BUG;
import static com.agentic.orchestrator.workflow.TaskState.CHANGES_REQUESTED;
import static com.agentic.orchestrator.workflow.TaskState.CODE_REVIEW;
import static com.agentic.orchestrator.workflow.TaskState.DEPLOYING;
import static com.agentic.orchestrator.workflow.TaskState.IN_PROGRESS;
import static com.agentic.orchestrator.workflow.TaskState.MERGED;
import static com.agentic.orchestrator.workflow.TaskState.READY;
import static com.agentic.orchestrator.workflow.TaskState.READY_FOR_DEPLOY;
import static com.agentic.orchestrator.workflow.TaskState.RELEASED;
import static com.agentic.orchestrator.workflow.TaskState.TESTING;
import static java.util.Map.entry;

import java.util.Map;
import java.util.Set;

/**
 * Deterministic transition rules for {@link TaskState}.
 *
 * <p>BLOCKED is never reached or left through the transition table: entering it requires an explicit
 * block from a blockable state, and leaving it requires an explicit unblock back to the previous state.
 */
public final class TaskStateMachine {

    private static final Map<TaskState, Set<TaskState>> TRANSITIONS = Map.ofEntries(
            entry(BACKLOG, Set.of(READY)),
            entry(READY, Set.of(IN_PROGRESS)),
            entry(IN_PROGRESS, Set.of(CODE_REVIEW)),
            entry(CODE_REVIEW, Set.of(CHANGES_REQUESTED, MERGED)),
            entry(CHANGES_REQUESTED, Set.of(IN_PROGRESS)),
            entry(MERGED, Set.of(TESTING)),
            entry(TESTING, Set.of(BUG, READY_FOR_DEPLOY)),
            entry(BUG, Set.of(IN_PROGRESS)),
            entry(READY_FOR_DEPLOY, Set.of(DEPLOYING)),
            entry(DEPLOYING, Set.of(RELEASED)),
            entry(RELEASED, Set.of()),
            entry(BLOCKED, Set.of()));

    private static final Set<TaskState> BLOCKABLE = Set.of(
            READY, IN_PROGRESS, CODE_REVIEW, CHANGES_REQUESTED, MERGED,
            TESTING, BUG, READY_FOR_DEPLOY, DEPLOYING);

    private TaskStateMachine() {
    }

    public static Set<TaskState> allowedTargets(TaskState from) {
        return TRANSITIONS.get(from);
    }

    public static boolean canTransition(TaskState from, TaskState to) {
        return TRANSITIONS.get(from).contains(to);
    }

    public static void requireTransition(TaskState from, TaskState to) {
        if (from == BLOCKED) {
            throw new InvalidTransitionException("Task is BLOCKED; it must be explicitly unblocked first");
        }
        if (to == BLOCKED) {
            throw new InvalidTransitionException("BLOCKED can only be entered through an explicit block action");
        }
        if (!canTransition(from, to)) {
            throw InvalidTransitionException.notAllowed(from, to);
        }
    }

    public static boolean canBlock(TaskState from) {
        return BLOCKABLE.contains(from);
    }
}
