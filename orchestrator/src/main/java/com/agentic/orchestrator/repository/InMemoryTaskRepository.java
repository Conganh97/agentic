package com.agentic.orchestrator.repository;

import com.agentic.orchestrator.domain.Task;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

public final class InMemoryTaskRepository implements TaskRepository {

    private final Map<String, Task> tasks = new ConcurrentHashMap<>();
    private final AtomicLong sequence = new AtomicLong();

    @Override
    public String nextId() {
        return "TASK-" + sequence.incrementAndGet();
    }

    @Override
    public Optional<Task> findById(String id) {
        return Optional.ofNullable(tasks.get(id));
    }

    @Override
    public Task save(Task task) {
        tasks.put(task.id(), task);
        return task;
    }
}
