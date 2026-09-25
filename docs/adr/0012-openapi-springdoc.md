# ADR-0012: springdoc-openapi for REST contract docs

- **Status:** Accepted
- **Date:** 2026-09-25
- **Deciders:** SA (REQ-001)

## Context

REQ-001 requires OpenAPI documentation for the Douyin crawler REST contract so n8n and later
services can consume it. Spring Boot 4 does not ship a Swagger UI renderer.

## Decision

Use **springdoc-openapi** (`springdoc-openapi-starter-webmvc-ui`) on backend services that expose
REST. The runtime contract is the Spring MVC API; OpenAPI is generated from controllers and
Jakarta Validation, not a hand-maintained spec file.

## Consequences

- `/v3/api-docs` and Swagger UI are available in non-prod profiles.
- A new OpenAPI library is an extra dependency; keep it off the domain module’s compile scope.
- Breaking path or field changes still require a new `/api/vN` version (backend standards).

## Alternatives considered

- Hand-written `openapi.yaml` only — rejected: drifts from controllers.
- Spring REST Docs snippets only — rejected: REQ asks for OpenAPI, not Asciidoctor.
