# Backend Standards

`product/services/<name>-service/`. Cores: Java 21 + Spring (ADR-0009).
DB, migrations, security, messaging: **SA design §5**.

## Layout (package by feature)

```
com.product.<name>/
  <Name>Application.java
  shared/
    config/            # Boot, CORS, properties
    error/             # ProblemDetail advice
    security/          # if the design has auth
  <feature>/           # catalog, cart, …
    api/               # @RestController, request/response records
    application/       # use cases, @Transactional
    domain/            # entities, value objects, rules
    infrastructure/    # persistence, HTTP clients
```

`api → application → domain`. Controllers never use persistence types. Create only features the
task needs.

## New service

- Folder `services/<name>-service/`, `artifactId` same, wrapper `mvn -N wrapper:wrapper`.
- Starters from the design (Boot 4 names: `webmvc`, `webmvc-test`, `restclient`, …).
- `server.port: ${SERVER_PORT:<default>}` in README.
- Unsure about a Boot 4 type → Context7 `/spring-projects/spring-boot`.

## REST

`/api/v1/<plural-kebab>`. JSON. DTOs are `record`s; never expose entities.
Jakarta Validation on fields (`@Size` on free text); no class-level `@Validated` on controllers.
One `@RestControllerAdvice` → RFC 9457 `ProblemDetail`; no stack traces.
200/201/204 · 400 · 401/403 · 404 · 409. Breaking change = new version path + SA design.

## Persistence (when the design has a DB)

One database per service. Schema only via the chosen migrator; never edit an applied migration.
`ddl-auto=validate` if JPA.

## CORS

If the browser calls the API (or Vite `/api` proxy), allow **both**
`http://localhost:<FE_PORT>` and `http://127.0.0.1:<FE_PORT>`. Credentials when cookies are used.
Tests must hit both origins.

## Code / tests

Constructor injection; `enum` / `record` / `Optional`; no secrets in repo; SLF4J without PII;
`/actuator/health` on.
≥1 test per AC. Controllers: `@WebMvcTest` + `@MockitoBean`. Domain: plain JUnit.
Persistence tests: slice + Testcontainers if Docker is up; else say so in Notes.
`./mvnw -q verify` before CODE_REVIEW.
