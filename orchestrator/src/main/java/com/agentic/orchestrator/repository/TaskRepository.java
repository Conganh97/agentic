package com.agentic.orchestrator.repository;

import com.agentic.orchestrator.domain.Task;
import java.util.Optional;

public interface TaskRepository {

    String nextId();

    Optional<Task> findById(String id);

    Task save(Task task);
}
