package com.agentic.orchestrator.domain;

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
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import com.agentic.orchestrator.workflow.InvalidTransitionException;
import com.agentic.orchestrator.workflow.TaskState;
import java.time.Instant;
import java.util.List;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.EnumSource;

class TaskTest {

    private static final Instant T0 = Instant.parse("2026-01-01T00:00:00Z");
    private static final Instant T1 = Instant.parse("2026-01-01T01:00:00Z");

    private static Task newTask() {
        return Task.create("TASK-1", NewTask.of("Login API", TaskType.STORY, Priority.HIGH,
                List.of("User can log in with valid credentials")), T0);
    }

    private static Task walk(Task task, TaskState... states) {
        Task current = task;
        for (TaskState state : states) {
            current = current.transitionTo(state, T1);
        }
        return current;
    }

    @Test
    void createStartsInBacklogWithZeroIterations() {
        Task task = newTask();

        assertThat(task.status()).isEqualTo(BACKLOG);
        assertThat(task.reviewIteration()).isZero();
        assertThat(task.testIteration()).isZero();
        assertThat(task.createdAt()).isEqualTo(T0);
        assertThat(task.updatedAt()).isEqualTo(T0);
        assertThat(task.blockedFrom()).isEmpty();
    }

    @Test
    void createRejectsBlankId() {
        NewTask details = NewTask.of("t", TaskType.TASK, Priority.LOW, List.of("ac"));
        assertThatThrownBy(() -> Task.create(" ", details, T0)).isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void transitionReturnsNewTaskAndLeavesOriginalUnchanged() {
        Task original = newTask();

        Task ready = original.transitionTo(READY, T1);

        assertThat(ready.status()).isEqualTo(READY);
        assertThat(ready.updatedAt()).isEqualTo(T1);
        assertThat(ready.createdAt()).isEqualTo(T0);
        assertThat(original.status()).isEqualTo(BACKLOG);
        assertThat(original.updatedAt()).isEqualTo(T0);
    }

    @Test
    void invalidTransitionIsRejected() {
        assertThatThrownBy(() -> newTask().transitionTo(MERGED, T1))
                .isInstanceOf(InvalidTransitionException.class);
    }

    @Test
    void cannotBecomeReadyWithoutAcceptanceCriteria() {
        Task task = Task.create("TASK-2", NewTask.of("t", TaskType.TASK, Priority.LOW, List.of()), T0);

        assertThatThrownBy(() -> task.transitionTo(READY, T1)).isInstanceOf(TaskNotReadyException.class);
    }

    @Test
    void happyPathReachesReleased() {
        Task released = walk(newTask(), READY, IN_PROGRESS, CODE_REVIEW, MERGED, TESTING,
                READY_FOR_DEPLOY, DEPLOYING, RELEASED);

        assertThat(released.status()).isEqualTo(RELEASED);
        assertThat(released.reviewIteration()).isZero();
        assertThat(released.testIteration()).isZero();
    }

    @Test
    void reviewLoopIncrementsReviewIteration() {
        Task task = walk(newTask(), READY, IN_PROGRESS, CODE_REVIEW, CHANGES_REQUESTED, IN_PROGRESS,
                CODE_REVIEW, CHANGES_REQUESTED, IN_PROGRESS, CODE_REVIEW, MERGED);

        assertThat(task.status()).isEqualTo(MERGED);
        assertThat(task.reviewIteration()).isEqualTo(2);
    }

    @Test
    void bugLoopIncrementsTestIteration() {
        Task task = walk(newTask(), READY, IN_PROGRESS, CODE_REVIEW, MERGED, TESTING, BUG, IN_PROGRESS,
                CODE_REVIEW, MERGED, TESTING, READY_FOR_DEPLOY);

        assertThat(task.status()).isEqualTo(READY_FOR_DEPLOY);
        assertThat(task.testIteration()).isEqualTo(1);
    }

    @Test
    void blockAndUnblockReturnsToPreviousState() {
        Task inProgress = walk(newTask(), READY, IN_PROGRESS);

        Task blocked = inProgress.block("Waiting for API contract", T1);
        assertThat(blocked.status()).isEqualTo(BLOCKED);
        assertThat(blocked.blockedFrom()).contains(IN_PROGRESS);
        assertThat(blocked.blockReason()).contains("Waiting for API contract");

        Task unblocked = blocked.unblock(T1);
        assertThat(unblocked.status()).isEqualTo(IN_PROGRESS);
        assertThat(unblocked.blockedFrom()).isEmpty();
        assertThat(unblocked.blockReason()).isEmpty();
    }

    @Test
    void blockPreservesIterations() {
        Task task = walk(newTask(), READY, IN_PROGRESS, CODE_REVIEW, CHANGES_REQUESTED);

        Task roundTrip = task.block("reason", T1).unblock(T1);

        assertThat(roundTrip.reviewIteration()).isEqualTo(1);
    }

    @ParameterizedTest
    @EnumSource(value = TaskState.class, names = {"BACKLOG", "RELEASED"})
    void nonWorkingStatesCannotBeBlocked(TaskState state) {
        Task task = state == BACKLOG ? newTask()
                : walk(newTask(), READY, IN_PROGRESS, CODE_REVIEW, MERGED, TESTING, READY_FOR_DEPLOY,
                        DEPLOYING, RELEASED);

        assertThatThrownBy(() -> task.block("reason", T1)).isInstanceOf(InvalidTransitionException.class);
    }

    @Test
    void blockedTaskCannotBeBlockedAgain() {
        Task blocked = walk(newTask(), READY).block("reason", T1);

        assertThatThrownBy(() -> blocked.block("again", T1)).isInstanceOf(InvalidTransitionException.class);
    }

    @Test
    void blockedTaskCannotTransitionWithoutUnblock() {
        Task blocked = walk(newTask(), READY).block("reason", T1);

        assertThatThrownBy(() -> blocked.transitionTo(IN_PROGRESS, T1))
                .isInstanceOf(InvalidTransitionException.class);
    }

    @Test
    void transitionToBlockedIsRejected() {
        Task ready = walk(newTask(), READY);

        assertThatThrownBy(() -> ready.transitionTo(BLOCKED, T1)).isInstanceOf(InvalidTransitionException.class);
    }

    @Test
    void unblockRequiresBlockedState() {
        assertThatThrownBy(() -> newTask().unblock(T1)).isInstanceOf(InvalidTransitionException.class);
    }

    @Test
    void blockRequiresReason() {
        Task ready = walk(newTask(), READY);

        assertThatThrownBy(() -> ready.block(" ", T1)).isInstanceOf(IllegalArgumentException.class);
    }
}
