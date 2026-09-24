# System Overview

## 1. Idea

The team runs inside Cursor. There is no orchestrator service: control comes from a workflow rule that
every agent follows, state comes from markdown files, and git records every change.

```
            HUMAN (requirements, approvals, unblock)
                          │
                   ┌──────▼──────┐
                   │ Scrum skill │  "scrum next": which task, which role
                   └──────┬──────┘
                          │
     ┌────────────────────▼─────────────────────┐
     │  tasks/TASK-###.md  (status = truth)     │◄── workflow rule (.cursor/rules/workflow.mdc)
     │  History table + git commit per change   │◄── pre-commit check, hooks
     └───┬──────────┬──────────┬─────────┬──────┘
         ▼          ▼          ▼         ▼
        SA        BE / FE     TEST     DEVOPS      (Cursor chats using role skills)
         │          │
         │          └──► product/ (one git repo per component, feature branches)
         └──► review ⇄ fix loop ──► MERGED ──► TESTING ⇄ BUG|FAILED ──► DEPLOY ──► RELEASED
```

## 2. Components

| Component | Implementation | Responsibility |
|-----------|----------------|----------------|
| Rules | `AGENTS.md`, `.cursor/rules/workflow.mdc` | Hard rules, state machine, transition protocol |
| Agents | `.cursor/skills/<role>/SKILL.md` | Role-specific reads, outputs and allowed transitions |
| State | `tasks/*.md` frontmatter | Single source of truth per task |
| Index | `tasks/board.md` | Overview of all tasks (derived) |
| Audit | History table + git log | Who changed what, when, why |
| Guardrails | git `pre-commit` + `.cursor/hooks.json` | Reject invalid transitions and dangerous commands |
| Knowledge | `docs/`, `memory/`, `project.md` | Targeted context for agents |
| Product | `product/` | The code being built (separate repo) |

## 3. Workflow

`BACKLOG → READY → IN_PROGRESS → CODE_REVIEW → MERGED → TESTING → READY_FOR_DEPLOY → DEPLOYING → RELEASED`

Loops: `CODE_REVIEW → CHANGES_REQUESTED → IN_PROGRESS` and `TESTING → BUG → IN_PROGRESS`
(max 3 iterations each). Execution failures use `FAILED` (then back to `failed_from`).
Any working state can go to `BLOCKED`; only an explicit unblock returns it.
Dependencies: `python3 scripts/deps.py`. Evidence: workflow §8.

Full transition table with roles and guards: plan §6. Transition protocol: plan §8.

## 4. Why this design

See `docs/adr/0002-markdown-driven-cursor-native-team.md`.
