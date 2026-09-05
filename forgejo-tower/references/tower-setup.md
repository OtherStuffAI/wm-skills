# Tower authentication and stock Forgejo setup

Read the active Tower repository's `agents.md`, `README.md`, `docs/forgejo-native-auth-migration.md`, production env example and Compose manifest. The migration document supersedes historical `git-authority-v1` and rollout documents.

The stack retains Tower OIDC, stock Forgejo 16.0.3 and an optional plain reverse proxy for the existing public URL. There are no identity/org/repository permission workers, issue broker, Tower capabilities or custom sharing intercept. Old worker bootstrap scripts are retired and must fail closed.

Configure `GIT_OIDC_ALLOWED_NPUBS` explicitly. Preserve `GIT_OIDC_ISSUER`, OIDC signing key, client ID/secret, callback URL and existing provider source/subject links. Keep secret files protected; never print resolved deployment environments. Provider reverse-proxy authentication must be off; native OAuth/API/Git must be reachable at the public Forgejo URL. Accounts register via the configured external provider. Never auto-link an existing account by matching an unverified alias/email.

For existing deployments, use the repository's migration handoff. Stop all old workers and scheduled/on-demand launchers and retain actual task/process proof before cutover. Snapshot Tower DB, provider DB/data/config, account IDs and OIDC links, native teams/collaborators and branch protections. Preserve old Tower grant rows read-only for audit. Restore intended access once through native Forgejo APIs after writers are disabled. Do not restart old workers during rollback.

Validate with stock Forgejo plus the actual shipped Autopilot broker/helper: fresh registration/login, direct Git/API writes, expiry re-login, unlisted denial, native permission revocation with the same token, branch protections and Tower outage with a still-valid native token. Do not claim Lara is fixed until tested in her actual runtime.

Autopilot configures `WINGMAN_FORGEJO_SERVERS` server-side as a JSON array of
`{origin,towerIssuer,sourceName,clientId,redirectUri}` bindings. These are public
routing/client identifiers, not credentials. The shipped helper version is 3.
Native tokens are cached in process-private memory per actor and host; restart
loses the cache and the next use signs in again. No token goes into disk, agent
environment or remote URLs. Use the stock public OAuth client, not an admin
application; preserve state, PKCE, CSRF and exact callback checks.

## Portable skills

The canonical source is `OtherStuffAI/wm-skills`. Sync only the requested skill into installed copies, preserving unrelated skills:

```bash
python3 scripts/sync-skills.py sync --skill forgejo-tower \
  --codex-dir "$HOME/.codex/skills" --claude-dir "$HOME/.claude/skills"
python3 scripts/sync-skills.py check --skill forgejo-tower \
  --codex-dir "$HOME/.codex/skills" --claude-dir "$HOME/.claude/skills"
```

Lara's automation pulls the published canonical skill. Source commits and local sync do not prove her deployed helper or runtime changed. For a task awaiting manager review, commit tested state and provide evidence; do not push, deploy or restart Autopilot. Follow the task's explicit rollout authorization.
