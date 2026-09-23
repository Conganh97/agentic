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
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatCode;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.ArrayList;
import java.util.EnumSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Stream;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.EnumSource;
import org.junit.jupiter.params.provider.MethodSource;

class TaskStateMachineTest {

    private static final List<TaskState[]> ALLOWED = List.of(
            new TaskState[] {BACKLOG, READY},
            new TaskState[] {READY, IN_PROGRESS},
            new TaskState[] {IN_PROGRESS, CODE_REVIEW},
            new TaskState[] {CODE_REVIEW, CHANGES_REQUESTED},
            new TaskState[] {CODE_REVIEW, MERGED},
            new TaskState[] {CHANGES_REQUESTED, IN_PROGRESS},
            new TaskState[] {MERGED, TESTING},
            new TaskState[] {TESTING, BUG},
            new TaskState[] {TESTING, READY_FOR_DEPLOY},
            new TaskState[] {BUG, IN_PROGRESS},
            new TaskState[] {READY_FOR_DEPLOY, DEPLOYING},
            new TaskState[] {DEPLOYING, RELEASED});

    static Stream<Arguments> allowedTransitions() {
        return ALLOWED.stream().map(pair -> Arguments.of(pair[0], pair[1]));
    }

    static Stream<Arguments> disallowedTransitions() {
        List<Arguments> result = new ArrayList<>();
        for (TaskState from : TaskState.values()) {
            for (TaskState to : TaskState.values()) {
                boolean allowed = ALLOWED.stream().anyMatch(p -> p[0] == from && p[1] == to);
                if (!allowed) {
                    result.add(Arguments.of(from, to));
                }
            }
        }
        return result.stream();
    }

    @ParameterizedTest(name = "{0} -> {1} is allowed")
    @MethodSource("allowedTransitions")
    void allowedTransitionsPass(TaskState from, TaskState to) {
        assertThat(TaskStateMachine.canTransition(from, to)).isTrue();
        assertThatCode(() -> TaskStateMachine.requireTransition(from, to)).doesNotThrowAnyException();
    }

    @ParameterizedTest(name = "{0} -> {1} is rejected")
    @MethodSource("disallowedTransitions")
    void disallowedTransitionsAreRejected(TaskState from, TaskState to) {
        assertThat(TaskStateMachine.canTransition(from, to)).isFalse();
        assertThatThrownBy(() -> TaskStateMachine.requireTransition(from, to))
                .isInstanceOf(InvalidTransitionException.class);
    }

    @ParameterizedTest(name = "{0} -> {1} is rejected (plan example)")
    @CsvSource({
        "BACKLOG, MERGED",
        "BACKLOG, RELEASED",
        "IN_PROGRESS, RELEASED",
        "CODE_REVIEW, RELEASED",
        "TESTING, RELEASED"
    })
    void planDisallowedExamplesAreRejected(TaskState from, TaskState to) {
        assertThatThrownBy(() -> TaskStateMachine.requireTransition(from, to))
                .isInstanceOf(InvalidTransitionException.class)
                .hasMessageContaining(from + " -> " + to);
    }

    @ParameterizedTest
    @EnumSource(TaskState.class)
    void everyStateHasADefinedTargetSet(TaskState state) {
        assertThat(TaskStateMachine.allowedTargets(state)).isNotNull();
    }

    @Test
    void terminalAndBlockedStatesHaveNoTableTransitions() {
        assertThat(TaskStateMachine.allowedTargets(RELEASED)).isEmpty();
        assertThat(TaskStateMachine.allowedTargets(BLOCKED)).isEmpty();
    }

    @Test
    void blockedCannotBeEnteredOrLeftThroughTransitions() {
        assertThatThrownBy(() -> TaskStateMachine.requireTransition(IN_PROGRESS, BLOCKED))
                .isInstanceOf(InvalidTransitionException.class)
                .hasMessageContaining("explicit block");
        assertThatThrownBy(() -> TaskStateMachine.requireTransition(BLOCKED, IN_PROGRESS))
                .isInstanceOf(InvalidTransitionException.class)
                .hasMessageContaining("unblocked");
    }

    @Test
    void onlyWorkingStatesAreBlockable() {
        Set<TaskState> blockable = EnumSet.noneOf(TaskState.class);
        for (TaskState state : TaskState.values()) {
            if (TaskStateMachine.canBlock(state)) {
                blockable.add(state);
            }
        }
        assertThat(blockable).containsExactlyInAnyOrder(
                READY, IN_PROGRESS, CODE_REVIEW, CHANGES_REQUESTED, MERGED,
                TESTING, BUG, READY_FOR_DEPLOY, DEPLOYING);
    }
}
