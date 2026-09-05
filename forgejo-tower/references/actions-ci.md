# Forgejo Actions and CI

Actions remains disabled by default (`FORGEJO__actions__ENABLED=false`). Enabling it is a separate infrastructure change. Use the documentation matching the pinned stock Forgejo version and a separately pinned runner.

Forgejo owns runner registration, job credentials, workflow APIs, artifacts, secrets, check statuses and branch protection. Runner and checkout traffic goes directly to Forgejo using native credentials. No Tower capability bridge, permission replica or required-check reconciler is needed.

Choose organization/repository runner scope, trusted workflow authors, labels, execution images, concurrency, retention and secret owners. Isolate runners from production Docker sockets and Tower/provider management credentials. Untrusted pull-request jobs must not receive secrets or access management networks. Store CI secrets in native Forgejo secret storage, never in source or chat.

After authorization, enable Actions declaratively, register the runner using supported native controls, and add `.forgejo/workflows/*.yml` using the repository's actual build/test commands. Pin third-party actions to reviewed immutable references where practical. Keep deployment authority separate from ordinary test jobs.

Verify a harmless job checks out code and passes, a failing job reports failure, untrusted jobs cannot obtain secrets or host control, and native protected-branch required check names match emitted statuses. YAML validation alone does not prove CI works.
