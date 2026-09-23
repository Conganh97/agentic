package com.agentic.orchestrator.service;

import com.agentic.orchestrator.domain.NewTask;
import com.agentic.orchestrator.domain.Task;
import com.agentic.orchestrator.repository.TaskRepository;
import com.agentic.orchestrator.workflow.TaskState;
import java.time.Clock;
import java.util.Objects;

public final class TaskService {

    private final TaskRepository repository;
    private final Clock clock;
    private final WorkflowLimits limits;

    public TaskService(TaskRepository repository, Clock clock, WorkflowLimits limits) {
        this.repository = Objects.requireNonNull(repository, "repository");
        this.clock = Objects.requireNonNull(clock, "clock");
        this.limits = Objects.requireNonNull(limits, "limits");
    }

    public Task create(NewTask details) {
        return repository.save(Task.create(repository.nextId(), details, clock.instant()));
    }

    public Task get(String id) {
        return repository.findById(id).orElseThrow(() -> new TaskNotFoundException(id));
    }

    /**
     * Applies a validated transition. If the transition would exceed a retry limit, the task is BLOCKED
     * instead and the blocked task is returned.
     */
    public Task transition(String id, TaskState target) {
        Task task = get(id);
        if (target == TaskState.CHANGES_REQUESTED && task.reviewIteration() >= limits.maxReviewIterations()) {
            return repository.save(task.block(
                    "Review iteration limit reached (" + limits.maxReviewIterations() + ")", clock.instant()));
        }
        if (target == TaskState.BUG && task.testIteration() >= limits.maxTestIterations()) {
            return repository.save(task.block(
                    "Test iteration limit reached (" + limits.maxTestIterations() + ")", clock.instant()));
        }
        return repository.save(task.transitionTo(target, clock.instant()));
    }

    public Task block(String id, String reason) {
        return repository.save(get(id).block(reason, clock.instant()));
    }

    public Task unblock(String id) {
        return repository.save(get(id).unblock(clock.instant()));
    }
}
