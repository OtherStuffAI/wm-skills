# Issues, pull requests and reviews

Forgejo owns repository collaboration. Use its native UI or direct `/api/v1` API with the actor's own Forgejo OAuth credential obtained by Autopilot's session broker. Tower does not proxy issue operations, check repository grants, or replace native attribution.

The shipped CLI accepts the native owner/repository name (`FORGEJO_URL` may
supply the default origin):

```bash
bun clis/wingman.ts forgejo issues list --repo owner/repository --forgejo-url https://forgejo.example
bun clis/wingman.ts forgejo issues read 1 --repo owner/repository --forgejo-url https://forgejo.example
bun clis/wingman.ts forgejo issues create --repo owner/repository --forgejo-url https://forgejo.example --title "Fix native login" --body-file issue.md
bun clis/wingman.ts forgejo issues comment 1 --repo owner/repository --forgejo-url https://forgejo.example --body-file update.md
bun clis/wingman.ts forgejo pulls create --repo owner/repository --forgejo-url https://forgejo.example --head work/fix --base main --title "Fix native login" --body-file pr.md
```

The native API paths include:

```text
GET  /api/v1/user/repos
GET  /api/v1/repos/<owner>/<repo>/issues
GET  /api/v1/repos/<owner>/<repo>/issues/<number>
POST /api/v1/repos/<owner>/<repo>/issues
POST /api/v1/repos/<owner>/<repo>/issues/<number>/comments
POST /api/v1/repos/<owner>/<repo>/pulls
```

Use the shipped Autopilot Forgejo CLI/API client for agent work, with the advertised Forgejo origin and native owner/repository name. The client obtains and stores credentials through the broker; do not paste tokens into shell commands. Native issue create takes `title` and `body`; comments take `body`; pull requests specify native `head`, `base` and `title`. Read the instance's native API schema for additional operations and exact fields.

Write an outcome-oriented title with reproduction, evidence, expected behavior and acceptance criteria. Verify a returned issue/comment/PR URL and follow-up native read. Forgejo authenticates and enforces effective account permissions. A denial needs a native collaborator/team/branch-policy check, not a Tower grant or reconcile call.

Use a Forgejo issue for repository-specific engineering discussion. Use Flight Deck for cross-repository planning, supervised assignments, approvals or business context. Cross-link one canonical record instead of maintaining divergent descriptions. Open native pull requests for protected targets and review checks/approvals in Forgejo.
