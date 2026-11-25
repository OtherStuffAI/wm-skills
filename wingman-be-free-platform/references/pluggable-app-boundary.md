# NStack pluggable application boundary

## Target and current contracts

NStack is a reusable backend for independently developed applications. Apps own their domain schema, tables or collections, validation and business rules in an isolated application namespace. A normal app feature should be deliverable without editing or redeploying NStack. NStack owns shared identity, authorization, namespace isolation, storage and reusable persistence/synchronization guarantees.

This is the design target, not a claim that every existing API satisfies it. The current source includes namespaced relational app databases, JSON app rows, organization data, napplet collections and typed Flight Deck PG services. Inspect their actual signer, ACL, query, concurrency, revision and realtime contracts before selecting one. A trusted app-signed database API is not automatically safe for an end-user client; namespace isolation alone does not supply row-level permissions.

Existing typed Flight Deck routes and data remain supported while app-owned equivalents are designed and verified. Keep exact machine routes, schemas and identities. Neither replacing them with legacy encrypted records nor moving data into a new catalogue is implied.

## Feature decision

Before proposing a route, table, migration or shared contract change:

1. State the app-owned data and behavior, and identify the supported generic contracts that could express it. Read the authoritative code/OpenAPI and relevant contract docs; verify the selected target's availability.
2. Check the complete behavior: registration and schema evolution, identity/delegation, per-user/group access, bounded queries, atomicity and conflict handling, storage/revisions, realtime and recovery. Record what is implemented, missing or unverified.
3. Implement app meaning through an existing suitable generic interface. For existing Ambulando Docs/Files, preserve canonical records, access, immutable versions, comments and assets using their supported routes.
4. When a generic contract is insufficient, describe a reusable capability gap, at least two plausible independent consumers and acceptance checks. The primitive must retain server-enforced authorization, validation, namespace isolation, resource limits and concurrency guarantees. Keep app vocabulary, template/editor registries and domain workflows in the application. An app-specific endpoint is not the default remedy.
5. Treat any extraction or migration as separate scoped implementation. Preserve IDs, history, ACLs, signatures, cursors, retries and all current consumers; prove recovery and rollback before activation. Do not weaken controls or expose unrestricted SQL to make a generic API appear complete.

## Completion evidence

A reusable backend extension must be demonstrable by a small independent application using published contracts without NStack source edits or an NStack deployment for each app feature. Include tests for cross-namespace denial, unauthorized access, stale/concurrent writes and recovery. Document remaining gaps rather than declaring the backend fully pluggable from endpoint names or a schema descriptor alone.
