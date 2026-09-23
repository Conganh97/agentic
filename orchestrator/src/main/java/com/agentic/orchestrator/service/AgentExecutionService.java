package com.agentic.orchestrator.service;

import com.agentic.orchestrator.agent.Agent;
import com.agentic.orchestrator.agent.AgentRequest;
import com.agentic.orchestrator.agent.AgentResponse;
import com.agentic.orchestrator.agent.AgentResponseValidator;
import com.agentic.orchestrator.agent.AgentWorkflowPolicy;
import com.agentic.orchestrator.domain.Task;
import com.agentic.orchestrator.workflow.TaskState;
import com.agentic.orchestrator.workflow.TaskStateMachine;
import java.time.Clock;
import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.function.Supplier;

/**
 * Agent execution lifecycle: check eligibility, build request, run agent, validate response, then let the
 * Orchestrator decide the state change. Agents never touch task state themselves.
 */
public final class AgentExecutionService {

    static final String AGENT_EXCEPTION = "AGENT_EXCEPTION";
    static final String INVALID_RESPONSE = "INVALID_RESPONSE";

    private final TaskService taskService;
    private final Clock clock;
    private final Supplier<String> executionIds;

    public AgentExecutionService(TaskService taskService, Clock clock, Supplier<String> executionIds) {
        this.taskService = Objects.requireNonNull(taskService, "taskService");
        this.clock = Objects.requireNonNull(clock, "clock");
        this.executionIds = Objects.requireNonNull(executionIds, "executionIds");
    }

    public AgentExecution execute(String taskId, Agent agent, Map<String, String> inputs) {
        Task task = taskService.get(taskId);
        if (!AgentWorkflowPolicy.canExecute(agent.role(), task.status())) {
            throw new AgentNotAllowedException(agent.role(), taskId, task.status());
        }
        AgentRequest request = new AgentRequest(executionIds.get(), agent.role(), task, inputs);
        Instant startedAt = clock.instant();

        Outcome outcome = run(agent, request);
        Task after = apply(task, outcome.response());
        return new AgentExecution(request.executionId(), agent.role(), taskId, startedAt, clock.instant(),
                outcome.response(), outcome.violations(), task.status(), after.status());
    }

    private record Outcome(AgentResponse response, List<String> violations) {
    }

    private static Outcome run(Agent agent, AgentRequest request) {
        AgentResponse raw;
        try {
            raw = agent.execute(request);
        } catch (RuntimeException e) {
            // Agents are untrusted boundaries; a crash must become a FAILED execution, not break the workflow.
            String violation = "agent threw " + e.getClass().getSimpleName() + ": " + e.getMessage();
            return new Outcome(AgentResponse.failed(request, AGENT_EXCEPTION, violation), List.of(violation));
        }
        List<String> violations = AgentResponseValidator.validate(request, raw);
        if (violations.isEmpty()) {
            return new Outcome(raw, violations);
        }
        return new Outcome(AgentResponse.failed(request, INVALID_RESPONSE, String.join("; ", violations)), violations);
    }

    private Task apply(Task task, AgentResponse response) {
        return switch (response.status()) {
            case COMPLETED -> AgentWorkflowPolicy.stepFor(task.status())
                    .flatMap(AgentWorkflowPolicy.Step::onCompleted)
                    .map(target -> taskService.transition(task.id(), target))
                    .orElse(task);
            case CHANGES_REQUESTED -> taskService.transition(task.id(), TaskState.CHANGES_REQUESTED);
            case BLOCKED -> TaskStateMachine.canBlock(task.status())
                    ? taskService.block(task.id(), "Agent " + response.agent() + ": " + response.error().message())
                    : task;
            case FAILED, NEEDS_INPUT -> task;
        };
    }
}
