package com.agentic.orchestrator.workflow;

public class InvalidTransitionException extends RuntimeException {

    public InvalidTransitionException(String message) {
        super(message);
    }

    public static InvalidTransitionException notAllowed(TaskState from, TaskState to) {
        return new InvalidTransitionException("Transition " + from + " -> " + to + " is not allowed");
    }
}
