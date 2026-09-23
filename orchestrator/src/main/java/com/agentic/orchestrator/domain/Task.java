package com.agentic.orchestrator.domain;

import com.agentic.orchestrator.workflow.InvalidTransitionException;
import com.agentic.orchestrator.workflow.TaskState;
import com.agentic.orchestrator.workflow.TaskStateMachine;
import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;

/**
 * Immutable task aggregate. Status can only change through {@link #transitionTo}, {@link #block} and
 * {@link #unblock}, all of which are validated by {@link TaskStateMachine}.
 */
public final class Task {

    private final String id;
    private final NewTask details;
    private final TaskState status;
    private final int reviewIteration;
    private final int testIteration;
    private final TaskState blockedFrom;
    private final String blockReason;
    private final Instant createdAt;
    private final Instant updatedAt;

    private Task(String id, NewTask details, TaskState status, int reviewIteration, int testIteration,
                 TaskState blockedFrom, String blockReason, Instant createdAt, Instant updatedAt) {
        this.id = id;
        this.details = details;
        this.status = status;
        this.reviewIteration = reviewIteration;
        this.testIteration = testIteration;
        this.blockedFrom = blockedFrom;
        this.blockReason = blockReason;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
    }

    public static Task create(String id, NewTask details, Instant now) {
        if (id == null || id.isBlank()) {
            throw new IllegalArgumentException("id must not be blank");
        }
        Objects.requireNonNull(details, "details");
        Objects.requireNonNull(now, "now");
        return new Task(id, details, TaskState.BACKLOG, 0, 0, null, null, now, now);
    }

    public Task transitionTo(TaskState target, Instant at) {
        Objects.requireNonNull(target, "target");
        Objects.requireNonNull(at, "at");
        TaskStateMachine.requireTransition(status, target);
        if (target == TaskState.READY && details.acceptanceCriteria().isEmpty()) {
            throw new TaskNotReadyException("Task " + id + " has no acceptance criteria");
        }
        int nextReview = target == TaskState.CHANGES_REQUESTED ? reviewIteration + 1 : reviewIteration;
        int nextTest = target == TaskState.BUG ? testIteration + 1 : testIteration;
        return new Task(id, details, target, nextReview, nextTest, null, null, createdAt, at);
    }

    public Task block(String reason, Instant at) {
        if (reason == null || reason.isBlank()) {
            throw new IllegalArgumentException("reason must not be blank");
        }
        Objects.requireNonNull(at, "at");
        if (!TaskStateMachine.canBlock(status)) {
            throw InvalidTransitionException.notAllowed(status, TaskState.BLOCKED);
        }
        return new Task(id, details, TaskState.BLOCKED, reviewIteration, testIteration, status, reason,
                createdAt, at);
    }

    public Task unblock(Instant at) {
        Objects.requireNonNull(at, "at");
        if (status != TaskState.BLOCKED) {
            throw new InvalidTransitionException("Task " + id + " is not BLOCKED (status " + status + ")");
        }
        return new Task(id, details, blockedFrom, reviewIteration, testIteration, null, null, createdAt, at);
    }

    public String id() {
        return id;
    }

    public String title() {
        return details.title();
    }

    public String description() {
        return details.description();
    }

    public TaskType type() {
        return details.type();
    }

    public Priority priority() {
        return details.priority();
    }

    public TaskState status() {
        return status;
    }

    public Optional<AgentRole> assigneeAgent() {
        return Optional.ofNullable(details.assigneeAgent());
    }

    public Optional<String> parentTaskId() {
        return Optional.ofNullable(details.parentTaskId());
    }

    public List<String> dependencies() {
        return details.dependencies();
    }

    public List<String> acceptanceCriteria() {
        return details.acceptanceCriteria();
    }

    public Optional<String> sprintId() {
        return Optional.ofNullable(details.sprintId());
    }

    public Optional<String> repository() {
        return Optional.ofNullable(details.repository());
    }

    public Map<String, String> metadata() {
        return details.metadata();
    }

    public int reviewIteration() {
        return reviewIteration;
    }

    public int testIteration() {
        return testIteration;
    }

    public Optional<TaskState> blockedFrom() {
        return Optional.ofNullable(blockedFrom);
    }

    public Optional<String> blockReason() {
        return Optional.ofNullable(blockReason);
    }

    public Instant createdAt() {
        return createdAt;
    }

    public Instant updatedAt() {
        return updatedAt;
    }

    @Override
    public String toString() {
        return "Task[" + id + ", " + status + ", " + details.title() + "]";
    }
}
