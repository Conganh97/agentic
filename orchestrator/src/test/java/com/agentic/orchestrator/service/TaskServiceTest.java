package com.agentic.orchestrator.service;

import static com.agentic.orchestrator.workflow.TaskState.BLOCKED;
import static com.agentic.orchestrator.workflow.TaskState.BUG;
import static com.agentic.orchestrator.workflow.TaskState.CHANGES_REQUESTED;
import static com.agentic.orchestrator.workflow.TaskState.CODE_REVIEW;
import static com.agentic.orchestrator.workflow.TaskState.IN_PROGRESS;
import static com.agentic.orchestrator.workflow.TaskState.MERGED;
import static com.agentic.orchestrator.workflow.TaskState.READY;
import static com.agentic.orchestrator.workflow.TaskState.TESTING;
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import com.agentic.orchestrator.domain.NewTask;
import com.agentic.orchestrator.domain.Priority;
import com.agentic.orchestrator.domain.Task;
import com.agentic.orchestrator.domain.TaskType;
import com.agentic.orchestrator.repository.InMemoryTaskRepository;
import com.agentic.orchestrator.workflow.InvalidTransitionException;
import com.agentic.orchestrator.workflow.TaskState;
import java.time.Clock;
import java.time.Instant;
import java.time.ZoneOffset;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class TaskServiceTest {

    private static final Instant NOW = Instant.parse("2026-01-01T00:00:00Z");

    private TaskService service;

    @BeforeEach
    void setUp() {
        service = new TaskService(new InMemoryTaskRepository(), Clock.fixed(NOW, ZoneOffset.UTC),
                new WorkflowLimits(2, 1));
    }

    private Task createTask() {
        return service.create(NewTask.of("Login API", TaskType.STORY, Priority.HIGH, List.of("ac")));
    }

    private Task walk(String id, TaskState... states) {
        Task current = null;
        for (TaskState state : states) {
            current = service.transition(id, state);
        }
        return current;
    }

    @Test
    void createAssignsSequentialIdsAndPersists() {
        Task first = createTask();
        Task second = createTask();

        assertThat(first.id()).isEqualTo("TASK-1");
        assertThat(second.id()).isEqualTo("TASK-2");
        assertThat(service.get("TASK-1").createdAt()).isEqualTo(NOW);
    }

    @Test
    void transitionPersistsNewState() {
        String id = createTask().id();

        service.transition(id, READY);

        assertThat(service.get(id).status()).isEqualTo(READY);
    }

    @Test
    void invalidTransitionDoesNotChangePersistedState() {
        String id = createTask().id();

        assertThatThrownBy(() -> service.transition(id, MERGED)).isInstanceOf(InvalidTransitionException.class);
        assertThat(service.get(id).status()).isEqualTo(TaskState.BACKLOG);
    }

    @Test
    void unknownTaskIsReported() {
        assertThatThrownBy(() -> service.get("TASK-404")).isInstanceOf(TaskNotFoundException.class);
        assertThatThrownBy(() -> service.transition("TASK-404", READY)).isInstanceOf(TaskNotFoundException.class);
    }

    @Test
    void exceedingReviewLimitBlocksTask() {
        String id = createTask().id();
        walk(id, READY, IN_PROGRESS, CODE_REVIEW, CHANGES_REQUESTED, IN_PROGRESS,
                CODE_REVIEW, CHANGES_REQUESTED, IN_PROGRESS, CODE_REVIEW);

        Task result = service.transition(id, CHANGES_REQUESTED);

        assertThat(result.status()).isEqualTo(BLOCKED);
        assertThat(result.blockedFrom()).contains(CODE_REVIEW);
        assertThat(result.blockReason()).hasValueSatisfying(r -> assertThat(r).contains("Review iteration limit"));
        assertThat(result.reviewIteration()).isEqualTo(2);
        assertThat(service.get(id).status()).isEqualTo(BLOCKED);
    }

    @Test
    void reviewWithinLimitIsAllowed() {
        String id = createTask().id();
        Task result = walk(id, READY, IN_PROGRESS, CODE_REVIEW, CHANGES_REQUESTED, IN_PROGRESS,
                CODE_REVIEW, CHANGES_REQUESTED);

        assertThat(result.status()).isEqualTo(CHANGES_REQUESTED);
        assertThat(result.reviewIteration()).isEqualTo(2);
    }

    @Test
    void exceedingTestLimitBlocksTask() {
        String id = createTask().id();
        walk(id, READY, IN_PROGRESS, CODE_REVIEW, MERGED, TESTING, BUG, IN_PROGRESS, CODE_REVIEW, MERGED, TESTING);

        Task result = service.transition(id, BUG);

        assertThat(result.status()).isEqualTo(BLOCKED);
        assertThat(result.blockedFrom()).contains(TESTING);
        assertThat(result.blockReason()).hasValueSatisfying(r -> assertThat(r).contains("Test iteration limit"));
    }

    @Test
    void blockAndUnblockThroughService() {
        String id = createTask().id();
        walk(id, READY, IN_PROGRESS);

        assertThat(service.block(id, "Waiting for design").status()).isEqualTo(BLOCKED);
        assertThat(service.unblock(id).status()).isEqualTo(IN_PROGRESS);
        assertThat(service.get(id).status()).isEqualTo(IN_PROGRESS);
    }

    @Test
    void limitsMustBePositive() {
        assertThatThrownBy(() -> new WorkflowLimits(0, 1)).isInstanceOf(IllegalArgumentException.class);
        assertThatThrownBy(() -> new WorkflowLimits(1, 0)).isInstanceOf(IllegalArgumentException.class);
    }
}
