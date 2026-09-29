# Wingman first setup

Install the guided Wingman Be Free setup skill for your agent after this package is published to npm:

```sh
npx @wingmanbefree/setup
```

By default the installer writes the skill to Codex (`~/.codex/skills`), Claude Code (`~/.claude/skills`), Goose (`~/.config/goose/skills`), and OpenCode (`~/.config/opencode/skills`). Use `--target codex|claude|goose|opencode` for one tool, or `--skills-dir PATH` for a custom parent directory. Run with `--dry-run` to inspect destinations. Existing different copies are preserved unless you pass `--force`; replacement makes a timestamped backup. The installer does not install the agent binaries.

Then ask your agent: **“Use wingman-first-setup to set up my Wingman.”** The agent interviews you one decision at a time and records public choices in `.wingman-first-setup.json`. It offers Other Stuff Hosted Tower by default or a self-hosted Tower, helps with a Wingman App identity when needed, chooses Docker isolation or native Bun for existing agent tools, configures transport, and verifies a test reply. The installer only installs the skill; it does not deploy services or collect credentials.

This is a pilot. The skill reads the current Autopilot and Tower setup contracts before changing a host, and reports any unsupported combination or missing authority.

The canonical skill is maintained at the root of the [wm-skills repository](https://github.com/OtherStuffAI/wm-skills/tree/main/wingman-first-setup). `npm pack` copies it into the published package. From a Git checkout, run `npm pack` in `packages/setup`, then `npx --yes --package ./wingmanbefree-setup-0.2.0.tgz wingman-setup` to try the unpublished package.
