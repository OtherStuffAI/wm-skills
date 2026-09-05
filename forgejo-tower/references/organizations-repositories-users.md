# Organizations, Repositories, Users, and Sharing

Use Tower's NIP-98 APIs for desired state and the reconciler for Forgejo state. Use the live Tower OpenAPI for exact schemas.

## Organization model

Each Tower workspace maps to a Forgejo organization. Choose a readable, globally unique namespace before creating the first repository:

```text
PUT /api/v4/git/workspaces/<workspace-id>/namespace
{"namespace":"studio"}
```

Examples:

```text
https://forgejo.example/studio/kindling
https://forgejo.example/wm-owner/tower
```

The namespace becomes locked when the first repository is created. Do not rename the Forgejo organization manually; Tower currently requires an explicit future namespace migration for that operation.

## Headless actor bootstrap and usernames

From an active Autopilot agent session, use the shipped broker-backed CLI:

```bash
cd "${AUTOPILOT_REPO:-$HOME/code/wm/autopilot}"
bun clis/wingman.ts forgejo username set --username agent-name
bun clis/wingman.ts forgejo bootstrap request
bun clis/wingman.ts forgejo bootstrap status
bun clis/wingman.ts forgejo repositories list
```

The username command is optional. The broker discovers the active Tower and workspace from the session's active subscription; no product hostname belongs in a script. If there is more than one active Tower binding, specify `--tower-url <advertised-Tower-origin>`. Optional `--workspace <uuid>` asserts the session workspace; it does not switch authority to another workspace.

`bootstrap request` is idempotent and returns `202` with a `bootstrap` object. Poll `bootstrap status` until its `state` is `ready`, or diagnose `last_error_code` when `error`. `account_state` and `organization_state` explain which stage is pending. `not_requested` means no request exists yet. A pending account with `git_forgejo_oidc_source_unconfigured` needs the Tower operator to configure the isolated identity worker. Keep polling bounded; report a persistent error to the operator with its code.

Tower APIs behind these commands are:

```text
GET/POST /api/v4/git/workspaces/<workspace-id>/actor-bootstrap
GET/PUT  /api/v4/git/workspaces/<workspace-id>/actor-username
PUT body: {"username":"agent-name"}
```

The isolated identity worker creates the external account using Tower's configured OIDC source and immutable actor UUID, links the numeric provider ID, and uses Forgejo's supported rename API for name changes. Username conflicts fail explicitly. Existing linked accounts keep their provider ID. No browser first login, human signer, raw nsec, stored user PAT, or manual provider account is needed. Do not revoke and restore grants to unblock bootstrap.

Account/organization `ready` does **not** grant repository access. An empty repository list means no visible effective grants; ask the workspace repository administrator to verify the actor or stable-group grant. Workspace membership alone does not authorize clone or push. Repository reconciliation and its desired/applied policy revisions must also be ready before Git works.

Use the repository's HTTPS clone URL on the Tower-advertised Forgejo gateway. `repositories list` identifies the authorized repositories and their canonical `git_path`; do not assume it returns a complete clone URL:

```bash
git-credential-wingman --version
git clone <advertised-clone-url>
git -C <checkout> fetch origin
```

Autopilot supplies the shipped `git-credential-wingman` in `PATH` and host-scoped Git configuration with `credential.useHttpPath=true`. Fresh sessions receive the active gateway configuration. Never substitute a shell helper that signs Tower requests directly: it bypasses the supported session broker path. Helper errors contain a safe stage, HTTP status, and Tower code. Repository resolution denials require checking workspace and grants; bootstrap/reconciliation errors require checking the corresponding Tower status and worker health.

The provider authentication actor and Git commit author are separate evidence; set normal Git author config when needed.

## Create a repository

Workspace owners/admins register private repositories through Tower:

```text
POST /api/v4/git/workspaces/<workspace-id>/repositories
{
  "slug":"kindling",
  "display_name":"Kindling",
  "description":"Shared Kindling repository",
  "scope_id":null
}
```

Tower creates an administrator grant for the creating actor and protected service-managed rules for `main`, `staging`, and `deployed`. The provider repository is created only after reconciliation.

The isolated organization worker automatically retries pending repositories after account and grant changes. An operator can also reconcile one repository by UUID from the Tower host:

```bash
docker compose --project-name wingman-tower --env-file .env.prod \
  -f docker-compose.prod.yml --profile tools run --rm git-reconciler \
  <repository-uuid>
```

Verify Tower's binding is `ready` with matching desired/applied policy revisions before browser or Git use.

## Share with people, agents, or groups

On a gateway with the sharing bridge deployed, open the repository’s **Settings → Collaborators** page. Select **Load sharing with Nostr**, using the identity with an explicit Tower `git.repo.admin` grant. Select a ready workspace actor or a Tower group and save Read, Write, or Administrator access. The browser signs the exact change; the page reports saved/pending until the stock provider has applied it. Reload to check. Older gateway releases do not bridge Forgejo UI edits; do not treat provider-only access as a successful grant.

Write includes fetch, work/feature branch pushes and branch creation. Protected branches retain their rules. Remove revokes all direct permissions for that selected principal; grants inherited from other groups remain. Change the relevant group grant to remove inherited access. Each change checks the page’s policy revision: if sharing changed concurrently, reload and submit the intended change again.

The Forgejo Owners and `tower-members` teams represent organization membership, not selectable Tower repository groups. Provider-only team/repository assignments are removed during reconciliation. Choose a stable Tower group for team sharing; no workspace-wide access is implied. Existing provider-only collaborator rows are not imported: the repository administrator must submit the intended sharing through this page after rollout.

The page uses `GET/POST /api/v4/git/forgejo/sharing/<organization>/<repository>` with NIP-98, immutable actor/provider IDs and stable group UUIDs. It does not use a service token to become the administrator. Agents can continue using the existing Tower grant API with their own authorized signer:

Create grants using stable actor or group UUIDs:

```text
POST /api/v4/git/workspaces/<workspace-id>/repositories/<repository-id>/grants
{
  "principal_type":"actor",
  "principal_id":"<actor-uuid>",
  "permission":"git.repo.write"
}
```

Supported permissions:

- `git.repo.read`
- `git.repo.write`
- `git.branch.create`
- `git.repo.admin`

Use a stable group UUID for team access; never use rotating `group_npub` as the principal. Reconcile after grant changes. Revocation increments policy revision so old short-lived capabilities fail closed.

Do not bypass the gateway to add provider collaborators or teams. Git capabilities are rechecked against current Tower policy on every operation; browser repository traffic is held closed while provider reconciliation is pending.

## Configure local repositories

Use the public gateway URL:

```bash
git remote add forgejo https://forgejo.example/<organization>/<repository>.git
git remote -v
```

Install/configure the Autopilot `git-credential-wingman` helper for the host with `credential.useHttpPath=true`. The helper exchanges a fresh NIP-98 proof for a repository/service/scope-bound capability. Do not use a long-lived Forgejo user token as the fallback.

Before pushing, check branch policy. Direct pushes to protected `main`, `staging`, and `deployed` are intentionally unavailable in Tower Git v1; use a work/feature branch and a pull request unless the live policy explicitly provides another service-managed path.

## Verification checklist

- The signed-in user profile shows the intended alias and display name.
- The organization appears for members and the organization root does not 404.
- Repository permissions match Tower grants.
- Revoked users cannot browse, fetch, or push.
- Commit author identity is correct in local Git config; provider authentication actor and commit author are related evidence but not the same field.
- Reconciliation errors are fixed in Tower/provider configuration, not by weakening gateway checks.
