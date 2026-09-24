# UX/UI Standards

Artifacts: `docs/design/ux/` + Figma file (ADR-0008). Skill: `.cursor/skills/ux-ui/SKILL.md`.

Required when `work_type: FRONTEND` or `requires_uxui: true`. Skip for BE/infra/DevOps and for
Playwright-only (`requires_uxui: false`).

## Outputs

| Kind | Where |
|------|--------|
| Machine contract | `docs/design/ux/REQ-###-ux.md`, tokens, page specs (`templates/ux-*.md`) |
| Visual (review) | Figma file URL + frame ids on the task `figma:` field |
| FE review | `docs/design/ux/reviews/TASK-###-review-NN.md` |

Small REQ: one spec + tokens + one Figma file.

Must define: brand/tokens, reusable components, named flows, per-page layout + 4 states,
responsive **layout change**, a11y, real image slots, **density** (fold contents at 390 / 1280).
Kit-default or sparse (chrome + empty canvas) pages are not done.

PQA reviews the contract and the FE (ADR-0010). UX/UI does not approve its own look.

## FE

Implement the markdown **and** the Figma frames. Ambiguity → `BLOCKED` for UX/UI.
A kit-correct page that ignores the spec/Figma is MAJOR.

## Figma

Official MCP: `.cursor/mcp.json` → `https://mcp.figma.com/mcp` (OAuth in Cursor Settings → Tools & MCP).
Write tools: `create_new_file`, `generate_figma_design`, `use_figma`, `get_screenshot`.
Markdown stays the workflow contract; Figma is how humans review the look. Task **status** never
lives in Figma. If MCP is `needsAuth`, stop and ask the human to Connect — do not skip Figma on a
UI task.
