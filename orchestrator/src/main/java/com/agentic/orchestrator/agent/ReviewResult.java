package com.agentic.orchestrator.agent;

import java.util.List;

/**
 * SA code review. The decision is carried by the response status: COMPLETED means approved,
 * CHANGES_REQUESTED means the comments must be addressed.
 */
public record ReviewResult(String summary, List<ReviewComment> comments) implements AgentResult {

    public ReviewResult {
        comments = comments == null ? List.of() : List.copyOf(comments);
    }
}
