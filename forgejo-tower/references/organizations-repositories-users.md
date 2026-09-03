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

## Human and agent usernames

An actor's npub/UUID remains authoritative. A readable Forgejo username is a global mutable alias:

```text
GET /api/v4/git/workspaces/<workspace-id>/actor-username

PUT /api/v4/git/workspaces/<workspace-id>/actor-username
{"username":"pw21"}
```

The PUT returns `202`. Continue using `applied_username` until state becomes `ready`; the identity reconciler performs a stock Forgejo rename and acknowledges it. Never delete/recreate the actor merely to change the username.

Use the Tower/Flight Deck profile display name for a human-readable contribution label. Keep the username short and stable enough for URLs and Git attribution.

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

Reconcile by repository UUID from the Tower host:

```bash
docker compose --project-name wingman-tower --env-file .env.prod \
  -f docker-compose.prod.yml --profile tools run --rm git-reconciler \
  <repository-uuid>
```

Verify Tower's binding is `ready` with matching desired/applied policy revisions before browser or Git use.

## Share with people, agents, or groups

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

Do not manually add Forgejo collaborators or teams as the only access record. Tower reconciliation may remove or supersede them, and the gateway still checks Tower on every browser request.

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
