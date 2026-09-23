package com.agentic.orchestrator.service;

import static com.agentic.orchestrator.agent.AgentFixtures.approval;
import static com.agentic.orchestrator.agent.AgentFixtures.changes;
import static com.agentic.orchestrator.agent.AgentFixtures.validDesign;
import static com.agentic.orchestrator.agent.AgentFixtures.validImplementation;
import static com.agentic.orchestrator.workflow.TaskState.BACKLOG;
import static com.agentic.orchestrator.workflow.TaskState.BLOCKED;
import static com.agentic.orchestrator.workflow.TaskState.CHANGES_REQUESTED;
import static com.agentic.orchestrator.workflow.TaskState.CODE_REVIEW;
import static com.agentic.orchestrator.workflow.TaskState.IN_PROGRESS;
import static com.agentic.orchestrator.workflow.TaskState.MERGED;
import static com.agentic.orchestrator.workflow.TaskState.READY;
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import com.agentic.orchestrator.agent.Agent;
import com.agentic.orchestrator.agent.AgentRequest;
import com.agentic.orchestrator.agent.AgentResponse;
import com.agentic.orchestrator.agent.AgentStatus;
import com.agentic.orchestrator.domain.AgentRole;
import com.agentic.orchestrator.domain.NewTask;
import com.agentic.orchestrator.domain.Priority;
import com.agentic.orchestrator.domain.TaskType;
import com.agentic.orchestrator.repository.InMemoryTaskRepository;
import com.agentic.orchestrator.workflow.TaskState;
import java.time.Clock;
import java.time.Instant;
import java.time.ZoneOffset;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;
import java.util.function.Function;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class AgentExecutionServiceTest {

    private static final Instant NOW = Instant.parse("2026-01-01T00:00:00Z");

    private TaskService tasks;
    private AgentExecutionService executor;

    private record StubAgent(AgentRole role, Function<AgentRequest, AgentResponse> behavior) implements Agent {
        @Override
        public AgentResponse execute(AgentRequest request) {
            return behavior.apply(request);
        }
    }

    @BeforeEach
    void setUp() {
        Clock clock = Clock.fixed(NOW, ZoneOffset.UTC);
        tasks = new TaskService(new InMemoryTaskRepository(), clock, WorkflowLimits.DEFAULT);
        AtomicInteger sequence = new AtomicInteger();
        executor = new AgentExecutionService(tasks, clock, () -> "EXEC-" + sequence.incrementAndGet());
    }

    private String taskIn(TaskState... path) {
        String id = tasks.create(NewTask.of("Login API", TaskType.STORY, Priority.HIGH, List.of("ac"))).id();
        for (TaskState state : path) {
            tasks.transition(id, state);
        }
        return id;
    }

    private static Agent be(Function<AgentRequest, AgentResponse> behavior) {
        return new StubAgent(AgentRole.BE, behavior);
    }

    private static Agent sa(Function<AgentRequest, AgentResponse> behavior) {
        return new StubAgent(AgentRole.SA, behavior);
    }

    @Test
    void completedImplementationMovesTaskToCodeReview() {
        String id = taskIn(READY, IN_PROGRESS);

        AgentExecution execution = executor.execute(id, be(r -> AgentResponse.completed(r, validImplementation())),
                Map.of());

        assertThat(execution.accepted()).isTrue();
        assertThat(execution.stateBefore()).isEqualTo(IN_PROGRESS);
        assertThat(execution.stateAfter()).isEqualTo(CODE_REVIEW);
        assertThat(tasks.get(id).status()).isEqualTo(CODE_REVIEW);
    }

    @Test
    void approvedReviewMovesTaskToMerged() {
        String id = taskIn(READY, IN_PROGRESS, CODE_REVIEW);

        executor.execute(id, sa(r -> AgentResponse.completed(r, approval())), Map.of());

        assertThat(tasks.get(id).status()).isEqualTo(MERGED);
    }

    @Test
    void changesRequestedMovesTaskAndCountsIteration() {
        String id = taskIn(READY, IN_PROGRESS, CODE_REVIEW);

        executor.execute(id, sa(r -> AgentResponse.changesRequested(r, changes())), Map.of());

        assertThat(tasks.get(id).status()).isEqualTo(CHANGES_REQUESTED);
        assertThat(tasks.get(id).reviewIteration()).isEqualTo(1);
    }

    @Test
    void completedDesignDoesNotChangeState() {
        String id = taskIn();

        AgentExecution execution = executor.execute(id, sa(r -> AgentResponse.completed(r, validDesign())),
                Map.of());

        assertThat(execution.accepted()).isTrue();
        assertThat(tasks.get(id).status()).isEqualTo(BACKLOG);
    }

    @Test
    void invalidResponseIsRejectedAndStateUnchanged() {
        String id = taskIn(READY, IN_PROGRESS);

        AgentExecution execution = executor.execute(id, be(r -> AgentResponse.completed(r, approval())), Map.of());

        assertThat(execution.accepted()).isFalse();
        assertThat(execution.violations()).isNotEmpty();
        assertThat(execution.response().status()).isEqualTo(AgentStatus.FAILED);
        assertThat(execution.response().error().code()).isEqualTo(AgentExecutionService.INVALID_RESPONSE);
        assertThat(tasks.get(id).status()).isEqualTo(IN_PROGRESS);
    }

    @Test
    void nullResponseIsRejected() {
        String id = taskIn(READY, IN_PROGRESS);

        AgentExecution execution = executor.execute(id, be(r -> null), Map.of());

        assertThat(execution.violations()).containsExactly("response must not be null");
        assertThat(tasks.get(id).status()).isEqualTo(IN_PROGRESS);
    }

    @Test
    void agentExceptionBecomesFailedExecution() {
        String id = taskIn(READY, IN_PROGRESS);

        AgentExecution execution = executor.execute(id, be(r -> {
            throw new IllegalStateException("boom");
        }), Map.of());

        assertThat(execution.response().status()).isEqualTo(AgentStatus.FAILED);
        assertThat(execution.response().error().code()).isEqualTo(AgentExecutionService.AGENT_EXCEPTION);
        assertThat(execution.violations()).singleElement().asString().contains("boom");
        assertThat(tasks.get(id).status()).isEqualTo(IN_PROGRESS);
    }

    @Test
    void failedAndNeedsInputDoNotChangeState() {
        String id = taskIn(READY, IN_PROGRESS);

        executor.execute(id, be(r -> AgentResponse.failed(r, "TOOL_ERROR", "tests crashed")), Map.of());
        executor.execute(id, be(r -> AgentResponse.needsInput(r, "UNCLEAR", "which DB?")), Map.of());

        assertThat(tasks.get(id).status()).isEqualTo(IN_PROGRESS);
    }

    @Test
    void blockedResponseBlocksTaskWithReason() {
        String id = taskIn(READY, IN_PROGRESS);

        executor.execute(id, be(r -> AgentResponse.blocked(r, "DEPENDENCY", "API contract missing")), Map.of());

        assertThat(tasks.get(id).status()).isEqualTo(BLOCKED);
        assertThat(tasks.get(id).blockReason()).contains("Agent BE: API contract missing");
    }

    @Test
    void blockedResponseOnNonBlockableStateLeavesState() {
        String id = taskIn();

        executor.execute(id, sa(r -> AgentResponse.blocked(r, "UNCLEAR", "requirement unclear")), Map.of());

        assertThat(tasks.get(id).status()).isEqualTo(BACKLOG);
    }

    @Test
    void ineligibleAgentIsRejectedBeforeRunning() {
        String id = taskIn(READY, IN_PROGRESS, CODE_REVIEW);
        AtomicInteger calls = new AtomicInteger();

        assertThatThrownBy(() -> executor.execute(id, be(r -> {
            calls.incrementAndGet();
            return AgentResponse.completed(r, validImplementation());
        }), Map.of())).isInstanceOf(AgentNotAllowedException.class);
        assertThat(calls).hasValue(0);
    }

    @Test
    void requestCarriesTaskSnapshotAndInputs() {
        String id = taskIn(READY, IN_PROGRESS);
        AtomicReference<AgentRequest> seen = new AtomicReference<>();

        AgentExecution execution = executor.execute(id, be(r -> {
            seen.set(r);
            return AgentResponse.completed(r, validImplementation());
        }), Map.of("design", "Use JWT"));

        assertThat(seen.get().executionId()).isEqualTo("EXEC-1").isEqualTo(execution.executionId());
        assertThat(seen.get().task().id()).isEqualTo(id);
        assertThat(seen.get().task().status()).isEqualTo(IN_PROGRESS);
        assertThat(seen.get().inputs()).containsEntry("design", "Use JWT");
        assertThat(execution.startedAt()).isEqualTo(NOW);
        assertThat(execution.finishedAt()).isEqualTo(NOW);
    }

    @Test
    void mvpReviewLoopEndsInMerged() {
        String id = taskIn(READY, IN_PROGRESS);
        Agent backend = be(r -> AgentResponse.completed(r, validImplementation()));

        executor.execute(id, backend, Map.of());
        executor.execute(id, sa(r -> AgentResponse.changesRequested(r, changes())), Map.of());
        tasks.transition(id, IN_PROGRESS);
        executor.execute(id, backend, Map.of());
        executor.execute(id, sa(r -> AgentResponse.completed(r, approval())), Map.of());

        assertThat(tasks.get(id).status()).isEqualTo(MERGED);
        assertThat(tasks.get(id).reviewIteration()).isEqualTo(1);
    }
}
