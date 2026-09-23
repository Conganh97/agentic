package com.agentic.orchestrator.agent;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/** Validates an agent response against its request and the result schema. Returns all violations found. */
public final class AgentResponseValidator {

    private AgentResponseValidator() {
    }

    public static List<String> validate(AgentRequest request, AgentResponse response) {
        Objects.requireNonNull(request, "request");
        if (response == null) {
            return List.of("response must not be null");
        }
        List<String> violations = new ArrayList<>();
        if (!request.executionId().equals(response.executionId())) {
            violations.add("executionId does not match request");
        }
        if (response.agent() != request.agent()) {
            violations.add("agent " + response.agent() + " does not match request agent " + request.agent());
        }
        if (!request.task().id().equals(response.taskId())) {
            violations.add("taskId does not match request");
        }
        if (response.status() == null) {
            violations.add("status must not be null");
            return List.copyOf(violations);
        }
        switch (response.status()) {
            case COMPLETED, CHANGES_REQUESTED -> {
                if (response.error() != null) {
                    violations.add("error must be null when status is " + response.status());
                }
                if (response.result() == null) {
                    violations.add("result is required when status is " + response.status());
                } else {
                    validateResult(request, response.status(), response.result(), violations);
                }
            }
            case FAILED, NEEDS_INPUT, BLOCKED -> {
                if (response.result() != null) {
                    violations.add("result must be null when status is " + response.status());
                }
                validateError(response.error(), response.status(), violations);
            }
        }
        return List.copyOf(violations);
    }

    private static void validateError(AgentError error, AgentStatus status, List<String> violations) {
        if (error == null) {
            violations.add("error is required when status is " + status);
            return;
        }
        if (isBlank(error.code())) {
            violations.add("error.code must not be blank");
        }
        if (isBlank(error.message())) {
            violations.add("error.message must not be blank");
        }
    }

    private static void validateResult(AgentRequest request, AgentStatus status, AgentResult result,
                                       List<String> violations) {
        var step = AgentWorkflowPolicy.stepFor(request.task().status());
        if (step.isEmpty()) {
            violations.add("no agent work is defined for task state " + request.task().status());
            return;
        }
        Class<? extends AgentResult> expected = step.get().resultType();
        if (!expected.isInstance(result)) {
            violations.add("result must be " + expected.getSimpleName() + " for task state "
                    + request.task().status() + " but was " + result.getClass().getSimpleName());
            return;
        }
        if (status == AgentStatus.CHANGES_REQUESTED && !(result instanceof ReviewResult)) {
            violations.add("CHANGES_REQUESTED is only valid for a review");
            return;
        }
        switch (result) {
            case DesignResult design -> validateDesign(design, violations);
            case ImplementationResult implementation -> validateImplementation(implementation, violations);
            case ReviewResult review -> validateReview(review, status, violations);
        }
    }

    private static void validateDesign(DesignResult design, List<String> violations) {
        if (isBlank(design.summary())) {
            violations.add("design.summary must not be blank");
        }
        if (design.tasks().isEmpty()) {
            violations.add("design.tasks must not be empty");
        }
        for (int i = 0; i < design.tasks().size(); i++) {
            ProposedTask task = design.tasks().get(i);
            String prefix = "design.tasks[" + i + "]";
            if (isBlank(task.title())) {
                violations.add(prefix + ".title must not be blank");
            }
            if (task.type() == null) {
                violations.add(prefix + ".type must not be null");
            }
            if (task.priority() == null) {
                violations.add(prefix + ".priority must not be null");
            }
            if (task.acceptanceCriteria().isEmpty()) {
                violations.add(prefix + ".acceptanceCriteria must not be empty");
            }
        }
    }

    private static void validateImplementation(ImplementationResult implementation, List<String> violations) {
        if (isBlank(implementation.summary())) {
            violations.add("implementation.summary must not be blank");
        }
        if (isBlank(implementation.branch())) {
            violations.add("implementation.branch must not be blank");
        }
        if (implementation.changedFiles().isEmpty()) {
            violations.add("implementation.changedFiles must not be empty");
        }
    }

    private static void validateReview(ReviewResult review, AgentStatus status, List<String> violations) {
        if (isBlank(review.summary())) {
            violations.add("review.summary must not be blank");
        }
        for (int i = 0; i < review.comments().size(); i++) {
            ReviewComment comment = review.comments().get(i);
            if (comment.severity() == null) {
                violations.add("review.comments[" + i + "].severity must not be null");
            }
            if (isBlank(comment.message())) {
                violations.add("review.comments[" + i + "].message must not be blank");
            }
        }
        if (status == AgentStatus.CHANGES_REQUESTED && review.comments().isEmpty()) {
            violations.add("CHANGES_REQUESTED requires at least one review comment");
        }
        if (status == AgentStatus.COMPLETED
                && review.comments().stream().anyMatch(c -> c.severity() == ReviewSeverity.BLOCKER)) {
            violations.add("an approved review must not contain BLOCKER comments");
        }
    }

    private static boolean isBlank(String value) {
        return value == null || value.isBlank();
    }
}
