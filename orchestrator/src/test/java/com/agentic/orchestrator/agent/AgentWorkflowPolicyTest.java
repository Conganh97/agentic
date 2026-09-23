package com.agentic.orchestrator.agent;

import static org.assertj.core.api.Assertions.assertThat;

import com.agentic.orchestrator.domain.AgentRole;
import com.agentic.orchestrator.workflow.TaskState;
import java.util.Set;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import org.junit.jupiter.params.provider.EnumSource;

class AgentWorkflowPolicyTest {

    @ParameterizedTest(name = "{0} may work in {1}")
    @CsvSource({"SA, BACKLOG", "BE, IN_PROGRESS", "FE, IN_PROGRESS", "SA, CODE_REVIEW"})
    void eligibleAgents(AgentRole role, TaskState state) {
        assertThat(AgentWorkflowPolicy.canExecute(role, state)).isTrue();
    }

    @ParameterizedTest(name = "{0} may not work in {1}")
    @CsvSource({
        "BE, BACKLOG", "SA, IN_PROGRESS", "BE, CODE_REVIEW", "FE, CODE_REVIEW",
        "TEST, TESTING", "DEVOPS, DEPLOYING", "SCRUM, BACKLOG"
    })
    void ineligibleAgents(AgentRole role, TaskState state) {
        assertThat(AgentWorkflowPolicy.canExecute(role, state)).isFalse();
    }

    @ParameterizedTest
    @EnumSource(value = TaskState.class, names = {"BACKLOG", "IN_PROGRESS", "CODE_REVIEW"}, mode = EnumSource.Mode.EXCLUDE)
    void noAgentWorksOutsideDefinedSteps(TaskState state) {
        assertThat(AgentWorkflowPolicy.stepFor(state)).isEmpty();
        for (AgentRole role : AgentRole.values()) {
            assertThat(AgentWorkflowPolicy.canExecute(role, state)).isFalse();
        }
    }

    @Test
    void completedTargetsFollowTheMvpLoop() {
        assertThat(AgentWorkflowPolicy.stepFor(TaskState.BACKLOG).orElseThrow().onCompleted()).isEmpty();
        assertThat(AgentWorkflowPolicy.stepFor(TaskState.IN_PROGRESS).orElseThrow().onCompleted())
                .contains(TaskState.CODE_REVIEW);
        assertThat(AgentWorkflowPolicy.stepFor(TaskState.CODE_REVIEW).orElseThrow().onCompleted())
                .contains(TaskState.MERGED);
    }

    @Test
    void reviewIsOnlyDoneBySa() {
        assertThat(AgentWorkflowPolicy.stepFor(TaskState.CODE_REVIEW).orElseThrow().roles())
                .isEqualTo(Set.of(AgentRole.SA));
    }
}
