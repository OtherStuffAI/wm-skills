---
name: forgejo-tower
description: "Operate stock Forgejo with Tower Nostr authentication: native accounts, organizations, teams, repositories, permissions, OAuth, Git, issues, pull requests, and CI."
---

# Forgejo with Tower sign-in

Tower authenticates explicitly allowlisted Nostr identities through OIDC. Stock Forgejo owns accounts and usernames after registration, organizations, teams, collaborators, repositories, permissions, branch protections, OAuth credentials, Git, and APIs. This supersedes old Tower grants, capability gateway, issue broker, bootstrap and reconciliation instructions.

Use [setup](references/tower-setup.md) for configuration and migration, [accounts and repositories](references/organizations-repositories-users.md) for native access and Git, [collaboration](references/collaboration-issues.md) for issues and pull requests, and [CI](references/actions-ci.md) before enabling Actions.

## Authentication and authorization

- A new allowlisted identity registers through stock Forgejo's external OIDC login. Preserve existing provider account IDs, Tower OIDC issuer, immutable subjects and source links. Account names and later renames are managed in Forgejo.
- Autopilot's shipped `git-credential-wingman` and session broker perform native Forgejo authorization-code + PKCE login, completing Tower's exact Nostr challenge with the managed signer. Forgejo issues the account's OAuth token. Use the shipped helper; never replace it with a custom signer or shared human credential.
- Credentials are protected per actor and Forgejo host. Never put tokens in Git URLs, logs, source, commands, or agent environment dumps. A management token is never an agent runtime credential.
- Expired credentials are discarded and the same native sign-in is repeated through Tower. Do not introduce Tower Git tokens, refresh authority, or retry a permission denial indefinitely.
- All repository discovery, Git and API traffic goes directly to stock Forgejo, including when a plain reverse proxy preserves its public URL. Native API and token routes are not blocked by Tower.
- Use Forgejo organizations, teams and collaborators to grant/revoke permissions. There is no Tower workspace-to-organization mapping, group replication, repository grant check, permission writer or reconciliation.
- Existing native credentials continue to work while Tower is unavailable. Removing a Nostr identity from Tower's login allowlist prevents new sign-ins; separately revoke native tokens or disable the Forgejo account when immediate access removal is intended.
- Forgejo OAuth scopes are not implemented in the pinned provider; do not describe OAuth credentials as repository-scoped. Native effective permissions and branch protections apply on every request.

## Verify

Verify the authenticated native account, intended native permissions and a real operation through the shipped helper/API path. Change Write to Read in Forgejo and prove push denial using the same issued token; removing all effective read should deny private fetch. Branch protections remain authoritative. No Tower grant or reconciler result constitutes native access evidence.
