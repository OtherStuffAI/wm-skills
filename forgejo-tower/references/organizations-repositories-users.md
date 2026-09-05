# Accounts, repositories and sharing

Register through stock Forgejo's Tower OIDC login using an explicitly allowlisted Nostr identity. An existing account keeps its numeric ID and immutable OIDC source/subject link. Select a username during native registration when prompted and manage later changes in Forgejo. Tower actor aliases do not rename provider users.

Create organizations, teams and repositories through Forgejo's UI or supported `/api/v1` API under the authenticated native account. Organization ownership is native; Tower workspace membership provides no Forgejo access. Stock Forgejo owns repository URLs and discovery, branch protections, invitations and permission checks.

Share in Forgejo's repository **Settings → Collaborators**, or use native organization teams. Read permits private clone/fetch; Write permits pushes subject to branch protection. Check all effective permissions: removing a collaborator does not remove access inherited through a team. Existing branch protection remains in force after a Write grant.

## Autopilot Git

Use an active Autopilot session with its managed signer and the shipped helper:

```bash
git-credential-wingman --version
git clone https://forgejo.example/organization/repository.git
git -C repository fetch origin
```

Autopilot installs host-scoped Git helper configuration. On first use, the broker obtains the actor's native Forgejo OAuth credential through standard authorization-code + PKCE and Tower Nostr sign-in. Native consent/session/CSRF and account security requirements remain effective. Do not inject a management PAT or bypass password/2FA prompts; an unsupported account requirement needs an explicit operator-facing error.

After expiry the helper discards the old credential and signs in again. A native 403 or private-repository 404 is normally an access problem, not proof of expiry. Check native effective access instead of repeatedly reauthenticating. There is no bootstrap worker or Tower repository resolution step.

Configure the canonical HTTPS remote without credentials. Git author configuration and provider authentication identity are separate; verify both for attribution. Push only to a permitted disposable/work branch and open a native pull request when target branches are protected.

## Access evidence

Verify `/api/v1/user` identifies the intended account and native permission reads show intended access. Test direct Git and API operations using that actor's OAuth token through the shipped path. Keep the same issued token when testing native collaborator/team permission changes. Do not use administrator tokens as access evidence for an agent.
