---
name: forgejo-tower
description: "Set up and operate Tower-backed Forgejo: install the private forge, create workspace organizations and repositories, choose human usernames, grant users or agents access, collaborate through issues and pull requests, and plan or enable Forgejo Actions/CI."
---

# Tower-backed Forgejo

Use this skill for Git collaboration on a Wingman Tower. Tower is the identity, workspace, repository, grant, capability, and audit authority. Stock Forgejo is the private Git/issue/PR/review provider and enforcement replica.

Do not create a Forgejo fork, mutate its database, hand out the reconciliation tokens, or manually use Forgejo collaborators/teams as the canonical access model.

## Select the workflow

- Read [references/tower-setup.md](references/tower-setup.md) to install or repair the Tower/Forgejo stack, bootstrap provider identities, configure ingress, or validate health.
- Read [references/organizations-repositories-users.md](references/organizations-repositories-users.md) to claim an organization namespace, select human usernames, create repositories, grant actors/groups access, reconcile Forgejo, or configure Git remotes.
- Read [references/collaboration-issues.md](references/collaboration-issues.md) to share work, use branches/pull requests, log or read issues, or decide whether an issue belongs in Forgejo or Flight Deck.
- Read [references/actions-ci.md](references/actions-ci.md) before enabling Actions, adding a runner, writing workflows, handling CI secrets, or diagnosing jobs.

## Authority rules

- One Tower workspace maps to one Forgejo organization; repositories belong to that organization.
- Workspace/repository UUIDs remain stable. The organization namespace and actor usernames are readable aliases.
- Claim the organization namespace before creating the first repository. It becomes locked after repository creation.
- Bootstrap headless actors through the Autopilot `forgejo bootstrap` CLI; see the organizations/users reference. Readiness and repository grants are separate.
- Change actor usernames through Tower. The identity reconciler uses Forgejo's supported rename API.
- Share repositories with Tower actor or stable-group UUID grants, then reconcile. Do not grant access only in Forgejo.
- Tower workspace owners/admins map to Forgejo's stock Owners team. Other authorized actors are organization members without blanket repository access; exact repository access comes from Tower grants.
- Git credentials are short-lived Tower capabilities obtained through a NIP-98-aware credential helper. Do not store Forgejo user tokens in repositories or agent environments.
- The public gateway deliberately blocks Forgejo's API and credential-management surfaces. Never bypass it by publishing Forgejo port 3000.

## Current capability matrix

| Workflow | Current supported path |
|---|---|
| Human browser login | Gateway Nostr challenge and short Tower session |
| Git clone/fetch/push | Stock Git plus Tower capability credential helper |
| Organization/repository provisioning | Tower NIP-98 API plus on-demand reconciler |
| Headless account bootstrap | Broker-signed Autopilot CLI → Tower → isolated identity worker |
| User aliases | Tower actor-username API plus isolated identity reconciler |
| Sharing | Tower actor/group grants plus reconciliation |
| Issue list/read/create/comment | Tower NIP-98 issue API and isolated private broker |
| Pull requests and reviews | Forgejo browser UI for authorized humans |
| Actions/CI | Disabled and not yet safely bridged through the current gateway; requires the platform seam in the Actions reference |

## Verification

For every mutation, verify both authority and provider state:

1. Tower shows the intended namespace, repository, grant, and ready reconciliation revision.
2. Forgejo shows the expected organization membership and repository permission.
3. The public gateway allows the authorized path and denies a foreign organization/repository.
4. Git operations use the expected human/agent identity in audit and commit attribution.

Do not treat a successful direct Forgejo edit as completion when Tower does not contain the matching state.
