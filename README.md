# Wingman Skills

Sanitized, portable skills for working on Wingman Be Free.

## Skills

- `wingman-be-free-platform`: compact architecture and routing entrypoint
- `forgejo-tower`: Tower-backed Forgejo setup, organizations, repositories, users, sharing, issues, Actions, and CI
- `flight-deck-workflow`: Flight Deck and supervised work
- `wingmen-pipelines`: Autopilot declarative pipelines
- `wapps`: WApp integration and operation
- `wingman-deploy`: deployed-branch release workflow
- `artifacts`: Artifact WApp and visual review surfaces
- `wingman-first-setup`: first Tower workspace, Autopilot, sovereign bot, transport, and Flight Deck connection

The platform skill is intentionally short. Conditional operating detail belongs in its references or the specialist skill that owns the workflow.

## Paths

Current Wingman checkouts normally live under `~/code/wm`; older installations may use `~/code/wingmanbefree`. Skills should inspect both and then follow the live repository instructions.

## Install or update

The sync tool discovers every top-level directory containing `SKILL.md`, so adding a skill does not require editing a hard-coded list:

```bash
git clone https://github.com/OtherStuffAI/wm-skills.git ~/code/wm/wm-skills
cd ~/code/wm/wm-skills
python3 scripts/sync-skills.py sync \
  --codex-dir "$HOME/.codex/skills" \
  --claude-dir "$HOME/.claude/skills"
```

It replaces only this repository's named skill directories. Restart the client or begin a new session after syncing so skills are rediscovered.

For the first-setup skill alone, the `packages/setup` npm package installs it without cloning this repository. Once published to npm, run `npx @wingmanbefree/setup` (or add `--target claude`). The package bundles the canonical `wingman-first-setup` directory at pack time. Before publication, you can use this Git checkout directly:

```bash
cd packages/setup
npm pack
npx --yes --package ./wingmanbefree-setup-0.2.0.tgz wingman-setup
```

Check drift without modifying installed copies:

```bash
python3 scripts/sync-skills.py check \
  --codex-dir "$HOME/.codex/skills" \
  --claude-dir "$HOME/.claude/skills"
```

`check` exits `0` when managed skills are exact, `1` for drift, and `2` for invalid arguments or filesystem errors.

To update only the Forgejo workflow while preserving other installed skill edits,
add `--skill forgejo-tower` to either command. The option is repeatable; unknown
names fail before any installed directory changes.
