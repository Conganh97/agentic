# Testing Standards

## Principles

- Every implementation step ships with tests. No test, no merge.
- Tests are deterministic: no real network, LLM, clock, or randomness. Use fakes/stubs
  (inject a fixed `Clock`).
- Test behavior and contracts, not implementation details.

## Tooling

- JUnit 5, AssertJ for assertions, Mockito only for I/O boundaries (prefer hand-written fakes).
- Pure `domain`/`workflow` tests are plain unit tests — no Spring context.
- Use `@SpringBootTest` only for integration tests of wiring/adapters.

## Layout

- `src/test/java` mirrors `src/main/java`:
  `workflow/TaskStateMachine.java` → `workflow/TaskStateMachineTest.java`.
- Unit tests: `*Test.java`. Integration tests: `*IT.java`.
- Test method names describe behavior: `backlogCannotTransitionToMerged()`,
  or use `@DisplayName`.

## What must be tested

- **State machine:** every allowed transition, representative disallowed transitions,
  `BLOCKED`/unblock behavior, retry limits.
- **Contracts:** valid payloads accepted, invalid payloads rejected with clear errors.
- **Agents:** given a fixed input (and stubbed LLM/tools), output conforms to schema.
- **Permissions/guardrails:** forbidden actions are rejected.

## Style

- Arrange / Act / Assert structure.
- Use `@ParameterizedTest` + `@MethodSource`/`@CsvSource` for transition tables.
- Use `assertThatThrownBy(...).isInstanceOf(SpecificException.class)`.

## Commands

```bash
./mvnw test      # unit tests
./mvnw verify    # unit + integration tests
```

## Coverage

- JaCoCo; target ≥ 90% line coverage for `domain` and `workflow`. Coverage is a signal, not a goal.
