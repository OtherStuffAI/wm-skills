# Setup manifest

The agent maintains `.wingman-first-setup.json` in the chosen setup working directory. It is a resumable record, not a credential store. Use `null` for unanswered public fields and update `status` as the interview and setup progress. Keep it out of Git and set file mode `0600`.

```json
{
  "schema_version": 1,
  "status": "interview",
  "tower": {
    "mode": "other_stuff_hosted",
    "url": "https://tower-stable-api.b.otherstuff.ai/",
    "workspace_name": null,
    "workspace_id": null
  },
  "owner": {
    "identity_plan": "existing",
    "npub": null
  },
  "host": {
    "os": null,
    "location": "this_computer",
    "agent_tools_present": [],
    "agent_mode": null,
    "runtime": null
  },
  "transport": {
    "mode": null,
    "endpoint": null
  },
  "bot": {
    "name": null,
    "harness": null,
    "npub": null
  },
  "steps": {},
  "next_action": "Ask for the next missing choice"
}
```

Choices:

- `tower.mode`: `other_stuff_hosted` or `self_hosted`. Set `tower.url` to the exact selected origin, and use the hosted default only for the hosted mode.
- `owner.identity_plan`: `existing` or `wingman_app`. `owner.npub` must be the human account npub, not the Wingman App device npub or bot npub. The Wingman App path may be chosen before the npub exists; do not mark the manifest ready until identity setup produces it.
- `host.agent_mode`: `use_installed` or `isolated`. `host.runtime`: `bun` or `docker`. Prefer `bun` for installed tools when available; use `docker` for isolation.
- `transport.mode`: `local_http`, `public_https`, `fips_only`, or `https_and_fips`.
- `bot.harness`: the exact installed harness selected for the first bot, such as `codex`, `claude`, `goose`, or `opencode`.
- `status`: `interview`, `ready`, `in_progress`, `blocked`, or `complete`.

Record each completed step under `steps` with its status, observed public ID/URL, and validation evidence. Keep a precise `next_action` when blocked. Validate a ready manifest with `node scripts/check-manifest.mjs <path> --ready`, resolving the script relative to this skill directory. A valid manifest means the choices are coherent; it does not prove Tower authorization, runtime readiness, billing, or a working connection.
