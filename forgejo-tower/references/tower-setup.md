# Tower and Forgejo Setup

Use this reference for a new Tower, a first Forgejo deployment, ingress changes, provider identity bootstrap, or runtime recovery.

## Read first

In the active Tower repo, read:

- `AGENTS.md` or `agents.md`
- `README.md`
- `docs/prod-deploy.md`
- `docs/git-authority-v1.md`
- `.env.prod.example`
- `docker-compose.prod.yml`

Treat those files as authoritative for the checked-out version. The current stack pins stock Forgejo and keeps it private behind `git-gateway`.

## Prepare configuration

For a fresh deployment, copy and complete the production template. For migration from an existing Tower, prefer the provided preparation script because it creates separate ignored Git secrets without printing them:

```bash
cd "${TOWER_REPO:-$HOME/code/wm/tower}"
./scripts/prepare-tower-git-deployment.sh /absolute/path/to/existing/.env.prod
docker compose --project-name wingman-tower --env-file .env.prod \
  -f docker-compose.prod.yml config --quiet
```

Required Git settings include:

- a unique capability hash key;
- a unique internal gateway token;
- `GIT_SERVICE_AUDIENCE`, normally `wingman-git`;
- a unique Forgejo webhook secret;
- a unique Tower-to-issue-broker token;
- private Tower and Forgejo origins;
- the exact public HTTPS `GIT_GATEWAY_BROWSER_ORIGIN`.

Keep secret values in ignored files under `.runtime/tower-git-secrets/`. Do not reuse the Tower service nsec or place secrets in chat, argv, committed env files, or resolved Compose output.

## Start the stack

```bash
docker compose --project-name wingman-tower --env-file .env.prod \
  -f docker-compose.prod.yml up -d --build

curl -fsS http://127.0.0.1:${TOWER_HOST_PORT:-3100}/health
curl -fsS http://127.0.0.1:${GIT_GATEWAY_HOST_PORT:-3180}/health
curl -fsS http://127.0.0.1:${GIT_GATEWAY_HOST_PORT:-3180}/ready
```

The expected services include Tower, Postgres, MinIO, Forgejo, the Git gateway,
and the isolated Git issue broker. Forgejo port 3000 and broker port 3190 must
remain unpublished. Route the public Forgejo hostname to the gateway, not
directly to either private service.

## Bootstrap provider identities

After Forgejo is healthy:

```bash
./scripts/bootstrap-forgejo-control.sh
./scripts/bootstrap-forgejo-identity.sh
```

- `tower-reconciler` is a non-site-admin account used only for Tower-managed organizations and repositories.
- `tower-identity-reconciler` is an isolated administrator used only for supported username renames.

Their tokens are mounted only into their dedicated reconciliation processes. Do not expose either token to Tower routes, the gateway, users, agents, or CI jobs.

## Ingress and login smoke

Verify:

- an anonymous browser is redirected to `/auth/login`;
- a valid Nostr login reaches the Forgejo home page;
- an authorized user can open their organization and repository;
- a user without a Tower grant receives a non-disclosing denial;
- public `/api/v1`, registry, internal login, registration, and credential-management paths remain blocked;
- a signed Tower issue create succeeds for an actor with repository write/admin authority and appears under that actor's applied Forgejo username.

Gateway restarts invalidate browser sessions by design.

## Data and recovery

Forgejo data lives in its persistent Docker volume. Tower authority and Forgejo provider data must both be backed up. Do not delete volumes to repair membership, aliases, or reconciliation drift. Reconcile from Tower first.

Only wipe Forgejo data when the user explicitly requests a destructive reset and confirms that repositories, issues, pull requests, attachments, Actions history, and provider configuration may be lost. Resolve the exact Compose project and volume names before removal.
