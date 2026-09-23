package com.agentic.orchestrator.agent;

import com.agentic.orchestrator.domain.AgentRole;
import com.agentic.orchestrator.domain.NewTask;
import com.agentic.orchestrator.domain.Priority;
import com.agentic.orchestrator.domain.Task;
import com.agentic.orchestrator.domain.TaskType;
import com.agentic.orchestrator.workflow.TaskState;
import java.time.Instant;
import java.util.List;
import java.util.Map;

public final class AgentFixtures {

    private static final Instant T0 = Instant.parse("2026-01-01T00:00:00Z");

    private AgentFixtures() {
    }

    public static Task taskIn(TaskState... path) {
        Task task = Task.create("TASK-1", NewTask.of("Login API", TaskType.STORY, Priority.HIGH, List.of("ac")), T0);
        for (TaskState state : path) {
            task = task.transitionTo(state, T0);
        }
        return task;
    }

    public static AgentRequest request(AgentRole role, Task task) {
        return new AgentRequest("EXEC-1", role, task, Map.of());
    }

    public static DesignResult validDesign() {
        return new DesignResult("REST login endpoint",
                List.of(new ProposedTask("Implement POST /login", "", TaskType.TASK, Priority.HIGH, AgentRole.BE,
                        List.of("Returns 200 with token for valid credentials"))),
                List.of("Brute-force attacks"));
    }

    public static ImplementationResult validImplementation() {
        return new ImplementationResult("Added login endpoint", "feature/TASK-1-login", null,
                List.of("src/LoginController.java"));
    }

    public static ReviewResult approval() {
        return new ReviewResult("Looks good", List.of());
    }

    public static ReviewResult changes() {
        return new ReviewResult("Needs fixes",
                List.of(new ReviewComment("src/LoginController.java", ReviewSeverity.BLOCKER, "Password is logged")));
    }
}
