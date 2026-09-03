# Forgejo Actions and CI

Read this before changing Tower Compose, registering a runner, adding workflow files, or giving CI access to secrets.

## Current Tower state

Tower's current production Compose explicitly sets:

```text
FORGEJO__actions__ENABLED=false
```

Actions/CI is therefore a platform extension, not a repository-only change. Do not add a workflow and claim CI is configured while the instance has no enabled Actions service, safe runner transport, and matching runner.

The current gateway also blocks Forgejo API/token access and accepts only Tower capabilities for public smart HTTP. A stock Forgejo Runner needs provider API, job-token, artifact, and checkout traffic that this public gateway does not currently expose. Do not connect workflow job containers to Tower's `git-private` control network as a shortcut.

Use the documentation for the pinned Forgejo major/minor version. Relevant official guides:

- `https://forgejo.org/docs/v16.0/admin/actions/`
- `https://forgejo.org/docs/v16.0/admin/actions/registration/`
- `https://forgejo.org/docs/v16.0/admin/actions/configuration/`
- `https://forgejo.org/docs/v16.0/admin/actions/docker-access/`
- `https://forgejo.org/docs/v16.0/user/actions/quick-start/`

## Design before enabling

Decide and document:

- system-, organization-, or repository-scoped runner;
- trusted repositories and who can edit workflows;
- runner labels and pinned execution images;
- concurrency/capacity;
- network egress and cache policy;
- secret owners and rotation;
- retention for logs/artifacts;
- how runner API/artifact traffic and checkout reach Forgejo without bypassing Tower's public security boundary;
- how CI status maps to Tower protected-branch policy;
- backup and recovery of runner registration/configuration.

Prefer an organization-scoped runner for one Tower workspace. Do not make every workspace share a global runner unless the trust boundary explicitly permits it.

## Isolation requirement

Never expose the host Docker socket used by Tower, Forgejo, Autopilot, or other production services to arbitrary workflow jobs. A job with that socket can inspect, stop, or mutate those services.

Prefer a runner on a separate VM/host or an isolated Docker-in-Docker/LXC boundary. Treat workflows and pull requests as code execution. Untrusted fork pull requests must not receive repository or deployment secrets.

## Required platform seam

Before enabling Actions on a live Tower, implement and test a runner-specific private seam with these properties:

- the runner daemon can reach only the Forgejo endpoints it needs;
- untrusted job containers cannot reach Tower, reconciliation services, provider administration, or secret files;
- checkout uses a Forgejo job token on a provider-internal Git path, not the public Tower-capability path;
- the public browser/API boundary remains unchanged;
- runner registration and Actions secrets remain outside repositories and agent sessions;
- provider check results are reconciled into the exact required-check names Tower protects.

Tower currently stores `required_checks`, but the Forgejo branch-protection reconciler does not yet configure required status checks. Treat required CI enforcement as incomplete until that mapping has implementation and tests.

## Enable the instance after the seam exists

Make the change declaratively in the Tower Compose configuration and add a separately pinned Forgejo Runner service/configuration. At minimum:

1. Set `FORGEJO__actions__ENABLED=true` for Forgejo.
2. Add the reviewed runner-specific network/transport, durable runner configuration, and ignored registration secret storage.
3. Register the runner at the intended organization/repository scope using the supported UI or `forgejo forgejo-cli actions register` inside the provider boundary.
4. Configure labels such as `node22:docker://node:22-bookworm` or another pinned image that contains the tools required by the workflows.
5. Rebuild/restart the affected services and verify the runner is online, can check out through the intended internal path, and cannot reach control services.
6. Implement and validate required-check reconciliation before making CI a protected-branch requirement.

Never print runner registration secrets or store them in workflow files, git config, task comments, or chat.

## Add a workflow

Forgejo reads workflows from `.forgejo/workflows/*.yml`. A small Bun example is:

```yaml
name: CI

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: node22
    steps:
      - uses: https://data.forgejo.org/actions/checkout@v6
      - uses: https://github.com/oven-sh/setup-bun@v2
        with:
          bun-version: "1.3.0"
      - run: bun install --frozen-lockfile
      - run: bun test
```

Adapt commands to the repository's native instructions. For production hardening, pin runner container images by digest and third-party actions to reviewed immutable commits where supported; a moving tag is not reproducible assurance.

## Secrets and deployments

- Repository CI secrets belong in Forgejo's Actions secret store, not in the repository.
- Prefer environment/OIDC or a narrow deployment broker over long-lived infrastructure credentials.
- Do not place Tower service keys, Forgejo reconciliation tokens, human nsecs, or Autopilot bot keys in Actions.
- Separate test/build CI from deployment authority. A passing PR workflow should not automatically gain production access.

## Validate

Verify all of these observably:

- Actions is visible and enabled for the repository.
- The intended runner is online with the exact `runs-on` label.
- A harmless test workflow starts, checks out code, executes, and reports success.
- A failing test reports failure.
- Pull requests from the chosen trust class do not receive protected secrets.
- Workflow jobs cannot access the Tower/Forgejo host Docker daemon or private reconciliation secrets.
- Required checks, if added to branch policy, match the emitted check names and do not deadlock protected branches.

Do not claim CI is complete from YAML validation alone.
