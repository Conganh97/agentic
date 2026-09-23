package com.agentic.orchestrator.domain;

import java.util.List;
import java.util.Map;
import java.util.Objects;

/**
 * Input for creating a task. {@code assigneeAgent}, {@code parentTaskId}, {@code sprintId} and
 * {@code repository} may be null; collections default to empty.
 */
public record NewTask(
        String title,
        String description,
        TaskType type,
        Priority priority,
        AgentRole assigneeAgent,
        String parentTaskId,
        List<String> dependencies,
        List<String> acceptanceCriteria,
        String sprintId,
        String repository,
        Map<String, String> metadata) {

    public NewTask {
        if (title == null || title.isBlank()) {
            throw new IllegalArgumentException("title must not be blank");
        }
        Objects.requireNonNull(type, "type");
        Objects.requireNonNull(priority, "priority");
        description = description == null ? "" : description;
        dependencies = dependencies == null ? List.of() : List.copyOf(dependencies);
        acceptanceCriteria = acceptanceCriteria == null ? List.of() : List.copyOf(acceptanceCriteria);
        metadata = metadata == null ? Map.of() : Map.copyOf(metadata);
    }

    public static NewTask of(String title, TaskType type, Priority priority, List<String> acceptanceCriteria) {
        return new NewTask(title, "", type, priority, null, null, List.of(), acceptanceCriteria, null, null, Map.of());
    }
}
