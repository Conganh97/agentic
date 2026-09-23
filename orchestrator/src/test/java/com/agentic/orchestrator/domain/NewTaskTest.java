package com.agentic.orchestrator.domain;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.Test;

class NewTaskTest {

    @Test
    void rejectsBlankTitle() {
        assertThatThrownBy(() -> NewTask.of(" ", TaskType.TASK, Priority.LOW, List.of("ac")))
                .isInstanceOf(IllegalArgumentException.class);
    }

    @Test
    void rejectsMissingTypeOrPriority() {
        assertThatThrownBy(() -> NewTask.of("t", null, Priority.LOW, List.of()))
                .isInstanceOf(NullPointerException.class);
        assertThatThrownBy(() -> NewTask.of("t", TaskType.TASK, null, List.of()))
                .isInstanceOf(NullPointerException.class);
    }

    @Test
    void defaultsNullCollectionsToEmpty() {
        NewTask task = new NewTask("t", null, TaskType.TASK, Priority.LOW, null, null, null, null, null, null, null);

        assertThat(task.description()).isEmpty();
        assertThat(task.dependencies()).isEmpty();
        assertThat(task.acceptanceCriteria()).isEmpty();
        assertThat(task.metadata()).isEmpty();
    }

    @Test
    void copiesCollectionsDefensively() {
        List<String> criteria = new ArrayList<>(List.of("ac-1"));
        NewTask task = NewTask.of("t", TaskType.TASK, Priority.LOW, criteria);

        criteria.add("ac-2");

        assertThat(task.acceptanceCriteria()).containsExactly("ac-1");
        assertThatThrownBy(() -> task.acceptanceCriteria().add("x"))
                .isInstanceOf(UnsupportedOperationException.class);
    }
}
