package com.agentic.orchestrator.agent;

import com.agentic.orchestrator.domain.AgentRole;

/** An agent performs work for one task and reports a structured result. It never changes task state. */
public interface Agent {

    AgentRole role();

    AgentResponse execute(AgentRequest request);
}
