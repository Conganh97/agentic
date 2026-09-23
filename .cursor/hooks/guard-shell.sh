#!/bin/bash
# beforeShellExecution guard for agents (humans in their own terminal are not affected).
input=$(cat)
cmd=$(printf '%s' "$input" | jq -r '.command // empty')
cwd=$(printf '%s' "$input" | jq -r '.cwd // empty')
lower=$(printf '%s' "$cmd" | tr '[:upper:]' '[:lower:]')

deny() {
  jq -n --arg m "$1" '{permission: "deny", user_message: ("Blocked by guard-shell: " + $m), agent_message: ("Blocked by .cursor/hooks/guard-shell.sh: " + $m + ". Do not work around this; report it to the user.")}'
  exit 0
}

ask() {
  jq -n --arg m "$1" '{permission: "ask", user_message: $m, agent_message: ("guard-shell requires human approval: " + $m)}'
  exit 0
}

if [[ "$lower" =~ git([[:space:]]+-c[[:space:]]+[^[:space:]]+)*[[:space:]]+push ]]; then
  [[ "$lower" =~ (^|[[:space:]])(--force|--force-with-lease|-f)([[:space:]=]|$) || "$lower" =~ [[:space:]]\+[^[:space:]]+ ]] \
    && deny "force push is not allowed"
  if [[ "$cwd" == */product || "$cwd" == */product/* || "$lower" =~ (-c[[:space:]]+|cd[[:space:]]+)[^[:space:]]*product ]]; then
    [[ "$lower" =~ push[^\;\&\|]*[[:space:]:](main|master)([[:space:]]|$) ]] && deny "direct push to main in product/ is not allowed"
  fi
fi

[[ "$lower" =~ (^|[[:space:];&|])gh[[:space:]]+repo[[:space:]]+(delete|rename|archive) ]] \
  && deny "deleting, renaming or archiving GitHub repositories is not allowed"

[[ "$lower" =~ git[^\;\&\|]*push[^\;\&\|]*(--delete|[[:space:]]-d[[:space:]]|[[:space:]]:)[^\;\&\|]*(main|master)([[:space:]]|$) ]] \
  && deny "deleting a remote main branch is not allowed"

[[ "$lower" =~ (^|[[:space:];&|])git[[:space:]]+(-c[[:space:]]+[^[:space:]]+[[:space:]]+)*commit[^\;\&\|]*(--no-verify|[[:space:]]-[a-z]*n[a-z]*([[:space:]]|$)) ]] \
  && deny "git commit --no-verify bypasses the task workflow check"

[[ "$lower" =~ (^|[[:space:];&|])rm[[:space:]]+(-[a-z]*r[a-z]*f|-[a-z]*f[a-z]*r|-r[[:space:]]+-f|-f[[:space:]]+-r|--recursive[[:space:]]+--force|--force[[:space:]]+--recursive) ]] \
  && deny "rm -rf is not allowed"

[[ "$lower" =~ (^|[^a-z_])(drop[[:space:]]+(table|database|schema)|truncate([[:space:]]+table)?[[:space:]]+[a-z_\"]) ]] \
  && deny "destructive SQL (DROP/TRUNCATE) is not allowed"

[[ "$lower" =~ (deploy|release|kubectl|helm|terraform[[:space:]]+apply) && "$lower" =~ (^|[^a-z])prod(uction)?([^a-z]|$) ]] \
  && ask "This looks like a PROD deployment. Approve only if the task has approved_by set by a human."

echo '{"permission": "allow"}'
exit 0
