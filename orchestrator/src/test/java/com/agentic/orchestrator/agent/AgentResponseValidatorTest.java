package com.agentic.orchestrator.agent;

import static com.agentic.orchestrator.agent.AgentFixtures.approval;
import static com.agentic.orchestrator.agent.AgentFixtures.changes;
import static com.agentic.orchestrator.agent.AgentFixtures.request;
import static com.agentic.orchestrator.agent.AgentFixtures.taskIn;
import static com.agentic.orchestrator.agent.AgentFixtures.validDesign;
import static com.agentic.orchestrator.agent.AgentFixtures.validImplementation;
import static com.agentic.orchestrator.workflow.TaskState.CODE_REVIEW;
import static com.agentic.orchestrator.workflow.TaskState.IN_PROGRESS;
import static com.agentic.orchestrator.workflow.TaskState.READY;
import static org.assertj.core.api.Assertions.assertThat;

import com.agentic.orchestrator.domain.AgentRole;
import com.agentic.orchestrator.domain.Priority;
import com.agentic.orchestrator.domain.TaskType;
import java.util.List;
import org.junit.jupiter.api.Test;

class AgentResponseValidatorTest {

    private final AgentRequest backlogSa = request(AgentRole.SA, taskIn());
    private final AgentRequest inProgressBe = request(AgentRole.BE, taskIn(READY, IN_PROGRESS));
    private final AgentRequest reviewSa = request(AgentRole.SA, taskIn(READY, IN_PROGRESS, CODE_REVIEW));

    private static List<String> validate(AgentRequest request, AgentResponse response) {
        return AgentResponseValidator.validate(request, response);
    }

    @Test
    void acceptsValidResponsesForEachStep() {
        assertThat(validate(backlogSa, AgentResponse.completed(backlogSa, validDesign()))).isEmpty();
        assertThat(validate(inProgressBe, AgentResponse.completed(inProgressBe, validImplementation()))).isEmpty();
        assertThat(validate(reviewSa, AgentResponse.completed(reviewSa, approval()))).isEmpty();
        assertThat(validate(reviewSa, AgentResponse.changesRequested(reviewSa, changes()))).isEmpty();
    }

    @Test
    void acceptsNonCompletedStatusesWithError() {
        assertThat(validate(inProgressBe, AgentResponse.failed(inProgressBe, "TOOL_ERROR", "tests crashed"))).isEmpty();
        assertThat(validate(inProgressBe, AgentResponse.needsInput(inProgressBe, "UNCLEAR", "which DB?"))).isEmpty();
        assertThat(validate(inProgressBe, AgentResponse.blocked(inProgressBe, "DEPENDENCY", "API missing"))).isEmpty();
    }

    @Test
    void rejectsNullResponse() {
        assertThat(validate(inProgressBe, null)).containsExactly("response must not be null");
    }

    @Test
    void rejectsIdentityMismatch() {
        AgentResponse response = new AgentResponse("OTHER", AgentRole.FE, "TASK-9", AgentStatus.COMPLETED,
                validImplementation(), null);

        assertThat(validate(inProgressBe, response)).containsExactlyInAnyOrder(
                "executionId does not match request",
                "agent FE does not match request agent BE",
                "taskId does not match request");
    }

    @Test
    void rejectsMissingStatus() {
        AgentResponse response = new AgentResponse("EXEC-1", AgentRole.BE, "TASK-1", null, null, null);

        assertThat(validate(inProgressBe, response)).containsExactly("status must not be null");
    }

    @Test
    void completedRequiresResultAndNoError() {
        AgentResponse response = new AgentResponse("EXEC-1", AgentRole.BE, "TASK-1", AgentStatus.COMPLETED, null,
                new AgentError("X", "y"));

        assertThat(validate(inProgressBe, response)).containsExactlyInAnyOrder(
                "error must be null when status is COMPLETED",
                "result is required when status is COMPLETED");
    }

    @Test
    void failedRequiresErrorAndNoResult() {
        AgentResponse response = new AgentResponse("EXEC-1", AgentRole.BE, "TASK-1", AgentStatus.FAILED,
                validImplementation(), null);

        assertThat(validate(inProgressBe, response)).containsExactlyInAnyOrder(
                "result must be null when status is FAILED",
                "error is required when status is FAILED");
    }

    @Test
    void errorFieldsMustNotBeBlank() {
        AgentResponse response = AgentResponse.blocked(inProgressBe, " ", null);

        assertThat(validate(inProgressBe, response)).containsExactlyInAnyOrder(
                "error.code must not be blank", "error.message must not be blank");
    }

    @Test
    void rejectsResultTypeNotMatchingTaskState() {
        assertThat(validate(inProgressBe, AgentResponse.completed(inProgressBe, approval())))
                .containsExactly("result must be ImplementationResult for task state IN_PROGRESS but was ReviewResult");
    }

    @Test
    void rejectsResultForStateWithoutAgentWork() {
        AgentRequest ready = request(AgentRole.BE, taskIn(READY));

        assertThat(validate(ready, AgentResponse.completed(ready, validImplementation())))
                .containsExactly("no agent work is defined for task state READY");
    }

    @Test
    void changesRequestedIsOnlyValidForReview() {
        AgentResponse response = new AgentResponse("EXEC-1", AgentRole.SA, "TASK-1", AgentStatus.CHANGES_REQUESTED,
                validDesign(), null);

        assertThat(validate(backlogSa, response)).containsExactly("CHANGES_REQUESTED is only valid for a review");
    }

    @Test
    void designMustHaveSummaryAndCompleteTasks() {
        DesignResult design = new DesignResult(" ", List.of(
                new ProposedTask(" ", "", null, null, AgentRole.BE, List.of())), List.of());

        assertThat(validate(backlogSa, AgentResponse.completed(backlogSa, design))).containsExactlyInAnyOrder(
                "design.summary must not be blank",
                "design.tasks[0].title must not be blank",
                "design.tasks[0].type must not be null",
                "design.tasks[0].priority must not be null",
                "design.tasks[0].acceptanceCriteria must not be empty");
    }

    @Test
    void designMustHaveTasks() {
        DesignResult design = new DesignResult("summary", List.of(), List.of());

        assertThat(validate(backlogSa, AgentResponse.completed(backlogSa, design)))
                .containsExactly("design.tasks must not be empty");
    }

    @Test
    void designTaskWithAllFieldsIsValid() {
        DesignResult design = new DesignResult("s", List.of(
                new ProposedTask("t", null, TaskType.TASK, Priority.LOW, null, List.of("ac"))), null);

        assertThat(validate(backlogSa, AgentResponse.completed(backlogSa, design))).isEmpty();
    }

    @Test
    void implementationMustHaveSummaryBranchAndFiles() {
        ImplementationResult implementation = new ImplementationResult("", null, null, List.of());

        assertThat(validate(inProgressBe, AgentResponse.completed(inProgressBe, implementation)))
                .containsExactlyInAnyOrder(
                        "implementation.summary must not be blank",
                        "implementation.branch must not be blank",
                        "implementation.changedFiles must not be empty");
    }

    @Test
    void changesRequestedNeedsAtLeastOneComment() {
        assertThat(validate(reviewSa, AgentResponse.changesRequested(reviewSa, approval())))
                .containsExactly("CHANGES_REQUESTED requires at least one review comment");
    }

    @Test
    void approvalCannotContainBlockers() {
        assertThat(validate(reviewSa, AgentResponse.completed(reviewSa, changes())))
                .containsExactly("an approved review must not contain BLOCKER comments");
    }

    @Test
    void reviewCommentsMustBeComplete() {
        ReviewResult review = new ReviewResult("s", List.of(new ReviewComment(null, null, " ")));

        assertThat(validate(reviewSa, AgentResponse.changesRequested(reviewSa, review))).containsExactlyInAnyOrder(
                "review.comments[0].severity must not be null",
                "review.comments[0].message must not be blank");
    }
}
