---
name: wingman-deploy
description: Use when deploying Wingman Be Free apps that use a long-lived deployed branch for CapRover/live builds. Covers validating and committing the source branch, pushing the configured source remote, fast-forwarding deployed, pushing the deployment remote, and returning to normal development.
---

# Wingman Deploy Branch Workflow

Use this skill when the user asks to deploy a Wingman app, push Flight Deck live, update the `deployed` branch, or follow the CapRover deployment pattern.

## Model

Normal development happens on `main` or a feature branch. The live deployment is driven by a remote `deployed` branch. Determine whether the deployment watches `origin`, `forgejo`, or another remote; do not assume GitHub.

The deployment branch should be a fast-forward copy of the source branch. Do not create merge commits on `deployed`.

## Workflow

1. Identify the repo, current branch, remotes, and dirty worktree:

```bash
git branch --show-current
git remote -v
git status --short
git fetch origin --prune
```

2. Preserve unrelated local changes.

- Do not commit unrelated files.
- If branch switching requires a clean tree, stash only the unrelated paths and restore them afterward.
- Call out preserved local changes in the final summary.

3. Identify the source and deployment remotes.

- Use the remote configured by the repository/deployment. Tower-hosted repositories commonly use `forgejo`; older CapRover setups may still watch `origin` on GitHub.
- Fetch the selected remotes explicitly and confirm the deployment target before pushing.

4. Validate and commit on the normal work branch.

- If currently on `deployed`, decide whether the work belongs on `main` first. Prefer committing to `main` or the requested source branch, then fast-forwarding `deployed`.
- Run appropriate tests/build for the change.
- Commit with a descriptive message that does not credit the agent.
- Push the source branch to the configured source remote.

Typical commands:

```bash
git switch main
git merge --ff-only <work-branch>   # only if needed and safe
git push <source-remote> main
```

5. Fast-forward `deployed` from the source branch.

```bash
git switch deployed
git merge --ff-only main
git push <deployment-remote> deployed
```

If `git merge --ff-only` fails, stop and explain why. Do not use a normal merge, rebase, reset, or force push unless the user explicitly asks for that exact recovery.

6. Return to the normal work branch.

After a successful deploy push, switch back to the branch the team should keep working on, normally `main`:

```bash
git switch main
```

Restore any preserved unrelated local changes if they existed.

7. Verify.

```bash
git rev-list --left-right --count <source-remote>/main...main
git rev-list --left-right --count <deployment-remote>/deployed...deployed
git log --oneline --decorate -n 5
git status --short
```

Report:

- source branch and commit SHA;
- `deployed` branch commit SHA;
- tests/build run;
- whether both remotes are fully pushed;
- any unrelated local changes preserved.

## Guardrails

- Never include generated runtime supervisor files, local app registry changes, or unrelated PM2/ecosystem edits unless they are explicitly part of the deployment.
- Do not leave the repository on `deployed` after deployment unless the user asks.
- Do not force push `deployed` as the standard path. The standard path is fast-forward only.
- Do not claim the live system has built successfully unless CapRover or the live URL has actually been checked.
