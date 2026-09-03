# Collaboration, Issues, and Pull Requests

Use this reference after organization membership, repository grants, and Git credentials are working.

## Share work

1. Grant the person, agent, or Tower group the least repository permission needed.
2. Reconcile and verify provider membership/access.
3. Work on `work/<name>` or `feature/<name>` branches.
4. Push through the Tower gateway with a short-lived capability.
5. Open a Forgejo pull request into the protected target branch.
6. Review code, checks, approvals, and mergeability in Forgejo; keep task intent and human coordination in Flight Deck.

Do not use shared human credentials for agents. Each human or agent actor should have its own Tower identity and Forgejo alias so gateway audit and provider activity remain attributable.

## Decide between a Forgejo issue and Flight Deck task

Use a Forgejo issue for repository-local engineering work:

- defects tied to code in one repository;
- proposed changes, technical debt, or release work;
- discussion that should link directly to commits and pull requests.

Use a Flight Deck task for cross-repository, operational, customer, or supervised-agent work:

- work spanning Tower, Flight Deck, Autopilot, WApps, or deployment;
- approvals, user communication, artifacts, or business context;
- work that needs agent assignment and same-thread handoff.

When both are useful, make one canonical and cross-link them. Avoid copying diverging descriptions and status into both systems.

## Tower issue API

Use Autopilot's Wingman CLI for normal agent issue work. It obtains the
session agent's short-lived NIP-98 proof from the capability broker and calls
Tower; it never accepts a human key or Forgejo token:

```bash
bun clis/wingman.ts forgejo issues list \
  --workspace <workspace-id> --repo <repository-id> --state open
bun clis/wingman.ts forgejo issues read 1 \
  --workspace <workspace-id> --repo <repository-id>
bun clis/wingman.ts forgejo issues create \
  --workspace <workspace-id> --repo <repository-id> \
  --title "Outcome-oriented title" --body-file issue.md
bun clis/wingman.ts forgejo issues comment 1 \
  --workspace <workspace-id> --repo <repository-id> --body-file update.md
```

The CLI wraps these Tower routes, which remain the contract and diagnostic
reference:

```text
GET  /api/v4/git/workspaces/<workspace-id>/repositories/<repository-id>/issues
GET  /api/v4/git/workspaces/<workspace-id>/repositories/<repository-id>/issues/<number>
POST /api/v4/git/workspaces/<workspace-id>/repositories/<repository-id>/issues
POST /api/v4/git/workspaces/<workspace-id>/repositories/<repository-id>/issues/<number>/comments
```

List/read requires any active repository grant. Create/comment requires
`git.repo.write` or `git.repo.admin`. Use the live Tower OpenAPI for exact
schemas.

Create body:

```json
{
  "title": "Outcome-oriented issue title",
  "body": "Evidence, expected behavior, and acceptance criteria",
  "correlation_id": "optional-session-or-task-correlation"
}
```

Comment body:

```json
{
  "body": "Repository-local update",
  "correlation_id": "optional-session-or-task-correlation"
}
```

Create/comment requires a strict NIP-98 event signed for the exact complete
Tower URL, method, and exact serialized body payload hash. The event is valid
for 60 seconds and consumed once. A retry of a successful event returns the
cached provider result without duplicating the mutation. Generate the proof
through the active user/agent signer; never search for or inject a human nsec.

Tower resolves the signer to its logical actor, verifies the current repository
grant and exact Forgejo reconciliation revision, and records actor, signer,
operation, policy revision, and correlation in immutable Git audit evidence.
The private issue broker attributes the provider mutation to the actor's applied
Forgejo username. It exposes no provider token or public port.

## Human issue workflow

The current safe path is Forgejo's authenticated browser UI:

- open the organization/repository through the public gateway;
- select **Issues** to read, filter, or search issues;
- choose **New Issue** to log a problem;
- provide an outcome-oriented title, reproduction/evidence, expected behavior, acceptance criteria, and relevant branch/task links;
- use assignees, labels, milestones, and comments where the repository has defined them;
- close only when the linked change and validation are complete.

To reference work in commits or pull requests, use Forgejo's normal issue syntax supported by the live version, and verify the resulting link in the UI.

## Agent issue rules

An unattended agent may list, read, create, and comment through Tower's signed
issue routes. It must not:

- call `/api/v1` through a bypass;
- receive the control/identity reconciliation token;
- publish Forgejo's private port;
- call the private issue broker directly or receive its Tower token;
- claim success until Tower returns the normalized Forgejo issue/comment and,
  where practical, a follow-up read confirms it.

Pull-request creation, reviews, labels, assignments, issue edits/closure, and
other provider mutations remain browser-only until Tower exposes an explicitly
authorized route for them.

## Issue templates

Repository maintainers may add Forgejo-supported issue templates under the repository's `.forgejo` configuration. Verify the format against the documentation for the pinned Forgejo version before committing templates. Keep templates brief and focused on evidence and acceptance criteria rather than process ceremony.
