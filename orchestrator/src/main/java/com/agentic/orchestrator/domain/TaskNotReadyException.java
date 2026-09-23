package com.agentic.orchestrator.domain;

public class TaskNotReadyException extends RuntimeException {

    public TaskNotReadyException(String message) {
        super(message);
    }
}
