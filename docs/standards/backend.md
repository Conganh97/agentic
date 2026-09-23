# Backend / Java Standards

Applies to the Orchestrator, agent runtime, and tool layer (all Java).

## Language and tooling

- Java 21 (LTS). Build: Maven (`pom.xml`, introduced in Phase 1). Use the Maven Wrapper (`./mvnw`).
- Application framework: Spring Boot — only in the application/adapters layer (see Structure),
  added when the Orchestrator needs an API or wiring.
- Tests: JUnit 5 + AssertJ (see `testing.md`).
- Formatting (Spotless) and coverage (JaCoCo) are added together with CI (Phase 6).

## Structure

Orchestrator module layout (base package `com.agentic.orchestrator`):

```
orchestrator/
├── pom.xml
└── src/
    ├── main/java/com/agentic/orchestrator/
    │   ├── workflow/      # TaskState + transition rules — pure Java, deterministic
    │   ├── domain/        # Task aggregate, enums, value objects — pure Java, no Spring, no I/O
    │   ├── service/       # use cases; coordinate domain + repositories
    │   └── repository/    # persistence interfaces + adapters (in-memory first)
    └── test/java/com/agentic/orchestrator/   # mirrors main
```

- Dependencies point inward: `service → domain/workflow`, `repository → domain`, `domain → workflow`.
  `workflow` depends on nothing. `domain` and `workflow` never import from `service`, `repository`, or Spring.
- No I/O, network, LLM calls, `Instant.now()`, or randomness inside `domain` and `workflow`.
  Inject them (e.g. `java.time.Clock`).

## Code rules

- Use `enum` for states, statuses, types, priorities — never raw strings.
- Use `record` for immutable data (value objects, DTOs, agent contracts).
- Prefer immutability: `final` fields, `List.copyOf(...)`, return new objects instead of mutating shared state.
- Never return `null` from public methods; use `Optional` for "maybe absent" results.
- Fail loudly: throw specific unchecked exceptions (e.g. `InvalidTransitionException`)
  instead of returning `false`/`null`.
- Never catch `Exception`/`Throwable` broadly or swallow exceptions silently.
- Constructor injection only (no field `@Autowired`).
- Methods do one thing; keep them small. Avoid premature abstraction (no interface with a single
  implementation unless it is a port to I/O).
- Names: `camelCase` methods/variables, `PascalCase` classes, `UPPER_SNAKE` constants,
  lowercase packages.
- Comments explain *why*, not *what*.

## Configuration and secrets

- Config via `application.yml` + environment variables; bind with `@ConfigurationProperties`.
- Never commit secrets; provide `.env.example` if env vars are needed.
- Never log secrets, tokens, or full LLM prompts containing sensitive data.

## Logging and audit

- SLF4J logging with structured context (`task_id`, `agent`, `execution_id` via MDC).
- State transitions and agent executions must be recorded for audit (see system-overview §9).

## Dependencies

- Add a dependency only when the current phase needs it; justify non-trivial ones in the PR.
- Manage versions via the Spring Boot BOM / `dependencyManagement`; no floating versions.
