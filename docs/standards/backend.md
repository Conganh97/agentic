# Backend Standards — Java Spring Microservices

Applies to everything in `product/services/`. Stack: `project.md`, ADR-0003.

## Service layout

```
services/<name>-service/
├── pom.xml                 # parent: spring-boot-starter-parent 4.0.x, java.version 21
├── mvnw, .mvn/
└── src/
    ├── main/java/com/product/<name>/
    │   ├── <Name>Application.java
    │   ├── api/            # @RestController, request/response DTOs (records), exception handler
    │   ├── service/        # business logic, @Transactional boundaries
    │   ├── domain/         # entities, value objects, domain rules
    │   ├── repository/     # Spring Data interfaces
    │   ├── client/         # RestClient clients to other services
    │   └── config/         # @Configuration, @ConfigurationProperties
    ├── main/resources/
    │   ├── application.yml
    │   └── db/migration/   # Flyway: V1__init.sql, V2__...
    └── test/java/...       # mirrors main
```

Dependencies point inward: `api → service → domain/repository`. Controllers never use repositories directly.
Create only the packages a task needs; trivial logic without dependencies (e.g. formatting) may stay in the
controller until a service is justified.

## New service checklist

- Folder `services/<name>-service/`, artifactId `<name>-service`, package `com.product.<name>`.
- Generate the wrapper: `mvn -N wrapper:wrapper` inside the service folder.
- Spring Boot 4 modular starters (names changed from Boot 3):
  - Web: `spring-boot-starter-webmvc`; tests: `spring-boot-starter-webmvc-test`
  - HTTP client: `spring-boot-starter-restclient`
  - Also `spring-boot-starter-validation`, `spring-boot-starter-actuator`; data: `spring-boot-starter-data-jpa`,
    `flyway-core` + `flyway-database-postgresql`, `postgresql`
- `@WebMvcTest` lives in `org.springframework.boot.webmvc.test.autoconfigure`; mock beans with
  `@MockitoBean` (`org.springframework.test.context.bean.override.mockito`). When unsure about a Boot 4
  API, check the docs (Context7 `/spring-projects/spring-boot`) instead of guessing.
- Distinct default port per service, overridable: `server.port: ${SERVER_PORT:<port>}`; document it in the
  service README.

## REST API

- Paths: `/api/v1/<resource>` (plural nouns, kebab-case). JSON only.
- DTOs are Java `record`s; never expose entities.
- Validate input with Jakarta Validation (`@Valid`, `@NotBlank`, ...). Put constraints directly on
  `@PathVariable`/`@RequestParam` parameters and do **not** add class-level `@Validated`: Spring MVC then
  validates the method itself and raises `HandlerMethodValidationException`, which the default handler maps to 400.
- Bound every free-text input (`@Size(max = …)` on path/query/body fields); never echo unbounded user input
  back in error details.
- Errors: RFC 9457 `ProblemDetail` from one `@RestControllerAdvice` that extends
  `ResponseEntityExceptionHandler`; no stack traces in responses.
- Status codes: 200/201/204 success, 400 validation, 401/403 auth, 404 missing, 409 conflict.
- Breaking API changes need a new version path and an SA-approved design.

## Persistence

- Database per service; no service reads another service's tables.
- Schema changes only via Flyway migrations; never edit an applied migration.
- `spring.jpa.hibernate.ddl-auto=validate`.

## CORS (browser + Vite proxy)

When the FE calls the API through the Vite `/api` proxy, the browser still sends `Origin` as the
page origin. Spring CORS that allows only `http://localhost:<port>` **rejects** `http://127.0.0.1:<port>`
with **403 `Invalid CORS request`** (register/login/cart POSTs fail in the browser).

- `allowedOrigins` must include **both** `http://localhost:<FE_PORT>` and `http://127.0.0.1:<FE_PORT>`
  (default FE port 15173 unless the design says otherwise).
- `allowCredentials(true)` when cookies/sessions are used.
- Tests must assert both origins (a test that only uses `localhost` will miss this).

## Cross-service calls

- `RestClient` in `client/`, base URL from configuration, explicit timeouts.
- Handle failures of other services explicitly (map to 503/502 or fallback defined in the design).

## Code rules

- Constructor injection only; no field `@Autowired`.
- `enum` for fixed sets, `record` for immutable data, `Optional` instead of returning `null`.
- Specific exceptions; never catch `Exception` broadly or swallow errors.
- Configuration via `application.yml` + environment variables; no secrets in code or config files.
- Logging with SLF4J; never log passwords, tokens or personal data.
- Actuator health enabled (`/actuator/health`).

## Testing

- Every acceptance criterion has at least one test; name tests after behaviour
  (e.g. `loginWithInvalidPasswordReturns401`).
- Controllers: `@WebMvcTest` + `MockMvcTester`/`MockMvc`, services mocked with `@MockitoBean`.
- Services/domain: plain unit tests (JUnit 5 + AssertJ + Mockito), no Spring context.
- Repositories: `@DataJpaTest` with Testcontainers PostgreSQL (needs Docker).
- Actuator/wiring checks: `@SpringBootTest` + `@AutoConfigureMockMvc` (mock servlet; no real port).
- `./mvnw -q verify` must pass before CODE_REVIEW.
