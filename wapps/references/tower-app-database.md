# Tower-managed application database

Use this pattern when a WApp should be independently deployable and stateless at rest while Tower manages its Postgres persistence. Keep the language and design app-generic: application-specific business logic remains in the WApp.

## Responsibility boundary

```text
browser
  -> WApp frontend
  -> thin WApp server / realtime gateway
  -> exact app-signed NIP-98 requests
  -> Tower generic app DB API
  -> isolated Postgres schema
```

The WApp owns:

- its UI, authentication/session handling, authorization, validation, and business invariants;
- its versioned migration files and data model;
- realtime broadcasts and reconnect protocol;
- orchestration of Autopilot, agents, and external services.

Tower owns:

- the physical Postgres connection and credentials;
- namespace allocation and isolation;
- migration validation, locking, execution, and history;
- bounded table CRUD/query execution and platform limits.

Do not add application-specific routes, tables, or business rules to Tower merely to use this pattern.

## Namespace and tenancy

Tower allocates one schema for each `(workspace_owner_npub, app_npub)` pair and persists the mapping. Discover the namespace through Tower; never guess a schema name or send schema-qualified table names.

Choose tenancy deliberately:

- **Shared service namespace:** one service-owned workspace and app namespace, with tenant/account IDs in app tables. This is simplest for a centrally operated SaaS WApp.
- **Workspace-per-customer namespace:** provision the same app in each customer workspace when hard schema isolation and independent lifecycle justify the added provisioning overhead.

Document which model the app uses. Do not accidentally mix both models.

## Provision and migrate

Use the current generic routes under:

```text
/api/v4/workspaces/:workspaceOwnerNpub/apps/:appNpub/db
```

Typical startup or deployment flow:

1. Register/provision the app identity and workspace binding through the supported Tower/WApp management path.
2. Read `GET .../db/descriptor` and provision with `POST .../db/provision` when needed.
3. Keep ordered migration files in the WApp repository.
4. Calculate each migration checksum and submit `{ version, checksum, sql }` to `POST .../db/migrations` using the app identity.
5. Inspect `GET .../db/migrations` before assuming schema state.
6. Access application tables through `.../db/tables/:table/...` CRUD/query routes.

Migrations are restricted to Tower's allowlisted DDL and the allocated schema. Do not rely on extensions, functions, triggers, grants, cross-schema references, arbitrary SQL, or direct Postgres credentials. Inspect the live Tower contract before introducing a migration feature that may be outside the allowlist.

## Authentication and secrets

Use a dedicated WApp service/app Nostr identity for server-to-Tower requests. Inject its signing credential through the deployment platform's protected runtime configuration or an approved signing broker.

- Never commit the credential or put it in an image layer.
- Never expose it through `VITE_*`, client-side configuration, browser storage, logs, or API responses.
- The WApp server signs the exact Tower URL, HTTP method, and body hash with NIP-98.
- Browsers authenticate to the WApp. The WApp enforces user and guest permissions, then performs authorized storage operations as the app service.
- Record actor fields such as `created_by_npub` when domain records need user attribution; the app identity must not be presented as the human actor.

Provision/descriptor operations may permit an authorized administrator or Tower service signer. Typed migrations and table operations require the registered app signer in the current contract. Verify the current route implementation rather than assuming all signers have the same authority.

## Stateless deployment boundary

"Stateless" means a container restart does not lose accepted durable state. It does not mean every byte belongs in Postgres.

- Put relational business state in the Tower app namespace.
- Put source history in Git/Forgejo.
- Put large files and immutable release artifacts in object storage.
- Store their IDs, URLs, checksums, versions, and status in Postgres.
- Treat local build directories, caches, connections, and in-process queues as disposable; persist or publish required results before cleanup.
- A browser database such as IndexedDB/Dexie is a cache/outbox, not cross-device authority.

## Realtime and consistency

Tower's generic app DB API is persistence, not a complete realtime backend. The current contract does not provide an app-table event stream, arbitrary joins/aggregates, or a multi-operation transaction endpoint.

For collaborative apps:

- accept commands through the WApp server;
- validate membership and current state there;
- use stable IDs and idempotency keys for retryable writes;
- serialize critical multi-step operations when the bounded API cannot express one transaction;
- broadcast only after Tower acknowledges the committed write;
- give clients an ordered cursor/sequence and a snapshot/replay path for reconnects.

Before relying on stricter invariants, inspect the live Tower API and tests. If a missing feature is generally useful, design a generic Tower capability. Otherwise keep the requirement inside the WApp or its purpose-built service.
