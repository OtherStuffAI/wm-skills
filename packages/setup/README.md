# Wingman first setup

Install the guided Wingman Be Free setup skill for your agent after this package is published to npm:

```sh
npx @wingmanbefree/setup
```

The default destination is `~/.codex/skills/wingman-first-setup`. Use `--target claude` for `~/.claude/skills/wingman-first-setup`, or `--skills-dir PATH` for another skill-capable agent. Run with `--dry-run` to inspect the destination. An existing different copy is preserved unless you pass `--force`; replacement makes a timestamped backup.

Then ask your agent: **“Use wingman-first-setup to set up my Wingman.”** The skill guides the choice of Docker or native Bun, HTTPS/local HTTP/FIPS transport, Tower workspace, sovereign bot, connection, and a test reply. The installer only installs the skill; it does not deploy services or collect credentials.

This is a pilot. The skill reads the current Autopilot and Tower setup contracts before changing a host, and reports any unsupported combination or missing authority.

The canonical skill is maintained at the root of the [wm-skills repository](https://github.com/OtherStuffAI/wm-skills/tree/main/wingman-first-setup). `npm pack` copies it into the published package. From a Git checkout, run `npm pack` in `packages/setup`, then `npx --yes --package ./wingmanbefree-setup-0.1.0.tgz wingman-setup` to try the unpublished package.
